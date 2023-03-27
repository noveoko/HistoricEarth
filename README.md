# Explore the World of 1939 with HistoricEarth

Step into the past and take a virtual flight over any part of the world as it appeared in 1939. Discover the charm of historic towns, find family homes, or stroll through your ancestors' gardens. HistoricEarth aims to breathe new life into old maps by rendering them as aerial photos, providing a unique Google Earth-like experience.

## Discovering the Past

Inspired by a vast collection of aerial photographs from the 1930s covering Poland, held by the British government, HistoricEarth seeks to make these valuable historical resources accessible to everyone. Unfortunately, the current licensing restrictions and fees ($20+ per image) put these amazing images out of reach for most. This project is our attempt to break down barriers and make historical aerial photos available to amateurs and professionals alike.

*Note: No images from the British WW2 Aerial photo archives were used to train this model.*

## Captivating Epoch Samples

### Epoch 66 + 11 (128x128)
![](images/epoch_66_11.png.png)

### Epoch 122 (128x128)
![](images/epoch_122_ready.png)

### Epoch 116 (128x128)
![](images/epoch_116_ready.png)

### Epoch 72 (128x128)
![](images/epoch_72_ready.png)

### Epoch 27
![](images/Early_Example_27.png)

### Epoch 22
![](images/Early_Example_22.png)

## Powering the Transformation

We utilized the [Contrastive Unpaired Translation](https://github.com/taesungp/contrastive-unpaired-translation) library for training our model.

## Training Progress

To enhance reliability and avoid issues encountered with Google Colab (free), we opted for the $8/month Paperspace Gradient Pro plan for our training environment. So far, we've successfully completed 86 epochs, with a goal to reach at least 200 epochs and evaluate the results.

Total training time thus far: approximately 10 hours

## A Vision for the Future

1. Expand our collection of early 20th-century maps to cover the entire globe, creating a simulation of Earth as it would have appeared from an airplane in 1939.
2. Develop an aerial photo search engine and geolocation tool to easily explore the past.

### Useful Resources Discovered During the Project

- [Using Colab features outside of Colab](https://github.com/TakahiroDoi/opencv-workaround-for-colab/blob/main/Example_Cv2Workaround.ipynb)
- [Comprehensive list of remote sensing tools](https://github.com/robmarkcole/satellite-image-deep-learning#image-chippingtiling--merging)
- [Related projects for inspiration](https://www.thoughtco.com/historical-map-overlays-for-google-1422162)
- [Free elevation maps](https://maps-for-free.com/)
- [Extensive guide to Polish map notations](http://maps.mapywig.org/m/m_documents/PL/WZORY_I_OBJASNIENIA_ZNAKOW_TOPOGRAFICZNYCH_10K_25K_WIG_1931.pdf)
- [David Rumsey Map Collection: remote sensing resources, photos, maps, etc.](https://www.davidrumsey.com/)
- [Map scraper tool for David Rumsey's collection](https://github.com/Rburdett4/David-Rumsey-DPLA-Map-Scraper)
