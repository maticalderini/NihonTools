#%% Libraries
from pathlib import Path

import requests

import srt
from datetime import timedelta

#%% Fetcher definitions
class SubFetcher():
    def __init__(self):
        pass
    
    def fetch_subs(self, url, save_path=None, overwrite=False):
        r = requests.get(url, allow_redirects=True)
        subs = r.content
        if save_path is not None:
            save_path = Path(save_path)
            if save_path.exists() and not overwrite:
                print('Save path exists, change overwrite option to True to overwrite files')
            else:
                open(save_path, 'wb').write(r.content)
        return(subs)

class SubParser():
    def __init__(self, start=timedelta(seconds=0),
                 end=timedelta(seconds=0)):
        self.start = start
        self.end = end

    def load_subs(self, filepath):
        with open(filepath, 'r') as f:
            subs = f.read()
        subs = srt.parse(subs)
        return(subs)
    
    def get_movie_content(self, subs):
        '''
        Takes iterable of srt sub objects and keeps those
        within the movie start and end time
        '''
        content = [line.content for line in subs if (line.start > self.start) and (line.end < self.end)]   
        return(content)
    
    def clean_line(self, line):
        line = line.replace('\n', ' ')
        return(line)

    def get_text(self, subs):
        subs_text = [self.clean_line(line) for line in self.get_movie_content(subs)]
        return(subs_text)

    def save_text(self, lines, save_path):
        with open(save_path, 'w+') as f:
            f.writelines('\n'.join(lines))
        
#%%
if __name__ == '__main__':
    # data_url = 'https://kitsunekko.net/subtitles/Tonari%20no%20Totoro/Moj.sosed.Totoro.1988.DUAL.BDRip.XviD.AC3.-HQCLUB.ENG.srt'
    save_dir = Path(__file__).parents[1]/'data'/'raw'
    filename = 'totoro_subs_en.srt'

    save_path = save_dir/filename

    start = timedelta(minutes=2, seconds=32)
    end = timedelta(hours=1, minutes=23, seconds=24)
    parser = SubParser(start=start, end=end)
    subs = parser.load_subs(save_path)
    # subs = list(subs)
    # test_line = list(subs)[0]
    all_text = parser.get_text(subs)

    parser.save_text(lines=all_text,
                      save_path=save_dir.parent/'proc'/('textonly_' + filename.removesuffix('.srt') + '.txt'))
# %%
