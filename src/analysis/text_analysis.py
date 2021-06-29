#%% Libraries
from pathlib import Path

import numpy as np
from collections import Counter
import string

from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image


#%% Class definitions
class TextAnalysis():
    def __init__(self, text_path):
        """
        Args:
            text_path (path): path to text file with movie text
        """        
        with open(text_path, 'r') as f:
            self.text = ' '.join([line.replace('\n', '') for line in f])

    def make_wordcloud(self, save_path=None, img_path=None, **kwargs):
        """
        Makes a word cloud from the movie text.
        Optionally, in the shape of a provided image (e.g. a character or iconic scene)
        Args:
            save_path (path, optional): path to save the wordcloud image. Defaults to None.
            img_path (path, optional): path to image for wordcloud shape. Defaults to None.
        """        
        if img_path:
            background_image = np.array(Image.open(img_path))
            kwargs.update({'mask': background_image})
            img_colors = ImageColorGenerator(background_image)

        word_cloud = WordCloud(**kwargs).generate(self.text)

        if img_path:
            word_cloud.recolor(color_func = img_colors)

        if save_path:
            word_cloud.to_file(save_path)
        return(word_cloud)

#%%
if __name__ == '__main__':
    data_dir = Path('/workspaces/NihonTools/data')
    data_proc_dir = data_dir/'proc'
    text_path = data_proc_dir/'subs'/'textonly_totoro_subs_en.txt'
    
    image_path = data_dir/'raw'/'imgs'/'totoro_image.jpg'
    save_path = data_proc_dir/'imgs'/'totoro_wordcloud1.png'
    
    
    text_proc = TextAnalysis(text_path)
    cloud = text_proc.make_wordcloud(save_path=save_path, img_path=image_path)
    

# %%
