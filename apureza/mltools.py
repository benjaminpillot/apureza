# -*- coding: utf-8 -*-

""" Machine learning tools

More detailed description.
"""
from keras import Sequential
from keras.layers import Dense
from numpy import genfromtxt
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from apureza.exceptions import KerasMlpError


class Data:

    _normalizer = None
    _standardizer = None

    def __init__(self, data):
        self._data = data

    def __repr__(self):
        return repr(self._data)

    def normalize(self, lower_bound=0, upper_bound=1):
        """ Normalize data

         Rescale from original range to the new range [lower_bound; upper_bound]
        :param lower_bound:
        :param upper_bound:
        :return:
        """
        self._normalizer = MinMaxScaler(feature_range=(lower_bound, upper_bound))
        normalize_data = self.__class__(self._normalizer.fit_transform(self._data))

    def normalize_inv(self, normalizer):
        """ Inverse normalization transform

        :param normalizer:
        :return:
        """
        return self.__class__(normalizer.inverse_transform(self._data))

    def standardize(self):
        """ Standardize data

        Standardization: rescaling distribution of values so that
        the mean of observed values is 0 and standard deviation is 1.
        :return:
        """
        self._standardizer = StandardScaler()
        return self.__class__(self._standardizer.fit_transform(self._data))

    def standardize_inv(self, standardizer):
        """ Inverse standardization transform

        :param standardizer: StandardScaler instance
        :return:
        """
        return self.__class__(standardizer.inverse_transform(self._data))

    @classmethod
    def from_csv(cls, path_to_file, delimiter=","):
        return cls(genfromtxt(path_to_file, delimiter=delimiter))


class ImgData(Data):
    """ Image data

    """


class KerasMlp:
    """ Keras-based multilayer perceptron

    """

    def __init__(self):

        self.model = Sequential()

    def build(self, nb_inputs, nb_outputs, nb_hidden_layer=1, hidden_activation=('sigmoid',), nb_hidden_units=(32,),
              output_activation='linear'):
        """ Build network architecture

        :param nb_inputs:
        :param nb_outputs:
        :param nb_hidden_layer:
        :param hidden_activation:
        :param nb_hidden_units:
        :param output_activation:
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
            self.model.add(Dense(units=nb_hidden_units[layer], activation=hidden_activation[layer],
                                 input_dim=nb_inputs))

        # Output layer
        self.model.add(Dense(units=nb_outputs, activation=output_activation))

        # Compile model
        self.model.compile(optimizer='rmsprop', loss='mse')

    def train(self):
        """ Train neural network

        :return:
        """