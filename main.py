import time
import board
import busio
import adafruit_gps
import adafruit_lsm6ds
import adafruit_lis3mdl
import firebase_admin
from firebase_admin import credentials, firestore

# Firestore setup
cred = credentials.Certificate("/path/to/your/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Create I2C bus for the SM6DSOX + LIS3MDL sensor
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the GPS module over UART
uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)

# Initialize the SM6DSOX (accelerometer + gyroscope) and LIS3MDL (magnetometer)
lsm6ds = adafruit_lsm6ds.LSM6DSOX(i2c)
lis3mdl = adafruit_lis3mdl.LIS3MDL(i2c)

# Turn on the basic GGA and RMC info (for GPS)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')  # Set GPS update rate to once a second (1000ms)

last_print = time.monotonic()

while True:
    gps.update()

    # Check GPS data every second
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        
        # GPS Data
        gps_data = {}
        if gps.has_fix:
            gps_data = {
                "latitude": gps.latitude,
                "longitude": gps.longitude,
                "fix_quality": gps.fix_quality,
                "timestamp": firestore.SERVER_TIMESTAMP
            }
        else:
            print('Waiting for GPS fix...')
        
        # SM6DSOX Sensor Data (accelerometer + gyroscope)
        accel_x, accel_y, accel_z = lsm6ds.acceleration
        gyro_x, gyro_y, gyro_z = lsm6ds.gyro
        accel_data = {
            "acceleration": {
                "x": accel_x,
                "y": accel_y,
                "z": accel_z
            },
            "gyroscope": {
                "x": gyro_x,
                "y": gyro_y,
                "z": gyro_z
            }
        }
        
        # LIS3MDL Magnetometer Data
        mag_x, mag_y, mag_z = lis3mdl.magnetic
        mag_data = {
            "magnetometer": {
                "x": mag_x,
                "y": mag_y,
                "z": mag_z
            }
        }
        
        # Combine all sensor data
        data = {
            "gps": gps_data,
            "accelerometer": accel_data["acceleration"],
            "gyroscope": accel_data["gyroscope"],
            "magnetometer": mag_data["magnetometer"],
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        
        # Send data to Firestore
        doc_ref = db.collection('sensor_readings').document()
        doc_ref.set(data)
        
        print(f"Data sent to Firestore: {data}")

    time.sleep(0.1)
