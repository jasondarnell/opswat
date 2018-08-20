import pkg_resources as pkgr

from opswat.meta_defender.meta_defender_api import MetaDefenderApi

try:
    __version__ = pkgr.get_distribution(__name__).version
except pkgr.DistributionNotFound as e:
    __version__ = 'dev'