import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate("C:\\Users\\smirz\\OneDrive\\Documents\\Coding Minds\\Jerry Ku\\tracktrail-c9b38-firebase-adminsdk-4uq2o-86b3327b37.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Replace with the actual user ID
user_id = 'oF0C5dWBXNdZuwg9VF2YmzrmPNy1'

# Sample trips data
sample_trips = [
   {
  "trip_id": "trip_001",
  "start_time": "2023-10-22T09:00:00Z",
  "end_time": "2023-10-22T09:30:00Z",
  "duration": 30.0,
  "distance": 10.5,
  "path": [
  {
    "latitude": 33.6426,
    "longitude": -117.8419,
    "speed": 0.0,
    "timestamp": "2023-10-22T09:00:00Z"
  },
  {
    "latitude": 33.6445,
    "longitude": -117.8428,
    "speed": 10.0,
    "timestamp": "2023-10-22T09:05:00Z"
  },
  {
    "latitude": 33.6462,
    "longitude": -117.8440,
    "speed": 12.0,
    "timestamp": "2023-10-22T09:10:00Z"
  },
  {
    "latitude": 33.6480,
    "longitude": -117.8455,
    "speed": 15.0,
    "timestamp": "2023-10-22T09:15:00Z"
  },
  {
    "latitude": 33.6495,
    "longitude": -117.8440,
    "speed": 8.0,
    "timestamp": "2023-10-22T09:20:00Z"
  },
  {
    "latitude": 33.6478,
    "longitude": -117.8425,
    "speed": 9.0,
    "timestamp": "2023-10-22T09:25:00Z"
  },
  {
    "latitude": 33.6426,
    "longitude": -117.8419,
    "speed": 0.0,
    "timestamp": "2023-10-22T09:30:00Z"
  }
]
    },
    {
  "trip_id": "trip_002",
  "start_time": "2023-10-21T14:15:00Z",
  "end_time": "2023-10-21T14:45:00Z",
  "duration": 30.0,
  "distance": 12.3,
  "path": [
  {
    "latitude": 33.6846,
    "longitude": -117.8265,
    "speed": 0.0,
    "timestamp": "2023-10-21T14:15:00Z"
  },
  {
    "latitude": 33.6855,
    "longitude": -117.8280,
    "speed": 11.0,
    "timestamp": "2023-10-21T14:20:00Z"
  },
  {
    "latitude": 33.6870,
    "longitude": -117.8295,
    "speed": 13.0,
    "timestamp": "2023-10-21T14:25:00Z"
  },
  {
    "latitude": 33.6890,
    "longitude": -117.8310,
    "speed": 9.0,
    "timestamp": "2023-10-21T14:30:00Z"
  },
  {
    "latitude": 33.6905,
    "longitude": -117.8290,
    "speed": 10.0,
    "timestamp": "2023-10-21T14:35:00Z"
  },
  {
    "latitude": 33.6880,
    "longitude": -117.8270,
    "speed": 12.0,
    "timestamp": "2023-10-21T14:40:00Z"
  },
  {
    "latitude": 33.6846,
    "longitude": -117.8265,
    "speed": 0.0,
    "timestamp": "2023-10-21T14:45:00Z"
  }
]
},
{
  "trip_id": "trip_003",
  "start_time": "2023-10-20T08:00:00Z",
  "end_time": "2023-10-20T08:25:00Z",
  "duration": 25.0,
  "distance": 8.7,
  "path": [
  {
    "latitude": 33.6695,
    "longitude": -117.8231,
    "speed": 0.0,
    "timestamp": "2023-10-20T08:00:00Z"
  },
  {
    "latitude": 33.6705,
    "longitude": -117.8250,
    "speed": 9.0,
    "timestamp": "2023-10-20T08:05:00Z"
  },
  {
    "latitude": 33.6720,
    "longitude": -117.8270,
    "speed": 10.0,
    "timestamp": "2023-10-20T08:10:00Z"
  },
  {
    "latitude": 33.6740,
    "longitude": -117.8285,
    "speed": 8.0,
    "timestamp": "2023-10-20T08:15:00Z"
  },
  {
    "latitude": 33.6760,
    "longitude": -117.8275,
    "speed": 12.0,
    "timestamp": "2023-10-20T08:20:00Z"
  },
  {
    "latitude": 33.6775,
    "longitude": -117.8255,
    "speed": 0.0,
    "timestamp": "2023-10-20T08:25:00Z"
  }
]

}


]

# Function to push trip data to Firestore
def push_trip_to_firestore(trip_data):
    trip_id = trip_data['trip_id']
    # Convert string timestamps to Firestore-compatible timestamps
    trip_data['start_time'] = datetime.datetime.fromisoformat(trip_data['start_time'].replace('Z', '+00:00'))
    trip_data['end_time'] = datetime.datetime.fromisoformat(trip_data['end_time'].replace('Z', '+00:00'))
    for point in trip_data['path']:
        point['timestamp'] = datetime.datetime.fromisoformat(point['timestamp'].replace('Z', '+00:00'))
    # Reference to the trip document
    trip_ref = db.collection('users').document(user_id).collection('gps_data').document(trip_id)
    # Set the trip data in Firestore
    trip_ref.set(trip_data)
    print(f"Trip {trip_id} data pushed to Firestore.")

# Push each sample trip to Firestore
for trip in sample_trips:
    push_trip_to_firestore(trip)
