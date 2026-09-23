
import json
import time
import random
from kafka import KafkaProducer
from datetime import datetime, timezone

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

campaigns = ['camp_A_summer_sale', 'camp_B_new_user', 'camp_C_retargeting']
events = ['impression', 'impression', 'impression', 'click']

def generate_ad_event():
    return {
        "event_id": f"evt_{random.randint(10000, 99999)}",
        "campaign_id": random.choice(campaigns),
        "event_type": random.choice(events),
        "user_device": random.choice(['ios', 'android', 'web']),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def generate_kafka_event():
    while True:
        event = generate_ad_event()
        producer.send('ad_events_topic', value=event)
        print(f"Sent: {event}")
        time.sleep(0.1)
