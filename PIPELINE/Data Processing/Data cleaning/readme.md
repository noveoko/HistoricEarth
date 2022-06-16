# Data Cleaning

Training a GANS requires very high-quality data. After attempts to train the model using uncleaned input data it became obvious rather soon that more effort had to be put into provding as high-quality (era-specific) input images (maps) as possible.

![a fake aerial with visible text remnants](images/text_from_map_visible_in_fake_aerial.png)

Apply a two-step process to remove all non geographic objects including:

* text
* numbers
* symbols (church, etc.)
* geometric shapes used as notation (triangles)

## Step 1
![image annoted with text/glyphs](images/annotated_image.png)

annotation performed using online service: [http://app.roboflow.com]()

For a given MAP input image identify all non-geographical objects 

## Step 2
![Normal map image vs map image with text removed via inpatining](images/normal_vs_removed_text.png)

example manually created using online inpainting service: [https://cleanup.pictures/](https://cleanup.pictures/)

Apply an in-painting algorithm to replace the identified objects with probable background (that which is occluded)
