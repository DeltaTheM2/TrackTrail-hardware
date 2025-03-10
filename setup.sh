#!/bin/bash

# Define paths
PROJECT_DIR="/home/jerry/TrackTrail-hardware"
SERVICE_DIR="/etc/systemd/system"

# Copy service files to systemd directory
sudo cp "$PROJECT_DIR/helmet.service" "$SERVICE_DIR/"
sudo cp "$PROJECT_DIR/gps.service" "$SERVICE_DIR/"
sudo cp "$PROJECT_DIR/main.service" "$SERVICE_DIR/"

# Reload systemd to recognize new service files
sudo systemctl daemon-reload

# Enable services to start on boot
sudo systemctl enable helmet.service
sudo systemctl enable gps.service
sudo systemctl enable main.service

# Start services immediately
sudo systemctl start helmet.service
sudo systemctl start gps.service
sudo systemctl start main.service

# Optional: Check status of services
echo "Checking service status..."
sudo systemctl status helmet.service
sudo systemctl status gps.service
sudo systemctl status main.service
