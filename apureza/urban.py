# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2019, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'

from fototex.foto import Foto
from utils.sys.timer import Timer
from matplotlib import pyplot as plt
# test2 = Foto("/home/benjamin/Desktop/APUREZA/FOTO/Images/SUBSET_PLEIADES_20160915_Pan.tif", method="moving")
# test2 = Foto("//home/benjamin/Desktop/APUREZA/FOTO/Images/IMG_SPOT7_PMS_2018.TIF", band=4, method="moving",
#              in_memory=False)
test2 = Foto("/home/benjamin/Desktop/APUREZA/FOTO/Images/IMG_SPOT6_PMS_2013.TIF", band=4, method="moving",
             in_memory=False)
for w_size in [13]:
    with Timer() as t:
        test2.run(w_size, progress_bar=True, sklearn_pca=True)
    print("spent time (%d): %s" % (w_size, t))
    test2.save_rgb(progress_bar=True)
    # test2.save_rgb(f"/home/benjamin/Desktop/APUREZA/FOTO/rgb/rgb_spot_moving_{w_size}.tif", progress_bar=True)
# test2.fit_transform(test, progress_bar=True)
# plt.pcolor(test2.rgb[:, :, 0])
# plt.imshow(test2.rgb)
# plt.show()
