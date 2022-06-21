from tiling import ConstSizeTiles

tiles = ConstSizeTiles(image_size=(500, 500), tile_size=(256, 256), min_overlapping=15, scale=1.0)

print("Number of tiles: %i" % len(tiles))
for extent, out_size in tiles:
    assert out_size[0] == tiles.tile_size[0]
    assert out_size[1] == tiles.tile_size[1]
    x, y, width, height = extent
    data = read_data(x, y, width, height,
                     out_width=out_size[0],
                     out_height=out_size[1])
    print("data.shape: {}".format(data.shape))

# Access a tile:
i = len(tiles) // 2
extent = tiles[i]


source: https://github.com/vfdev-5/ImageTilingUtils