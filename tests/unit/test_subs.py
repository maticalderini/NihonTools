#%%
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[2]))

import unittest
import requests

from src.subs import SubFetcher

#%%
class TestFetcher(unittest.TestCase):
    def setUp(self):
        self.url = 'https://kitsunekko.net/subtitles/Tonari%20no%20Totoro/Moj.sosed.Totoro.1988.DUAL.BDRip.XviD.AC3.-HQCLUB.ENG.srt'
        self.known_subs = requests.get(self.url, allow_redirects=True).content
        self.fetcher = SubFetcher()

    def test_fetch(self):
        fetched_subs = self.fetcher.fetch_subs(self.url)
        self.assertEqual(self.known_subs, fetched_subs)

if __name__ == '__main__':
    unittest.main()



# #%%
# url = 'https://kitsunekko.net/subtitles/Tonari%20no%20Totoro/Moj.sosed.Totoro.1988.DUAL.BDRip.XviD.AC3.-HQCLUB.ENG.srt'
# subs = requests.get(url, allow_redirects=True)
# # fetcher = SubFetcher