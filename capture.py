#!/usr/bin/python3

from picamera import PiCamera
from time import *
import datetime
from gps import *
import math
from dateutil import parser
from detect_usb import get_mount_points
from pathlib import Path
from geopy.distance import distance


camera = PiCamera()
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
previous_cordinate = ()
accepted_distance = 1.5 # in meter

def isUSBStorageExist():
    if get_mount_points():
        return get_mount_points()[0][1]
    else:
        return False


def getDistance(prev_cord, cur_cord):
    print(prev_cord, cur_cord)
    if prev_cord:
        # Calculate distance
        return distance(prev_cord, cur_cord).m
        #return 2 # return meter (double)
    else:
        return accepted_distance # Return offset value the we accept as significant distance
        
    


while True:
    report = gpsd.next()
    if report['class'] == 'TPV':
        # 1. Set orientation to normal landscape.
        camera.exif_tags['IFD0.Orientation'] = '1'

        # 2. Set picture date and time to GPS values.
        # TODO Tag the date time based on the raspberry PI (Timezone)
        #now = parser.parse(report.get('time', datetime.isoformat()))
        camera.exif_tags['EXIF.DateTimeOriginal'] = "1"

        # 3. Set altitude to GPS value.
        alt = report.get('alt', 0.0)
        print(alt)
        camera.exif_tags['GPS.GP SAltitudeRef'] = '0' if alt > 0 else '1'
        aalt = math.fabs(alt)
        camera.exif_tags['GPS.GPSAltitude'] = '%d/100' % int(100 * aalt)

        # Convert speed from m/s to km/h and set tag.
        speed = report.get('speed', 0.0)
        print(speed)
        camera.exif_tags['GPS.GPSSpeedRef'] = 'K'
        camera.exif_tags['GPS.GPSSpeed'] = '%d/1000' % int(3600 * speed)

        # Set direction of motion and direction along which the picture is taken (assuming frontal view).
        track = report.get('track', 0.0)
        print(track)
        camera.exif_tags['GPS.GPSTrackRef'] = 'T'
        camera.exif_tags['GPS.GPSTrack'] = '%d/10' % int(10 * track)
        camera.exif_tags['GPS.GPSImgDirectionRef'] = 'T'
        camera.exif_tags['GPS.GPSImgDirection'] = '%d/10' % int(10 * track)

        # Set GPS latitude.
        lat = report.get('lat', 0.0)
        print(lat)
        camera.exif_tags['GPS.GPSLatitudeRef'] = 'N' if lat > 0 else 'S'
        alat = math.fabs(lat)
        dlat = int(alat)
        mlat = int(60 * (alat - dlat))
        slat = int(6000 * (60 * (alat - dlat) - mlat))
        camera.exif_tags['GPS.GPSLatitude'] = '%d/1,%d/1,%d/100' % (dlat, mlat, slat)

        # Set GPS longitude.
        lon = report.get('lon', 0.0)
        print(lon)
        camera.exif_tags['GPS.GPSLongitudeRef'] = 'E' if lon > 0 else 'W'
        alon = math.fabs(lon)
        dlon = int(alon)
        mlon = int(60 * (alon - dlon))
        slon = int(6000 * (60 * (alon - dlon) - mlon))
        camera.exif_tags['GPS.GPSLongitude'] = '%d/1,%d/1,%d/100' % (dlon, mlon, slon)
        directory = "pidash-"+str(datetime.date.today())
        usbStorage = isUSBStorageExist()
        if usbStorage:
            dist = getDistance(previous_cordinate, (lat,lon))
            print("Distance:"+str(dist))
            
            if(dist>=accepted_distance): # Assume returned value is in meter
                Path(usbStorage+'/'+directory).mkdir(parents=True, exist_ok=True)
                camera.capture(usbStorage+'/'+directory+'/image-'+str(int(time.time()))+'.jpeg')
                previous_cordinate = (lat,lon)
                print("Image Created:"+str(int(time.time()))+'.jpeg')
        else:
            print("Please Insert USB Flash Drive")
    sleep(1)
