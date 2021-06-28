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
        """ Cleans up the line string (content)

        Args:
            line (str): a subtitle line (most often an srt.content)
        """
        mapping = {'\n': ' ', '\u3000': ' ', '♪♪～':''}
        
        for original, replacement in mapping.items():
            line = line.replace(original, replacement)    
        return(line)

    def get_text(self, subs):
        subs_text = [self.clean_line(line) for line in self.get_movie_content(subs)]
        subs_text = [line for line in subs_text if line != '']
        return(subs_text)

    def save_text(self, lines, save_path):
        with open(save_path, 'w+') as f:
            f.writelines('\n'.join(lines))

#%%
if __name__ == '__main__':
    url = 'https://kitsunekko.net/subtitles/japanese/Tonari%20no%20Totoro/tonari%20no%20totoro%20[bd%20x264%20720p%20aac%20sub(chs,cht,jap,eng,ger,fre,ita,kor)][kamigami].ja.srt'
    save_dir = Path(__file__).parents[1]/'data'/'raw'/'subs'
    filename = 'totoro_subs_jp.srt'
    
    start = timedelta(minutes=2, seconds=32)
    end = timedelta(hours=1, minutes=23, seconds=24)

    save_path = save_dir/filename

#%%
    fetcher = SubFetcher()
    fetcher.fetch_subs(url, save_path=save_path)

#%%
    parser = SubParser(start=start, end=end)
    
    subs = parser.load_subs(save_path)
    subs = list(subs)
    all_text = parser.get_text(subs)

    parser.save_text(lines=all_text,
                      save_path=save_dir.parent/'proc'/('textonly_' + filename.removesuffix('.srt') + '.txt'))

# %%
