from EXOSIMS.Prototypes.StarCatalog import StarCatalog
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord

class FakeCatalog_Uniform_Adj_Bounds(StarCatalog):
    
    def __init__(self, lat_sep=0.3, lon_sep=0.3, star_dist=1, lon_range=[0,360], lat_range=[-90,90], lat_extra = np.array([]), lon_extra = np.array([]), dist_extra = np.array([]), **specs):
        """
        lon_sep and lat_sep should be in deg
        """
        
        StarCatalog.__init__(self,**specs)
        
        lonRng = np.arange(  lon_range[0],lon_range[-1],lon_sep)
        latRng = np.arange(lat_range[0]+lat_sep, lat_range[-1],lat_sep) #not including the 90 deg this way, I get a singularity...
        
        lon,lat = np.meshgrid(lonRng,latRng)
        
        lon_Array = np.hstack([lon_extra,lon.flatten()])*u.deg
        lat_Array = np.hstack([lat_extra,lat.flatten()])*u.deg
        
        # putting it all together
        dists = star_dist*np.ones(len(lon.flatten()))
        dists = np.hstack([dist_extra,dists])*u.pc
        
        # ntargs must be an integer >= 1
        self.ntargs = max(int(lon_Array.size), 1)
    
        
        # reference star should be first on the list
        coords = SkyCoord(lon_Array,lat_Array,dists,frame='barycentrictrueecliptic')
        # coords = coords.transform_to('icrs')
        
        # list of astropy attributes
        self.coords = coords     # barycentric true ecliptic coordinates
        self.dist = dists             # distance
        self.parx = self.dist.to('mas', equivalencies=u.parallax())  # parallax
        self.pmra = np.zeros(self.ntargs)*u.mas/u.yr                 # proper motion in RA
        self.pmdec = np.zeros(self.ntargs)*u.mas/u.yr                # proper motion in DEC
        self.rv = np.zeros(self.ntargs)*u.km/u.s                     # radial velocity
        
        # list of non-astropy attributes to pass target list filters
        self.Name = np.array([str(x) for x in range(self.ntargs)])   # star names
        self.Spec = np.array(['G']*self.ntargs)                      # spectral types
        self.Umag = np.zeros(self.ntargs)                            # U magnitude
        self.Bmag = np.zeros(self.ntargs)                            # B magnitude
        self.Vmag = 5*np.ones(self.ntargs)                           # V magnitude
        self.Rmag = np.zeros(self.ntargs)                            # R magnitude
        self.Imag = np.zeros(self.ntargs)                            # I magnitude
        self.Jmag = np.zeros(self.ntargs)                            # J magnitude
        self.Hmag = np.zeros(self.ntargs)                            # H magnitude
        self.Kmag = np.zeros(self.ntargs)                            # K magnitude
        self.BV = np.zeros(self.ntargs)                              # B-V Johnson magnitude
        self.MV   = self.Vmag - 5*( np.log10(star_dist) - 1 )   # absolute V magnitude 
        self.BC   = -0.10*np.ones(self.ntargs)                       # bolometric correction
        
        BM        = self.MV + self.BC
        L0        = 3.0128e28
        BMsun     = 4.74
        self.L    = L0*10**(0.4*(BMsun-BM))                     # stellar luminosity in ln(SolLum)
        self.Binary_Cut = np.zeros(self.ntargs, dtype=bool)          # binary closer than 10 arcsec
        
        # populate outspecs
        self._outspec['ntargs'] = self.ntargs
        
        
