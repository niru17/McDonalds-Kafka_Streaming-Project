from datetime import datetime,timedelta
import time
import uuid
import random
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry.avro import AvroSerializer


def delivery_report(err,msg):
    if err is not None:
        print("Error occurred at user record {} : {}".format(msg.key(),err))
        return
    print("User record {} successfully sent to {} [{}] at offset {}".format(msg.key(),msg.topic(),msg.partition(),msg.offset()))
    print("============================================")


kafka_config= {
    'bootstrap.servers':'pkc-l7pr2.ap-south-1.aws.confluent.cloud:9092',
    'sasl.mechanisms':'PLAIN',
    'security.protocol':'SASL_SSL',
    'sasl.username':'S6LYG5UXE35D2AE4',
    'sasl.password':'fP3gWkeCYiHUpjkhzK7RvPHzlWQr4wucRcxUnThY3Q2UB/Ddgqy2qOxIohIAkDSI'
}

schema_registry_client=SchemaRegistryClient({
    'url':'https://psrc-v7vorn.southeastasia.azure.confluent.cloud',
    'basic.auth.user.info':'{}:{}'.format('SE62XLUZJTRFE43H','3hSvinK8YTb5CzcAo+vSuKOXo4cpoKHRCyG9vatU77oYB55/w8lkEapYVvF3Fl5b')
})

key_serializer=StringSerializer('utf-8')

def get_latest_schema(subject):
    schema=schema_registry_client.get_latest_version(subject).schema.schema_str
    return AvroSerializer(schema_registry_client,schema)

orders_producer=SerializingProducer({**kafka_config,
                                     'key.serializer':key_serializer,
                                     'value.serializer':get_latest_schema('mcd_orders-value')})

payments_producer=SerializingProducer({**kafka_config,
                                       'key.serializer':key_serializer,
                                       'value.serializer':get_latest_schema('mcd_payments-value')})

menu_items=[
    "Big Mac", "McChicken", "Quarter Pounder", "French Fries", "McFlurry",
    "Filet-O-Fish", "Chicken McNuggets", "Egg McMuffin", "Hash Browns", "Apple Pie"
]

def generate_orders_and_payments():
    utc_now=int(datetime.utcnow().timestamp()*1000)

    for i in range(100):
        order_id=str(uuid.uuid4())
        customer_id=f"cust_{random.randint(1000,9999)}"
        order_total=round(random.uniform(10,100),2)
        order_time= utc_now-random.randint(0,24*60*60*1000)

        order_items= [
            {"item_name":random.choice(menu_items), "quantity":random.randint(1,5),"price":round(random.uniform(1,10),2)}
            for _ in range(random.randint(1,3))
        ]

        payment_id=str(uuid.uuid4())
        payment_amount=order_total
        payment_method=random.choice(["credit_card", "cash", "mobile_payment"])
        payment_time=order_time+random.randint(0,5*60*1000)

        orders_producer.produce(
            topic='mcd_orders',
            key=order_id,
            value={
                "order_id":order_id,
                "customer_id":customer_id,
                "order_total":order_total,
                "order_items":order_items,
                "order_time":order_time
            },
            on_delivery=delivery_report
        )
        orders_producer.flush()

        payments_producer.produce(
            topic='mcd_payments',
            key=payment_id,
            value={
                "payment_id":payment_id,
                "order_id":order_id,
                "payment_amount":payment_amount,
                "payment_method":payment_method,
                "payment_time":payment_time
            },
            on_delivery=delivery_report
        )
        orders_producer.flush()

        time.sleep(5)

generate_orders_and_payments()
print("Mock data successfully published.")
