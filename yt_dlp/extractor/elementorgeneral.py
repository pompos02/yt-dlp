from .common import InfoExtractor
import re
from ..utils import (
    ExtractorError,
    traverse_obj,
    clean_html,
    unescapeHTML,
)

class ElementorGeneralIE(InfoExtractor):
    _VALID_URL = False
    _TESTS = [{
        'url': 'https://capitaltv.cy/2023/12/14/υγεια-και-ζωη-14-12-2023-δρ-ξενια-κωσταντινιδο/',
        'info_dict': {
            'id': 'https://www.youtube.com/watch?v=KgzuxwuQwM4',
            'ext': 'mp4',
            'title': 'ΥΓΕΙΑ ΚΑΙ ΖΩΗ 14 12 2023 ΔΡ  ΞΕΝΙΑ ΚΩΣΤΑΝΤΙΝΙΔΟΥ',
            'url': 'https://www.youtube.com/watch?v=KgzuxwuQwM4',
            'thumbnail': 'https://i.ytimg.com/vi/KgzuxwuQwM4/maxresdefault.jpg',
            'ie_key': 'Youtube',
        },
    }, {
        'url': 'https://elementor.com/academy/theme-builder-collection/?playlist=76011151&video=9e59909',
        'info_dict': {
            'id': '76011151&video=9e59909',
            'title': 'theme-builder-collection',
        },
        'playlist_mincount': 2,
        'params': {
            'skip_download': True,
        },
    }]
    def _extract_from_webpage(self, url, webpage):
        for element in re.findall(r'<div[^>]+class="[^"]*elementor-widget-(?:video|video-playlist)[^"]*"[^>]*data-settings="([^"]*)"', webpage):
            data_settings = unescapeHTML(clean_html(element))
            data = self._parse_json(data_settings, None, fatal=False)
            
            tabs = data.get('tabs', [])
            if tabs:  # Handling playlists
                for tab in tabs:
                    video_url = tab.get('youtube_url') or tab.get('vimeo_url') or tab.get('dailymotion_url') or tab.get('videopress_url')
                    if video_url:
                        title = tab.get('title') or self._og_search_title(webpage)
                        thumbnail = tab.get('thumbnail', {}).get('url') or self._og_search_thumbnail(webpage)
                        id=data.get('id') or video_url
                        ie_key = self._get_ie_key(video_url)
                        print(id)
                        print(title)
                        print(video_url)
                        print(thumbnail)
                        print(ie_key)
                        yield self._build_result(video_url, title, thumbnail, ie_key)
            else:
                video_url = data.get('youtube_url') or data.get('vimeo_url') or data.get('dailymotion_url') or data.get('videopress_url')
                title = data.get('title') or self._og_search_title(webpage)
                thumbnail = traverse_obj(data, ('image_overlay', 'url')) or self._og_search_thumbnail(webpage)
                id=data.get('id') or video_url
                ie_key=self._get_ie_key(video_url)
                yield self._build_result(video_url, title, thumbnail, ie_key)
    def _get_ie_key(self, url):
        if 'youtube' in url or 'youtu.be' in url:
            return 'Youtube'
        elif 'vimeo' in url:
            return 'Vimeo'
        elif 'dailymotion' in url:
            return 'Dailymotion'
        elif 'videopress' in url:
            return 'Videopress'
        return 'Generic'
    def _build_result(self, video_url, title, thumbnail, ie_key):
        return {
            'id': video_url,
            'title': title,
            '_type': 'url_transparent',
            'url': video_url,
            'thumbnail': thumbnail,
            'ie_key': ie_key,
        }


