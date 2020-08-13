## exif-gps-to-csv

Extracts the exif GPS information (latitude, longitude and altitude) from JPG images and dumps it into a CVS file. If a second argument is set, it will be added or subtracted to the altitude value.<br>

It is primarily intended to correct ellipsoidal <> orthometric heights, or fix up constant difference height values.<br>

## Requeriments
- [ExifRead](https://pypi.org/project/ExifRead/)

## Instructions
`python process.py ./pathToFolder float[optional]`

### Csv structure:

FileName | Latitude | Longitude | Altitude | SubFolder
