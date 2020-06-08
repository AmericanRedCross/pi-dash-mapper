# pi-dash-mapper
## Components
1. Raspberry PI
2. PiCamera
3. USB GPS Device 
4. Battery Pack for Raspberry PI

### Configure the PI
#### 1. Install gpsd
```shell script
sudo apt-get install gpsd
```
#### 2. Configure gpsd
```shell script
sudo nano /etc/default/gpsd
```
Update as follows based on the GPS device connected to the PI
```shell script
# Devices gpsd should collect to at boot time.
# They need to be read/writeable, either by user gpsd or the group dialout.
DEVICES="/dev/gps0"  
# OR DEVICES=/dev/ttyACM0 -- Will work
```
#### 3. Validate gpsd
```shell script
cgps -s
```
Output:
```shell script
┌───────────────────────────────────────────┐┌─────────────────────────────────┐
│    Time:       2020-06-08T05:26:30.000Z   ││PRN:   Elev:  Azim:  SNR:  Used: │
│    Latitude:    xx.xxxxxxxx N             ││  10    67    083    45      Y   │
│    Longitude:   xx.xxxxxxxx W             ││  11    22    293    26      Y   │
│    Altitude:   1296.916 ft                ││  14    57    279    28      Y   │
│    Speed:      0.02 mph                   ││  20    36    118    31      Y   │
│    Heading:    0.0 deg (true)             ││  21    21    176    34      Y   │
│    Climb:      0.00 ft/min                ││  24    14    043    23      Y   │
│    Status:     3D FIX (35 secs)           ││  31    32    196    36      Y   │
│    Longitude Err:   +/- 33 ft             ││  32    69    326    37      Y   │
│    Latitude Err:    +/- 32 ft             ││                                 │
│    Altitude Err:    +/- 106 ft            ││                                 │
│    Course Err:      n/a                   ││                                 │
│    Speed Err:       n/a                   ││                                 │
│    Time offset:     0.083                 ││                                 │
│    Grid Square:     EM26vi                ││                                 │
└───────────────────────────────────────────┘└─────────────────────────────────┘
```

### Configure Python Service

Under Development .......

Readme pending .....

Test ...


