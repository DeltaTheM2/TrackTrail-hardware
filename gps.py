import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
import serial
import adafruit_gps
import firebase_admin
from firebase_admin import credentials, firestore

# Firestore setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# I2C for LSM6DSOX + LIS3MDL sensors
i2c = board.I2C()  # Uses board.SCL and board.SDA

# Initialize LSM6DSOX (accelerometer + gyroscope) and LIS3MDL (magnetometer)
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)

# Initialize GPS using pyserial
uart = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)

# Turn on the basic GGA and RMC info (for GPS)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')  # Set GPS update rate to once a second (1000ms)

# Path list to store GPS points
path = []

last_print = time.monotonic()

while True:
    gps.update()

    # Check GPS data every second
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current

        if gps.has_fix:
            # Extract GPS data
            gps_point = {
                "latitude": gps.latitude,
                "longitude": gps.longitude,
                "speed": gps.speed_knots if gps.speed_knots is not None else 0,  # Speed in knots
            }

            # Add the GPS point to the path
            path.append(gps_point)

            # Print GPS data to the console
            print(f"Latitude: {gps.latitude}, Longitude: {gps.longitude}, Speed: {gps.speed_knots} knots")

            # Send path data to Firestore
            trip_ref = db.collection('users').document('oF0C5dWBXNdZuwg9VF2YmzrmPNy1').collection('gps_data').document('trip_test')
            trip_ref.set({
                "path": path,  # Store path as an array of GPS points
                "timestamp": firestore.SERVER_TIMESTAMP  # Top-level timestamp
            }, merge=True)

            print(f"Data sent to Firestore: {gps_point}\n")
        
        else:
            print('Waiting for GPS fix...')

    time.sleep(0.5)
