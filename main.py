import time
import board
import busio
import adafruit_gps
import adafruit_lsm6ds
import adafruit_lis3mdl
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

i2c = busio.I2C(board.SCL, board.SDA)
uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)
lsm6ds = adafruit_lsm6ds.LSM6DSOX(i2c)
lis3mdl = adafruit_lis3mdl.LIS3MDL(i2c)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')

def main():
    last_print = time.monotonic()
    
    while True:
        gps.update()
        current = time.monotonic()
        
        if current - last_print >= 1.0:
            last_print = current
            
            gps_data = {}
            if gps.has_fix:
                gps_data = {
                    "latitude": gps.latitude,
                    "longitude": gps.longitude,
                    "fix_quality": gps.fix_quality,
                    "timestamp": firestore.SERVER_TIMESTAMP
                }
            
            accel_x, accel_y, accel_z = lsm6ds.acceleration
            gyro_x, gyro_y, gyro_z = lsm6ds.gyro
            mag_x, mag_y, mag_z = lis3mdl.magnetic
            
            data = {
                "gps": gps_data,
                "accelerometer": {"x": accel_x, "y": accel_y, "z": accel_z},
                "gyroscope": {"x": gyro_x, "y": gyro_y, "z": gyro_z},
                "magnetometer": {"x": mag_x, "y": mag_y, "z": mag_z},
                "timestamp": firestore.SERVER_TIMESTAMP
            }
            
            doc_ref = db.collection('sensor_readings').document()
            doc_ref.set(data)
            print(f"Data sent: {data}")
        else:
            print("waiting for GPS fix...")
            
        time.sleep(0.1)

if __name__ == "__main__":
    main()