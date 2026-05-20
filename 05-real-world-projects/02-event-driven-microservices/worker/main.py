import pika
import pymongo
import json
import os
import time

def process_job(ch, method, properties, body):
    try:
        job = json.loads(body)
        print(f"Processing job: {job}")
        
        # Simulate CPU work
        time.sleep(2)
        
        # Connect to MongoDB
        mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/jobs')
        client = pymongo.MongoClient(mongo_url)
        db = client.get_default_database()
        collection = db.processed_jobs
        
        # Save output
        collection.insert_one({
            "job_id": job.get("job_id"),
            "original_data": job.get("data"),
            "processed": True,
            "timestamp": time.time()
        })
        print(f"Job {job.get('job_id')} saved to database.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing job: {e}")

def main():
    rabbitmq_url = os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')
    params = pika.URLParameters(rabbitmq_url)
    
    # Retry connecting until RabbitMQ is fully up
    connection = None
    for i in range(10):
        try:
            connection = pika.BlockingConnection(params)
            break
        except Exception as e:
            print(f"Waiting for RabbitMQ ({i}/10)... {e}")
            time.sleep(3)
            
    if not connection:
        print("Failed to connect to RabbitMQ.")
        return

    channel = connection.channel()
    channel.queue_declare(queue='jobs')
    channel.basic_consume(queue='jobs', on_message_callback=process_job)
    print('🚀 Go Worker (Python Mock) waiting for messages...')
    channel.start_consuming()

if __name__ == '__main__':
    main()
