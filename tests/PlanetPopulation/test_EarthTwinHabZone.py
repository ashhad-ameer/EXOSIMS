r"""Test code for modules EarthTwinHabZone1 and EarthTwinHabZone2 within EXOSIMS PlanetPopulation.

Cate Liu, IPAC, 2016"""

import unittest
from EXOSIMS.Prototypes.PlanetPopulation import PlanetPopulation
from EXOSIMS.PlanetPopulation.EarthTwinHabZone1 import EarthTwinHabZone1
from EXOSIMS.PlanetPopulation.EarthTwinHabZone2 import EarthTwinHabZone2
from EXOSIMS.PlanetPopulation.EarthTwinHabZone3 import EarthTwinHabZone3
import numpy as np
from astropy import units as u
import scipy.stats


class TestEarthTwinHabZone(unittest.TestCase):
    
    def setUp(self):
        self.spec = {'modules':{'PlanetPhysicalModel': ''}}
        self.x = 10000

        #critical value chi^2: chi^2 must be smaller than this value for .01 significance
        self.crit = scipy.stats.chi2.ppf(1-.01,99)
        pass
    
    def tearDown(self):
        pass

    # helper function for asserting histogram passes a chisquare test
    def chisquare_test_helper(self, hist_param):
        h = np.histogram(hist_param,100,density=False)
        chi2 = scipy.stats.chisquare(h[0])
        self.assertLess(chi2[0], self.crit)
        #assert that chi^2 is less than critical value

    def test_gen_plan_params_zone1(self):
        r"""Test generated planet parameters:
        Expected: all 1 R_E, all p = 0.67, e = 0, and uniform a in arange
        Updated by Sonny Rapapport, Cornell 7/16/2021. Strategy: Generate the histogram of values for 
        the generated values. As the distribution should be uniform, just check that all the buckets
        in the histogram have approximately even distributions with a chi^2 test. 
        """

        obj = EarthTwinHabZone1(**self.spec)

        a, e, p, Rp = obj.gen_plan_params(self.x)
        
        assert(np.all(e == 0))
        assert(np.all(p == 0.367))
        assert(np.all(Rp == 1.0*u.R_earth))

        self.chisquare_test_helper(a.to('AU').value)

    def test_gen_plan_params_zone2(self):
        r"""Test generated planet parameters:
        Expected: all 1 R_E, all p = 0.67, e = 0, and uniform a,e in arange,erange
        Updated by Sonny Rapapport, Cornell 7/16/2021. Strategy: Generate the histogram of values for 
        the generated values. As the distribution should be uniform, just check that all the buckets
        in the histogram have approximately even distributions with a chi^2 test. 
        
        """

        obj = EarthTwinHabZone2(constrainOrbits=False,erange=[0.1,0.5],**self.spec)

        a, e, p, Rp = obj.gen_plan_params(self.x)
        
        assert(np.all(p == 0.367))
        assert(np.all(Rp == 1.0*u.R_earth))

        for param,param_range in zip([a.value,e],[obj.arange.value,obj.erange]):
            self.chisquare_test_helper(param)
        
    def test_gen_sma_zone3(self):
        r"""Tests generated semi-major axis
        Strategy: Uses chi^2 test to check that uniform distribution is indeed uniform
        
        """

        obj = EarthTwinHabZone3(**self.spec)
        a = obj.gen_sma(self.x)
        self.chisquare_test_helper(a.to('AU').value)

    
if __name__ == "__main__":
    unittest.main()
