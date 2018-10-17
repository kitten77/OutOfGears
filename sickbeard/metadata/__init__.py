# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of SickGear.
#
# SickGear is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickGear is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickGear.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ['generic', 'helpers', 'kodi', 'mede8er', 'mediabrowser', 'ps3', 'tivo', 'wdtv', 'xbmc', 'xbmc_12plus']

import sys

import sickbeard.metadata.kodi
import sickbeard.metadata.mede8er
import sickbeard.metadata.mediabrowser
import sickbeard.metadata.ps3
import sickbeard.metadata.tivo
import sickbeard.metadata.wdtv
import sickbeard.metadata.xbmc
import sickbeard.metadata.xbmc_12plus


def available_generators():
    return filter(lambda x: x not in ('generic', 'helpers'), __all__)


def _getMetadataModule(name):
    name = name.lower()
    prefix = "sickbeard.metadata."
    if name in __all__ and prefix + name in sys.modules:
        return sys.modules[prefix + name]
    else:
        return None


def _getMetadataClass(name):
    module = _getMetadataModule(name)

    if not module:
        return None

    return module.metadata_class()


def get_metadata_generator_dict():
    result = {}
    for cur_generator_id in available_generators():
        cur_generator = _getMetadataClass(cur_generator_id)
        if not cur_generator:
            continue
        result[cur_generator.name] = cur_generator

    return result
        
