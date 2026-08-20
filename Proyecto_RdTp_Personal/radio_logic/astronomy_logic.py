from astropy.coordinates import AltAz, SkyCoord, EarthLocation, get_sun
from astropy.time import Time
import astropy.units as u
from astropy.utils.iers import conf

conf.auto_max_age = None

# Location constant
casa = EarthLocation(lat=4.51 * u.deg, lon=-75.68 * u.deg)

def buscar_sol():
    """Calculates instantaneous Azimuth and Altitude for the Sun."""
    ahora = Time.now()
    sol_pos = get_sun(ahora).transform_to(AltAz(obstime=ahora, location=casa))
    return round(float(sol_pos.az.deg), 2), round(float(sol_pos.alt.deg), 2)

def rastrear(ra: float, dec: float):
    """Calculates instantaneous Azimuth and Altitude for given RA and DEC."""
    ahora = Time.now()
    objectC = SkyCoord(ra * u.deg, dec * u.deg)
    position = objectC.transform_to(AltAz(obstime=ahora, location=casa))
    return round(float(position.az.deg), 2), round(float(position.alt.deg), 2)
