"""
An attempt to implementing Clay Fraction approach in Pytorch.
"""
from math import sqrt

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math.log as ln
import scipy.special as special



class ClayFraction(nn.Module):
    """Define the computation graph for clay fraction model."""

    def __init__(self, log_X, log_Y, log_CF, AEM_X, AEM_Y, AEM_resist, constraint_pair, tolerant_err, learning_rate,num_Neighbor):
        """Init the model with default parameters/hyperparameters."""
        super(ClayFraction, self).__init__()
        self.log_X = log_X
        self.log_Y = log_Y
        self.log_CF = log_CF
        self.AEM_X = AEM_X
        self.AEM_Y = AEM_Y
        self.AEM_resist = AEM_resist
        self.constraint_pair = constraint_pair
        self.tolerant_err = tolerant_err
        self.neighbor = num_Neighbor
        self.loss_func = self.objective_function
        self.model = nn.Linear(1,1)
        self.leaning_rate = learning_rate
        self.optimizer = torch.optim.SGD(self.parameters(), lr=self.learning_rate)

    def forward(self):
        # raise NotImplementedError
        fed_out = self.model(self.AEM_resist)
        self.translator_function(fed_out)
        interpolated_CF, resist_variance = self.Kriging_interpolation()
        return interpolated_CF,resist_variance

    def translator_function(self,fed_out):
        k= special.erfcinv(0.05)
        self.AEM_CF = 0.5*torch.erfc(k*fed_out)
        return self.AEM_CF


    def Kriging_interpolation (self):
        log_X = self.log_X
        log_Y = self.log_Y
        AEM_X = self.AEM_X
        AEM_Y = self.AEM_Y
        AEM_CF = self.AEM_CF
        num = self.neighbor
        #TODO: implement kriging interpolation in tensor.
        return 0,0  #interpolated_CF,resist_variance

    def regularization_data(self,resist_fraction, resist_variance):
        log_CF = self.log_CF
        total = torch.sum(log_CF)
        length = log_CF.size()[1]
        log_deviation = log_CF- (total-log_CF)/(length-1)
        log_deviation_trans = torch.transpose(log_deviation,0,1)
        log_variance_trans = torch.mul(log_deviation_trans,log_deviation_trans)
        sum_variance_trans = torch.transpose(resist_variance,0,1) +log_variance_trans
        reciprocal_variance = torch.reciprocal(sum_variance_trans)
        diff_CF_trans = torch.transpose(log_CF- resist_fraction,0,1)
        term_trans = torch.mul(diff_CF_trans,reciprocal_variance)
        term = torch.transpose(term_trans,0,1)
        sum_term = torch.matmul(term, term_trans)
        res = sqrt(1/length * sum_term)
        return res

    def regularization_constraint(self):
        constraint_pair = self.constraint_pair
        con_horizontal  = constraint_pair[0]
        con_vertical = constraint_pair[1]
        tolerant_err= self.tolerant_err
        log_err = torch.reciprocal(torch.log(tolerant_err))
        term = torch.mul(log_err,ln(con_horizontal) - ln(con_vertical))
        trans_err = torch.transpose(term,0,1)
        mul_err = torch.matmul(log_err,trans_err)
        length = tolerant_err.size()[1]
        res = sqrt(1/length * mul_err)
        return res

    def objective_function(self, resist_fraction, resist_variance):
        n_data = self.log_CF.size()[1]
        n_constraint = self.tolerant_err.size()[1]
        reg_data = self.regularization_data(self, resist_fraction,resist_variance)
        reg_constraint = self.regularization_constraint(self)
        res = sqrt((n_data*reg_data**2+n_constraint*reg_constraint**2)/(n_data+n_constraint))
        return res
