# Helmet and GPS Tracking Project

This project consists of three Python scripts (`helmet.py`, `gps.py`, and `main.py`) designed to run on a Raspberry Pi. The scripts handle helmet detection using a camera and machine learning model, GPS tracking with movement detection, and continuous sensor data collection, respectively. The system runs automatically on startup using systemd services.

## Prerequisites

### Hardware:
- Raspberry Pi (tested with Raspberry Pi 5)
- Camera module (for `helmet.py`)
- GPS module (connected via UART)
- LSM6DSOX (accelerometer/gyroscope) and LIS3MDL (magnetometer) sensors (connected via I2C)

### Software:
- Raspberry Pi OS 64bit
- Python 3.11
- Access to a Firebase project with Firestore enabled

### Files:
- `serviceAccountKey.json`: Firebase service account key file 
- `helmet_detection_model.h5`: Trained helmet detection model
- `no_helmet.mp3`: Audio file for helmet warning

## Project Structure
```
/home/jerry/Project/
├── helmet.py           # Helmet detection script
├── gps.py              # GPS tracking and trip status script
├── main.py             # Sensor data collection script
├── helmet.service      # Systemd service file for helmet.py
├── gps.service         # Systemd service file for gps.py
├── main.service        # Systemd service file for main.py
├── setup.sh            # Bash script to configure services
├── serviceAccountKey.json  # Firebase credentials (update path in 
├── helmet_detection_model.h5  # ML model (update path in helmet.py)
└── no_helmet.mp3       # Warning sound (update path in helmet.py)
```

## Setup Instructions

### 1. Make the Setup Script Executable
Set execute permissions for `setup.sh`:
```bash
chmod +x /home/jerry/Project/setup.sh
```

### 6. Run the Setup Script
Execute the bash script to copy service files, enable, and start the services:
```bash
cd /home/jerry/Project
./setup.sh
```
This script will:
- Copy `*.service` files to `/etc/systemd/system/`
- Reload systemd
- Enable services to start on boot
- Start services immediately

### 7. Verify Services
Check the status of each service:
```bash
sudo systemctl status helmet.service
sudo systemctl status gps.service
sudo systemctl status main.service
```

## How It Works

### Helmet Detection (`helmet.py`):
- Runs first, captures images, and uses a TensorFlow model to detect a helmet.
- Plays a warning sound if no helmet is detected; exits when a helmet is detected.

### GPS Tracking (`gps.py`):
- Starts after helmet detection, tracks GPS coordinates, and detects movement.
- Sets `is_in_trip` to `true` in Firestore when movement begins, and `false` after 3 minutes of no movement.
- Stores GPS data in unique documents in the `gps_data` collection.

### Sensor Data (`main.py`):
- Runs continuously, collecting accelerometer, gyroscope, magnetometer, and GPS data.
- Stores data in the `sensor_readings` collection in Firestore.

## Troubleshooting

### Service Fails to Start:
- Check logs: `journalctl -u <service-name>.service`
- Verify file paths and permissions.

### Hardware Not Detected:
- Ensure I2C and UART are enabled: `sudo raspi-config`
- Check connections and permissions.

### Python Errors:
- Verify all dependencies are installed.
- Run scripts manually to debug: `python3 /home/jerry/Project/<script>.py`

## Stopping or Modifying Services

- Stop a service:
  ```bash
  sudo systemctl stop <service-name>.service
  ```
- Disable on boot:
  ```bash
  sudo systemctl disable <service-name>.service
  ```
- Restart after changes:
  ```bash
  sudo systemctl restart <service-name>.service
  ```

