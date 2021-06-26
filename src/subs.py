#%% Libraries
import requests

from pathlib import Path

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


#%%
if __name__ == '__main__':
    data_url = 'https://kitsunekko.net/subtitles/Tonari%20no%20Totoro/Moj.sosed.Totoro.1988.DUAL.BDRip.XviD.AC3.-HQCLUB.ENG.srt'
    save_dir = Path(__file__).parents[1]/'data'/'raw'
    filename = 'totoro_subs_en.srt'

    save_path = save_dir/filename

    fetcher = SubFetcher()
    subs = fetcher.fetch_subs(data_url, save_path=save_path)


# %%
