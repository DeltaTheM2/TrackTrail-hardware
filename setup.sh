#!/bin/bash

# Define paths
PROJECT_DIR="/home/jerry/TrackTrail-hardware"
SERVICE_DIR="/etc/systemd/system"

# Copy service files to systemd directory
cp "$PROJECT_DIR/helmet.service" "$SERVICE_DIR/"
cp "$PROJECT_DIR/gps.service" "$SERVICE_DIR/"
cp "$PROJECT_DIR/main.service" "$SERVICE_DIR/"

# Reload systemd to recognize new service files
systemctl daemon-reload

# Enable services to start on boot
systemctl enable helmet.service
systemctl enable gps.service
systemctl enable main.service

# Start services immediately
systemctl start helmet.service
systemctl start gps.service
systemctl start main.service

# Optional: Check status of services
echo "Checking service status..."
systemctl status helmet.service
systemctl status gps.service
systemctl status main.service
