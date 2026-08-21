import os
import sys
import requests
from google.transit import gtfs_realtime_pb2 as gtfs_rt
from dotenv import load_dotenv

load_dotenv()

FEED_URLS = {
    "vehicles": "UBIRIDER_INCOFER_VEHICLES_TEST",
    "trips": "UBIRIDER_INCOFER_TRIPS_TEST",
    "alerts": "UBIRIDER_INCOFER_ALERTS_TEST",
}

if len(sys.argv) != 2 or sys.argv[1] not in FEED_URLS:
    print(f"Usage: python {sys.argv[0]} <{'|'.join(FEED_URLS)}>")
    sys.exit(1)

feed_url = os.getenv(FEED_URLS[sys.argv[1]])
token = os.getenv("UBIRIDER_TOKEN_TEST")

feed_response = requests.get(feed_url, headers={"Authorization": f"Bearer {token}"})

if not feed_response.ok:
    print(f"HTTP {feed_response.status_code}: {feed_response.text}")
    sys.exit(1)

feed = gtfs_rt.FeedMessage()
try:
    feed.ParseFromString(feed_response.content)
except Exception:
    print(f"Could not parse response as protobuf. Raw content:\n{feed_response.text}")
    raise

print(feed)
