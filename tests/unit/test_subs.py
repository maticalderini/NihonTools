from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[2]))

import unittest
import requests

from src.subs import SubFetcher, SubParser
from datetime import timedelta
import srt

class TestSubs(unittest.TestCase):
    def setUp(self):
        self.url = 'https://kitsunekko.net/subtitles/Tonari%20no%20Totoro/Moj.sosed.Totoro.1988.DUAL.BDRip.XviD.AC3.-HQCLUB.ENG.srt'
        self.known_subs = requests.get(self.url, allow_redirects=True).content
        self.fetcher = SubFetcher()
        self.parser = SubParser(start=timedelta(minutes=2, seconds=32),
                                end=timedelta(hours=1,minutes=26, seconds=10))

    def test_fetch(self):
        fetched_subs = self.fetcher.fetch_subs(self.url)
        self.assertEqual(self.known_subs, fetched_subs)

    def test_get_movie_content(self):
        with open(Path(__file__).parent/'fixtures/test_subs.srt') as f:
            subs = srt.parse(f.read())
        parsed_content = self.parser.get_movie_content(subs)
        good_content = ["Dad, do you want a caramel?",
                        "Τhanks. Αren't you tired?"]      
        self.assertListEqual(good_content, parsed_content)     

if __name__ == '__main__':
    unittest.main()