# Lidar

## Convert LAZ to LAS

[info](https://laszip.org/)

[download](http://www.cs.unc.edu/~isenburg/laszip/download/)

### Compress LAS to LAZ
laszip -i lidar.las -o lidar.laz

### Uncompress LAZ to LAS
laszip -i lidar.laz -o lidar_copy.las

### Convert LAS to PLY
laszip -i lidar.las -o lidar.ply

Free Viewer
http://www.visualizationsoftware.com/3dem/


Blender Point Cloud Add-On
https://www.youtube.com/watch?v=eXct_7k779Q

## Cloud Compare (Free)

I use it to convert LAS to PLY files
https://www.danielgm.net/cc/

### Convert LAS to PLY using Cloud Compare
cloudcompare -O <path_to_file> -C_EXPORT_FMT PLY

# Geoportal.pl

## Scale
According to a screenshot scale of Lidar is 1:2500
