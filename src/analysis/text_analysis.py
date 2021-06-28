#%% Libraries
from pathlib import Path

from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np

class TExtAnalysis():
    def __init__(self, text_path):
        pass 

#%%
if __name__ == '__main__':
    data_dir = Path('/workspaces/2021-06-21/data')
    image_path = data_dir/'raw'/'totoro_image.jpg'
    text_path = data_dir/'proc'/'textonly_totoro_subs_en.srt'
    save_path = image_path.parents[1]/'proc'/'totoro_wordcloud.png'

    with open(text_path, 'r') as f:
        text = ' '.join([line.replace('\n', '') for line in f])
    
    background_image = np.array(Image.open(image_path))


    word_cloud = WordCloud(background_color = 'white',
                           mask = background_image,
                           width = 3840, height = 2160).generate(text)

    # font color matching the masked image
    img_colors = ImageColorGenerator(background_image)
    word_cloud.recolor(color_func = img_colors)


    #saving the image
    word_cloud.to_file(save_path)
# %%
