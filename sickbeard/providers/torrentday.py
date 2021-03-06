# coding=utf-8
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

import base64
import re
import time

from . import generic
from sickbeard.bs4_parser import BS4Parser
from sickbeard.helpers import tryInt, anon_url


class TorrentDayProvider(generic.TorrentProvider):

    def __init__(self):
        generic.TorrentProvider.__init__(self, 'TorrentDay')

        self.url_home = ['https://www.torrentday.com/'] + \
                        ['http://td.%s/' % base64.b64decode(x) for x in [''.join(x) for x in [
                            [re.sub('(?i)[I\s1]+', '', x[::-1]) for x in [
                                'y92d', 'zl12a', 'y9mY', 'n5 Wa', 'vNmIL', '=i1=Qb']],
                            [re.sub('(?i)[T\sq]+', '', x[::-1]) for x in [
                                '15TWd', 'hV 3c', 'lBHb', 'vNncq', 'j5ib', '=qQ02b']],
                        ]]]

        self.url_vars = {'login': 'rss.php', 'search': 't?%s%s&qf=&q=%s'}
        self.url_tmpl = {'config_provider_home_uri': '%(home)s', 'login': '%(home)s%(vars)s',
                         'search': '%(home)s%(vars)s'}

        self.categories = {'Season': [31, 33, 14], 'Episode': [24, 32, 26, 7, 34, 2], 'anime': [29]}
        self.categories['Cache'] = self.categories['Season'] + self.categories['Episode']

        self.proper_search_terms = None

        self.digest, self.freeleech, self.minseed, self.minleech = 4 * [None]

    def _authorised(self, **kwargs):

        return super(TorrentDayProvider, self)._authorised(
            logged_in=(lambda y='': all(
                ['RSS URL' in y, self.has_all_cookies()] +
                [(self.session.cookies.get(x) or 'sg!no!pw') in self.digest for x in 'uid', 'pass'])),
            failed_msg=(lambda y=None: u'Invalid cookie details for %s. Check settings'))

    @staticmethod
    def _has_signature(data=None):
        return generic.TorrentProvider._has_signature(data) or \
               (data and re.search(r'(?i)<title[^<]+?(td|torrentday)', data))

    def _search_provider(self, search_params, **kwargs):

        results = []
        if not self._authorised():
            return results

        items = {'Cache': [], 'Season': [], 'Episode': [], 'Propers': []}

        rc = dict((k, re.compile('(?i)' + v)) for (k, v) in {'get': 'download'}.items())
        for mode in search_params.keys():
            for search_string in search_params[mode]:
                search_string = '+'.join(search_string.split())

                search_url = self.urls['search'] % (
                    self._categories_string(mode, '%s=on'), ('&free=on', '')[not self.freeleech], search_string)

                html = self.get_url(search_url)
                if self.should_skip():
                    return results

                cnt = len(items[mode])
                try:
                    if not html or self._has_no_results(html):
                        raise generic.HaltParseException

                    with BS4Parser(html, features=['html5lib', 'permissive'], tag='table', attr='torrentTable') as soup:
                        torrent_table = soup.find('table', id='torrentTable')
                        torrent_rows = [] if not torrent_table else torrent_table.find_all('tr')

                        if 2 > len(torrent_rows):
                            raise generic.HaltParseException

                        head = None
                        for tr in torrent_rows[1:]:
                            cells = tr.find_all('td')
                            if 4 > len(cells):
                                continue
                            try:
                                head = head if None is not head else self._header_row(
                                    tr, header_strip='(?i)(?:leechers|seeders|size);')
                                seeders, leechers, size = [tryInt(n, n) for n in [
                                    cells[head[x]].get_text().strip() for x in 'seed', 'leech', 'size']]
                                if self._reject_item(seeders, leechers):
                                    continue

                                dl = tr.find('a', href=rc['get'])['href']
                                title = tr.find('a', href=re.compile(
                                    '/t/%s' % re.findall('download.*?/([^/]+)', dl)[0])).get_text().strip()
                                download_url = self._link(dl)
                            except (AttributeError, TypeError, ValueError, IndexError):
                                continue

                            if title and download_url:
                                items[mode].append((title, download_url, seeders, self._bytesizer(size)))

                except generic.HaltParseException:
                    pass
                except (StandardError, Exception):
                    time.sleep(1.1)

                self._log_search(mode, len(items[mode]) - cnt, search_url)

            results = self._sort_seeding(mode, results + items[mode])

        return results

    def _episode_strings(self, ep_obj, **kwargs):

        return super(TorrentDayProvider, self)._episode_strings(ep_obj, sep_date='.', date_or=True, **kwargs)

    def ui_string(self, key):
        if 'torrentday_digest' == key and self._valid_home():
            current_url = getattr(self, 'urls', {}).get('config_provider_home_uri')
            return ('use... \'uid=xx; pass=yy\'' +
                    (current_url and (' from a session logged in at <a target="_blank" href="%s">%s</a>' %
                                      (anon_url(current_url), current_url.strip('/'))) or ''))
        return ''


provider = TorrentDayProvider()
