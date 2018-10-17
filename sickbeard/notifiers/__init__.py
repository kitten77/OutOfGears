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
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickGear.  If not, see <http://www.gnu.org/licenses/>.

import sickbeard.notifiers.emby
import sickbeard.notifiers.kodi
import sickbeard.notifiers.plex
# import xbmc
import sickbeard.notifiers.nmj
import sickbeard.notifiers.nmjv2
import sickbeard.notifiers.synoindex
import sickbeard.notifiers.synologynotifier
import sickbeard.notifiers.pytivo

import sickbeard.notifiers.boxcar2
# import pushalot
import sickbeard.notifiers.pushbullet
import sickbeard.notifiers.pushover
import sickbeard.notifiers.growl
import sickbeard.notifiers.prowl
from . import libnotify

from lib import libtrakt
import sickbeard.notifiers.trakt
import sickbeard.notifiers.slack
import sickbeard.notifiers.discordapp
import sickbeard.notifiers.gitter
import sickbeard.notifiers.tweet
import sickbeard.notifiers.emailnotify

import sickbeard


class NotifierFactory(object):

    def __init__(self):
        self.notifiers = dict(
            # home theater / nas
            EMBY=emby.EmbyNotifier,
            KODI=kodi.KodiNotifier,
            PLEX=plex.PLEXNotifier,
            # ### XBMC=xbmc.XBMCNotifier,
            NMJ=nmj.NMJNotifier,
            NMJV2=nmjv2.NMJv2Notifier,
            SYNOINDEX=synoindex.SynoIndexNotifier,
            SYNOLOGY=synologynotifier.SynologyNotifier,
            PYTIVO=pytivo.PyTivoNotifier,

            # devices,
            BOXCAR2=boxcar2.Boxcar2Notifier,
            # PUSHALOT=pushalot.PushalotNotifier,
            PUSHBULLET=pushbullet.PushbulletNotifier,
            PUSHOVER=pushover.PushoverNotifier,
            GROWL=growl.GrowlNotifier,
            PROWL=prowl.ProwlNotifier,
            LIBNOTIFY=libnotify.LibnotifyNotifier,

            # social
            TRAKT=trakt.TraktNotifier,
            SLACK=slack.SlackNotifier,
            DISCORDAPP=discordapp.DiscordappNotifier,
            GITTER=gitter.GitterNotifier,
            TWITTER=tweet.TwitterNotifier,
            EMAIL=emailnotify.EmailNotifier,
        )

    @property
    def enabled(self):
        """
        Generator to yield iterable IDs for enabled notifiers
        :return: ID String
        :rtype: String
        """
        for n in filter(lambda v: v.is_enabled(), self.notifiers.values()):
            yield n.id()

    @property
    def enabled_onsnatch(self):
        for n in filter(lambda v: v.is_enabled() and v.is_enabled_onsnatch(), self.notifiers.values()):
            yield n.id()

    @property
    def enabled_ondownload(self):
        for n in filter(lambda v: v.is_enabled() and v.is_enabled_ondownload(), self.notifiers.values()):
            yield n.id()

    @property
    def enabled_onsubtitledownload(self):
        for n in filter(lambda v: v.is_enabled() and v.is_enabled_onsubtitledownload(), self.notifiers.values()):
            yield n.id()

    @property
    def enabled_library(self):
        for n in filter(lambda v: v.is_enabled() and v.is_enabled_library(), self.notifiers.values()):
            yield n.id()

    def get(self, nid):
        """
        Get a notifier instance
        :param nid: Notified ID
        :type nid: String
        :return: Notifier instance
        :rtype: Notifier
        """
        return self.notifiers[nid]()

    def get_enabled(self, kind=None):
        """
        Generator to yield iterable notifier instance(s) that are either enabled or enabled for requested actions
        :param kind: Action
        :type kind: String
        :return: Notifier instance
        :rtype: Notifier
        """
        for n in getattr(self, 'enabled' + ('' if None is kind else ('_' + kind))):
            yield self.get(n)


def notify_snatch(ep_name):
    for n in NotifierFactory().get_enabled('onsnatch'):
        n.notify_snatch(ep_name)


def notify_download(ep_name):
    for n in NotifierFactory().get_enabled('ondownload'):
        n.notify_download(ep_name)


def notify_subtitle_download(ep_name, lang):
    for n in NotifierFactory().get_enabled('onsubtitledownload'):
        n.notify_subtitle_download(ep_name, lang)


def notify_git_update(new_version=''):
    if sickbeard.NOTIFY_ON_UPDATE:
        for n in NotifierFactory().get_enabled():
            n.notify_git_update(new_version)


def notify_update_library(ep_obj):
    for n in NotifierFactory().get_enabled('library'):
        n.update_library(show=ep_obj.show, show_name=ep_obj.show.name, ep_obj=ep_obj)
