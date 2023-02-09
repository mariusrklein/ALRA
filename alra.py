import warnings
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri as numpy2ri
from rpy2.robjects.packages import importr
import numpy as np

class alraInstance():

    def __init__(self) -> None:
        self.r = robjects.r
        try:
            self.rsvd = importr('RSVD')
        except:
            warnings.warn('R package RSVD is required for ALRA. Please run ' +
                          'alraInstance.install_r_packages() to install it.')
        
        numpy2ri.activate()
        self.r.source('alra.R')

    def install_r_packages(self):
        self.r.source('install.R')

    def alra(
        self,
        a_norm: np.array,
        k=0,
        q=10,
        quantile_prob = 0.001,
        use_mkl = False,
        mkl_seed=-1
    ) -> np.array:
        
        R_array = numpy2ri.numpy2rpy(a_norm)

        R_imputed = self.r.alra(
            A_norm = R_array,
            k = k,
            q = q,
            quantile_prob = quantile_prob,
            use_mkl = use_mkl,
            mkl_seed = mkl_seed
        )

        py_array = np.array(R_imputed)

        return (py_array[0], py_array[1], py_array[2])
