from glob import glob
import os
from PIL import Image
from pathlib import Path

HEIGHT = 250
WIDTH = 250

files_a = glob('example_images/65941.tif', recursive=True)
#files_b = glob('128x128/trainB/*.*', recursive=True)

assert all([os.path.isfile(f) for f in files_a])
#assert all([os.path.isfile(f) for f in files_b])

for list in [files_a]:#, files_b]:
    for file in list:
        try:
            print(f"Processing {file}")
            pth = Path(file)
            root = pth.parent
            if not os.path.exists(root/f'{WIDTH}x{HEIGHT}'):
                os.mkdir(root / f'{WIDTH}x{HEIGHT}')
            stem = pth.stem
            img = Image.open(file).convert('L')
            destination = root / f"{WIDTH}x{HEIGHT}" / (stem + '.png')
            img.resize((HEIGHT, WIDTH), Image.BICUBIC).save(destination)
        except Exception as e:
            print(e)
