## exif-gps-to-csv

Extracts from JPG images the Exif GPS information (latitude, longitude and altitude), and dumps it into a CVS file.

# Requeriments
- [ExifRead](https://pypi.org/project/ExifRead/)

# Instructions
`python process.py ./pathToFolder`. It will search for images recursively within the specified folder.

### Csv structure:

FileName | Latitude | Longitude | Altitude | SubFolder
