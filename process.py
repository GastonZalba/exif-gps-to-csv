import glob
import os
import exifread as ef
import csv
import sys
from pathlib import Path

csvFileName = 'GPSExif.csv'

def appendCsvLine(list):
    with open(csvFile, 'a', newline='') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(list)
        print(list)
    
    
def getGPS(filepath):
    '''
    returns gps data if present other wise returns empty dictionary
    '''
    with open(filepath, 'rb') as f:
        tags = ef.process_file(f)
        altitude = tags.get('GPS GPSAltitude')
        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')
        
        if altitude:
            alt_value = eval(str(altitude))
            # sum or rest custom value
            if sys.argv[2:]:
                alt_value = (alt_value + float(sys.argv[2]))
        else:
            return {}
        
        if latitude:
            lat_value = _convert_to_degress(latitude)
            if latitude_ref.values != 'N':
                lat_value = -lat_value
        else:
            return {}
        
        if longitude:
            lon_value = _convert_to_degress(longitude)
            if longitude_ref.values != 'E':
                lon_value = -lon_value
        else:
            return {}
        return {'latitude': lat_value, 'longitude': lon_value, 'altitude' : alt_value}
    return {}

    
    
# https://gist.github.com/snakeye/fdc372dbf11370fe29eb 
def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)

                
def processFile(filepath, subFolder = ''):
    filename = os.path.basename(filepath)
    gps = getGPS(filepath)
    list = [filename,gps.get('latitude'), gps.get('longitude'), gps.get('altitude'), subFolder ]
    appendCsvLine(list)  


def loopImages():

    infiles = glob.glob( "{}/*.JPG".format(surveyFolder))

    for filepath in infiles:
        processFile(filepath)

    for dirpath, subdirs, files in os.walk(surveyFolder):
      
        infiles = glob.glob( "{}/{}/*.JPG".format(surveyFolder, subdirs))
        for filepath in infiles:
            processFile(filepath, dirpath)

        for dir in subdirs:
            infiles = glob.glob( "{}/{}/*.JPG".format(surveyFolder, dir))

            for filepath in infiles:
                processFile(filepath, dir)
     
                

def prepareCSV():
    global csvFile
    csvFile = '{}\{}'.format(surveyFolder, csvFileName)
    # delete old file
    if os.path.exists(csvFile):
        os.remove(csvFile)
        
   # write headers
    list = ["FileName", "Latitude", "Longitude", "Altitude", "SubFolder"]    
    appendCsvLine(list)
    
    print('>> CSV created')
    
    
## helpers
def getFolder(folderName):
    if not os.path.exists(folderName):
        print('>> Folder {} not found'.format(folderName))
        exit()

    return folderName


def getArgument(num):
    if len(sys.argv) < (num+1):
        print('>> Argument {} not found'.format(num))
        exit()

    return str(sys.argv[num])


print('>> Start')
surveyFolder = getFolder(getArgument(1))
prepareCSV()
loopImages()
print('>> Finish')