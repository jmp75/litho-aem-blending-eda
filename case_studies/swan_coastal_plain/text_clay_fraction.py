from case_studies.swan_coastal_plain.clayfraction import  *
import numpy as np


def test_bore_to_fraction():
    bore_dict = {(0.61, 0.0): "subsoil",
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
    fraction_list = bore_to_fraction(10, bore_dict)
    print(fraction_list)
    np.testing.assert_almost_equal (fraction_list[(0.61, 0.0)], 0)
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
    fraction_list = bore_to_fraction(10,bore_dict)
    np.testing.assert_almost_equal(fraction_list[(10,0)],1)
    print("bore_to_fraction test all passed")


def test_translator_function() :
    np.testing.assert_almost_equal(translator_function(50), 0.743225,5)
    np.testing.assert_almost_equal(translator_function(10), 1,5)
    np.testing.assert_almost_equal(translator_function(100), 0,5)
    np.testing.assert_almost_equal(translator_function(50,30,60),0.256774,5)
    np.testing.assert_almost_equal(translator_function(10,30,60),1,5)
    np.testing.assert_almost_equal(translator_function(100,30,60),0,5)
    print("translator_function all past")


#def test_resist_to_fraction():




test_bore_to_fraction()
test_translator_function()
