#-plugin-sig:VbtoObE5WJjtyyzTgarUcbCYqCFTefL0c20QMCzQI06WEcri3Ww08A3TjhzVcAngUe1qTbJ6DXfYPURn8JDrPsC+fhOBCUcfRAzNIfW9Sk7RO1zC1G1nOJa2G57B8WYdJ73UB7GrWKRS6zhhDT9BngUIz4WX00xC5vNDPoAe4lfA+Z5eILeFxTUjpRls6a7wtxCOjSiuq0okOzKju8EdTzv25ho+J51x0//h12TrDy6DYpCgptycJGTQNVbbPnZ7hg2dgkVLdQPDgqHoHiGVEfExhrvvcW05anoEaBjfHaM205oo2ioYO+n5R5t/bR9end3PoVrNtjtZLx71ilz+zg==
import random
import re

from ACEStream.PluginsContainer.livestreamer.plugin import Plugin
from ACEStream.PluginsContainer.livestreamer.plugin.api import http, validate
from ACEStream.PluginsContainer.livestreamer.stream import RTMPStream

PLAYER_VERSION = "0.1.1.767"
INFO_URL = "http://mvn.vaughnsoft.net/video/edge/mnt-{domain}_{channel}?{version}_{ms}-{ms}-{random}"

DOMAIN_MAP = {
    "breakers": "btv",
    "vapers": "vtv",
    "vaughnlive": "live",
}

_url_re = re.compile("""
    http(s)?://(\w+\.)?
    (?P<domain>vaughnlive|breakers|instagib|vapers).tv
    (/embed/video)?
    /(?P<channel>[^/&?]+)
""", re.VERBOSE)

_swf_player_re = re.compile('swfobject.embedSWF\("(/\d+/swf/[0-9A-Za-z]+\.swf)"')

_schema = validate.Schema(
    validate.transform(lambda s: s.split(";")),
    validate.length(3),
    validate.union({
        "server": validate.all(
            validate.get(0),
            validate.text
        ),
        "token": validate.all(
            validate.get(1),
            validate.text,
            validate.startswith(":mvnkey-"),
            validate.transform(lambda s: s[len(":mvnkey-"):])
        ),
        "ingest": validate.all(
            validate.get(2),
            validate.text
        )
    })
)


class VaughnLive(Plugin):
    @classmethod
    def can_handle_url(cls, url):
        return _url_re.match(url)

    def _get_streams(self):
        res = http.get(self.url)
        match = _swf_player_re.search(res.text)
        if match is None:
            return
        swfUrl = "http://vaughnlive.tv" + match.group(1)

        match = _url_re.match(self.url)
        params = {}
        params["channel"] = match.group("channel").lower()
        params["domain"] = DOMAIN_MAP.get(match.group("domain"), match.group("domain"))
        params["version"] = PLAYER_VERSION
        params["ms"] = random.randint(0, 999)
        params["random"] = random.random()
        info = http.get(INFO_URL.format(**params), schema=_schema)

        app = "live"
        if info["server"] in ["198.255.17.18:1337", "198.255.17.66:1337", "50.7.188.2:1337"]:
            if info["ingest"] == "SJC":
                app = "live-sjc"
            elif info["ingest"] == "NYC":
                app = "live-nyc"
            elif info["ingest"] == "ORD":
                app = "live-ord"
            elif info["ingest"] == "AMS":
                app = "live-ams"
            elif info["ingest"] == "DEN":
                app = "live-den"

        stream = RTMPStream(self.session, {
            "rtmp": "rtmp://{0}/live".format(info["server"]),
            "app": "{0}?{1}".format(app, info["token"]),
            "swfVfy": swfUrl,
            "pageUrl": self.url,
            "live": True,
            "playpath": "{domain}_{channel}".format(**params),
        })

        return dict(live=stream)

__plugin__ = VaughnLive
