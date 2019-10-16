from case_studies.swan_coastal_plain.CF_tensor import *
import numpy as np
from torch import *
from case_studies.swan_coastal_plain.CF_tensor import ClayFraction

log_x=torch.rand(1,10)*10
log_y = torch.rand(1,10)*10
log_cf= torch.rand(1,10)
aem_x = torch.rand(1,100)*10
aem_y = torch.rand(1,100)*10
aem_resist =  torch.rand(1,100,2)*100
constraint_pair =[2,3] #assume the constraint scale is 2*3
tolerant_err = torch.rand(1,6)
learning_rate =0.01

clay_fraction = ClayFraction(log_x,log_y,log_cf,aem_x,aem_y,aem_resist,constraint_pair,tolerant_err,learning_rate)


def test_translator_function():
    m_up=70
    m_low = 50
    fed_out = (2*clay_fraction.AEM_resist-m_up-m_low)/(m_up-m_low)
    interval = torch.FloatTensor([4,6])
    aem_cf = clay_fraction.translator_function(fed_out,interval)
    assert(aem_cf.size() == torch.Size([1,100]))
    print('translator function test passed')
    return aem_cf


def test_kriging_interpolation(aem_cf):
    interpolated_cf, interpolated_var = clay_fraction.Kriging_interpolation(aem_cf)
    assert (interpolated_cf.size() == torch.Size([10]))
    assert (interpolated_var.size() == torch.Size([10]))
    print('Kriging interpolation dimension test passed')
    return interpolated_cf,interpolated_var

def test_regularisation_constraint():
    print(clay_fraction.regularization_constraint())
    print('reg constraint test passed')

def test_regularisation_data():
    print(clay_fraction.regularization_data(interpolated_cf,interpolated_var))
    print('reg data test passed')

def test_objective_function():
    print(clay_fraction.objective_function(interpolated_cf,interpolated_var))
    print('obj function test passed')

aem_cf = test_translator_function()
interpolated_cf, interpolated_var = test_kriging_interpolation(aem_cf)
test_regularisation_constraint()
test_regularisation_data()
test_objective_function()

"""
The tensor version is difficult to test, so I tried to print important tensors and checked them with manual calculation 
result. However, this can be adapted to a representation of interface. The shape/format of input tensors can be indicated 
here.
"""