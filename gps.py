import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
import serial
import adafruit_gps
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
USER_ID = 'oF0C5dWBXNdZuwg9VF2YmzrmPNy1'

i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
uart = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')

def check_movement():
    accel_x, accel_y, accel_z = accel_gyro.acceleration
    threshold = 1.0
    return abs(accel_x) > threshold or abs(accel_y) > threshold or abs(accel_z) > threshold

def main():
    path = []
    last_movement_time = time.monotonic()
    is_in_trip = False
    
    while True:
        gps.update()
        current = time.monotonic()
        
        if current - last_movement_time >= 1.0:
            if gps.has_fix:
                gps_point = {
                    "latitude": gps.latitude,
                    "longitude": gps.longitude,
                    "speed": gps.speed_knots if gps.speed_knots is not None else 0,
                }
                path.append(gps_point)
                
                # Check movement and update trip status
                if check_movement():
                    if not is_in_trip:
                        db.collection('users').document(USER_ID).set({"is_in_trip": True}, merge=True)
                        is_in_trip = True
                    last_movement_time = current
                elif is_in_trip and (current - last_movement_time >= 180):
                    db.collection('users').document(USER_ID).set({"is_in_trip": False}, merge=True)
                    is_in_trip = False
                    path = []
                
                # Create a new document with a unique ID in gps_data collection
                trip_ref = db.collection('users').document(USER_ID).collection('gps_data').document()
                trip_ref.set({
                    "path": path,
                    "timestamp": firestore.SERVER_TIMESTAMP
                })
                print(f"Data sent with doc ID {trip_ref.id}: {gps_point}")
            else:
                print('Waiting for GPS fix...')
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()