from util import tprint
import requests
import html.parser
from urllib import parse
import json

class _DummyXMLParser(html.parser.HTMLParser):
    "Dummy XML parser. Not using XML parser because of malformed XML feeds."
    _ignore = True
    _isLink = False
    _lastTag = None

    _pool = []

    def resetPool(self):
        self._pool = []

    @property
    def pool(self):
        return self._pool

    def handle_starttag(self, tag, attrs):
        if tag == "item":
            self._ignore = False
            tprint("-- Torrent --")
            self._pool.append({})
        elif not self._ignore:
            tprint(tag + ":", end=" ")
            self._lastTag = tag
            self._pool[-1][self._lastTag] = None
        if tag == "link":
            self._isLink = True

    def handle_data(self, data):
        if data.strip() and not self._ignore:
            if self._isLink:
                data = data.replace(" ", "%20")
            tprint(data, end=" ")
            self._pool[-1][self._lastTag] = data

    handle_comment = handle_data
    handle_decl = handle_data

    def handle_endtag(self, tag):
        if tag == "item":
            self._ignore = True
        elif tag == "link":
            self._isLink = False
        tprint()

class Scout(object):
    "Find torrents from ThePirateBay and compare against IMDB"

    _FEEDS = [
        "https://piratebay.to/pub/rss/Category_1.rss.xml",
        "https://nyaa.si/?page=rss"
    ]
    _HTML_PARSER = _DummyXMLParser()

    def __init__(self, queries=None, blacklist=None):
        self.queries = queries if queries else []
        self.blacklist = blacklist if blacklist else []
        self.torrentPool = []

    def _grabTorrentPool(self):
        for feed in self._FEEDS:
            self._HTML_PARSER.resetPool()
            response = requests.get(feed)
            if response.ok:
                self._HTML_PARSER.feed(response.text)
            input(json.dumps(self._HTML_PARSER.pool, indent=2))
            