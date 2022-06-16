# Data Cleaning

Apply a two-step process to remove all non geographic objects including:

* text
* numbers
* symbols (church, etc.)
* geometric shapes used as notation (triangles)

## Step 1

1. For a given MAP input image identify all non-geographical objects
2. Apply an in-painting algorithm to replace the identified objects with probable background (that which is occluded)