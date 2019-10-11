# -*- coding: utf-8 -*-

""" Machine learning tools

More detailed description.
"""
import copy
import warnings
from abc import abstractmethod

from keras import Sequential
from keras.callbacks import EarlyStopping
from keras.layers import Dense, BatchNormalization
from numpy import genfromtxt, savetxt
from scipy.stats import pearsonr
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from apureza.exceptions import KerasMlpError, DataWarning, DataError


class Data:

    _normalizer = None
    _standardizer = None

    def __init__(self, data):
        """ Data constructor

        :param data: numpy array
        """
        try:
            if data.ndim == 1:
                data = data.reshape(-1, 1)
        except AttributeError:
            raise DataError("Input must be a numpy array but is '%s'" % type(data))

        self._data = data

    def _inv_scale(self, scaler_name):
        scaler_name = "_" + scaler_name
        scale_data = self.copy()

        if self.__getattribute__(scaler_name):
            scale_data.__setattr__(scaler_name, None)
            scale_data._data = self.__getattribute__(scaler_name).inverse_transform(self._data)

        return scale_data

    def _scale(self, scaler_name, scaler):
        scaler_name = "_" + scaler_name
        scale_data = self.copy()

        if not self.__getattribute__(scaler_name):
            scale_data.__setattr__(scaler_name, scaler)
            scale_data._data = scaler.fit_transform(self._data)
        else:
            warnings.warn("Cannot scale data that have already been scaled", DataWarning)

        return scale_data

    def __repr__(self):
        return repr(self._data)

    def copy(self):
        return copy.deepcopy(self)

    def normalize(self, lower_bound=0, upper_bound=1):
        """ Normalize data

         Rescale from original range to the new range [lower_bound; upper_bound]
        :param lower_bound: lower bound of the new range
        :param upper_bound: upper bound of the new range
        :return:
        """
        return self._scale("normalizer", MinMaxScaler(feature_range=(lower_bound, upper_bound)))

    def normalize_inv(self):
        """ Inverse normalization transform

        :return:
        """
        return self._inv_scale("normalizer")

    def pearson(self, other):
        """ Compute pearson correlation coefficient

        :param other:
        :return:
        """
        try:
            cc, p_value = pearsonr(self._data, other._data)
        except TypeError:
            try:
                cc, p_value = pearsonr(self._data.flatten(), other._data.flatten())
            except ValueError:
                raise DataError("Input must have the same length")
        except AttributeError:
            raise DataError("Input must be a Data class instance but is '%s'" % type(other))

        return cc, p_value

    def standardize(self):
        """ Standardize data

        Standardization: rescaling distribution of values so that
        the mean of observed values is 0 and standard deviation is 1.
        :return:
        """
        return self._scale("standardizer", StandardScaler())

    def standardize_inv(self):
        """ Inverse standardization transform

        :return:
        """
        return self._inv_scale("standardizer")

    def to_csv(self, path_to_file, delimiter=","):
        """ Write to csv file

        :return:
        """
        savetxt(path_to_file, self._data, delimiter=delimiter)

    @property
    def values(self):
        return self._data.copy()

    @property
    def normalizer(self):
        return self._normalizer

    @property
    def standardizer(self):
        return self._standardizer

    @classmethod
    def from_csv(cls, path_to_file, delimiter=","):
        return cls(genfromtxt(path_to_file, delimiter=delimiter))


class ImgData(Data):
    """ Image data

    """


class NeuralNetwork:

    model = None

    @abstractmethod
    def build(self, *args, **kwargs):
        pass

    @abstractmethod
    def train(self, *args, **kwargs):
        pass

    @abstractmethod
    def predict(self, *args, **kwargs):
        pass


class KerasMlp(NeuralNetwork):
    """ Keras-based multilayer perceptron

    """

    def __init__(self):

        self.model = Sequential()

    def build(self, nb_inputs, nb_outputs, nb_hidden_layer=1, hidden_activation=('sigmoid',), nb_hidden_units=(32,),
              output_activation='linear'):
        """ Build network architecture

        :param nb_inputs: number of input units
        :param nb_outputs: number of output units
        :param nb_hidden_layer: number of hidden layer
        :param hidden_activation: activation function type for each hidden layer
        :param nb_hidden_units: number of hidden units for each hidden layer
        :param output_activation: output activation function type
        :return:
        """
        try:
            assert nb_hidden_layer == len(hidden_activation) == len(nb_hidden_units)
        except AssertionError:
            raise KerasMlpError("Hidden attributes must have the same size:\n -nb of hidden layers=%d\n -hidden "
                                "activation functions=%d\n -hidden units tuple length=%d" %
                                (nb_hidden_layer, len(hidden_activation), len(nb_hidden_units)))
        # Hidden layers
        for layer in range(nb_hidden_layer):
            self.model.add(BatchNormalization(input_shape=(4,)))
            self.model.add(Dense(units=nb_hidden_units[layer], activation=hidden_activation[layer]))

        # Output layer
        self.model.add(Dense(units=nb_outputs, activation=output_activation))

        return self

    def train(self, input_data, output_target, batch_size=None, validation_split=0.3, epochs=100,
              early_stopping=True, stop_after=10, min_delta=1e-6, monitor='val_loss', optimizer='rmsprop',
              loss_function='mean_squared_error'):
        """ Train neural network

        :param input_data: Data class instance for input data
        :param output_target: Data class instance for output target(s)
        :param batch_size: number of samples per gradient update
        :param validation_split: value for validation samples within data
        :param epochs:
        :param early_stopping:
        :param stop_after: nb of epochs to stop after (if early_stopping is True)
        :param min_delta: minimum change in the monitored quantity to qualify as an improvement
        :param monitor: which loss to monitor for early stopping ('loss' or 'val_loss')
        :param optimizer: optimizer name
        :param loss_function: loss function name
        :return:
        """

        # Compile model
        self.model.compile(optimizer=optimizer, loss=loss_function)

        # Early stopping
        if early_stopping:
            early_stopping = [EarlyStopping(monitor=monitor, min_delta=min_delta, patience=stop_after,
                                            restore_best_weights=True)]
        else:
            early_stopping = None

        # Train model using keras "fit" model function
        self.model.fit(input_data.values, output_target.values, callbacks=early_stopping, batch_size=batch_size,
                       validation_split=validation_split, epochs=epochs)

        return self

    def predict(self, input_data, *args, **kwargs):
        """

        :param input_data:
        :param args:
        :param kwargs:
        :return:
        """
        return input_data.__class__(self.model.predict(input_data.values))


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    rgb = Data.from_csv("/home/benjamin/Documents/apureza/data/rg_meanpan_ndvi.csv").normalize(-1, 1)
    density = Data.from_csv("/home/benjamin/Documents/apureza/data/density.csv")
    ann = KerasMlp().build(nb_inputs=4, nb_outputs=1).train(rgb, density, batch_size=32, validation_split=0.4,
                                                            epochs=200, early_stopping=False)
    estimated_density = ann.predict(rgb)
    print("corr coeff = %.2f (p-value = %f)" % estimated_density.pearson(density))
    measured_density = density.values
    plt.figure(1)
    plt.imshow(estimated_density.reshape(88, 125))
    plt.figure(2)
    plt.imshow(measured_density.reshape(88, 125))
    plt.show()
