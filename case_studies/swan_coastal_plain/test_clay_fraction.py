from case_studies.swan_coastal_plain.clayfraction import *
import numpy as np


def test_bore_to_fraction():
    bore_dict = {(0.61, 0.0): "subsoil", #'clay',
                 (0, -0.61): "clay",
                 (-0.61, -1.52): "boulder",
                 (-1.52, -6.71): "limestone",
                 (-6.71, -10.36): "limestone",
                 (-10.36, -11.89): "clay",
                 (-11.89, -12.8): "limestone",
                 (-12.8, -14.93): "strata",
                 (-14.93, -18.59): "limestone",
                 (-18.59, -38.71): "limestone",
                 (-38.71, -40.23): "limestone",
                 (-40.23, -62.18): "limestone",
                 (-62.18, -77.72): "clay",
                 (-77.72, -86.87): "limestone"}
    fraction_list = bore_to_fraction(10, 10,bore_dict)
    print(fraction_list)
    np.testing.assert_almost_equal (fraction_list[(10, 0.0)], 0)
    np.testing.assert_almost_equal(fraction_list[(0.0, -10.0)] , 0.061)
    np.testing.assert_almost_equal(fraction_list[(-10.0, -20.0)] , 0.153)
    np.testing.assert_almost_equal(fraction_list[(-20.0, -30.0)] , 0)
    np.testing.assert_almost_equal(fraction_list[(-40, -50)] , 0)
    np.testing.assert_almost_equal(fraction_list[(-50, -60)] , 0)
    np.testing.assert_almost_equal(fraction_list[(-60, -70)] , 0.782)
    np.testing.assert_almost_equal(fraction_list[(-70, -80)] , 0.772)
    np.testing.assert_almost_equal(fraction_list[(-80, -86.87)] , 0)
    print("bore_to_fraction test all passed")
    bore_dict = {(11, -1): "clay"}
    fraction_list = bore_to_fraction(10,10,bore_dict)
    np.testing.assert_almost_equal(fraction_list[(10,0)],1)
    print("bore_to_fraction test all passed")


def test_translator_function() :
    np.testing.assert_almost_equal(translator_function(50), 0.743225,5)
    np.testing.assert_almost_equal(translator_function(10), 1,5)
    np.testing.assert_almost_equal(translator_function(100), 0,5)
    np.testing.assert_almost_equal(translator_function(50,30,60),0.256774,5)
    np.testing.assert_almost_equal(translator_function(10,30,60),1,5)
    np.testing.assert_almost_equal(translator_function(100,30,60),0,5)
    print("translator_function all passed")


def test_resist_to_fraction():
    interval = (10,0)
    resist_dict = {(12,-1): 50}
    np.testing.assert_almost_equal(resist_to_fraction(interval, resist_dict, translator_function, False), 0.743225,5) # layer cover whole interval
    ##TODO: more tests for different cases
    print("resist to fraction all passed")


def test_kriging_to_borehole():

    data = np.array([[0.3, 1.2, 0.47],
                     [1.9, 0.6, 0.56],
                     [1.1, 3.2, 0.74],
                     [3.3, 4.4, 1.47],
                     [4.7, 3.8, 1.74]])

    gridx = np.arange(0.0, 5.5, 0.5)
    gridy = np.arange(0.0, 5.5, 0.5)

    z,ss = kriging_to_borehole(data[:,0],data[:,1],data[:,2], gridx,gridy)
    np.testing.assert_equal(len(z),11)
    print("all tests passed")


test_bore_to_fraction()
test_translator_function()
test_resist_to_fraction()
test_kriging_to_borehole()