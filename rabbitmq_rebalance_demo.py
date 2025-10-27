import pika
import threading
import time
import random

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "test-queue"
USERNAME = "admin"
PASSWORD = "strongpass"

# ========================
#  Hàm gửi message test
# ========================
def send_messages():
    creds = pika.PlainCredentials(USERNAME, PASSWORD)
    conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=creds))
    ch = conn.channel()
    ch.queue_declare(queue=QUEUE_NAME, durable=True)

    for i in range(1, 11):
        msg = "CRASH" if i == 5 else f"Message-{i}"
        ch.basic_publish(exchange="", routing_key=QUEUE_NAME, body=msg)
        print(f"→ Sent: {msg}")
    conn.close()


# ========================
#  Worker thread (consumer)
# ========================
def worker(name):
    creds = pika.PlainCredentials(USERNAME, PASSWORD)
    conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=creds))
    ch = conn.channel()
    ch.queue_declare(queue=QUEUE_NAME, durable=True)
    ch.basic_qos(prefetch_count=1)

    print(f"✅ {name} started")

    def callback(ch, method, properties, body):
        msg = body.decode()
        print(f"[{name}] Received: {msg}")

        try:
            time.sleep(random.uniform(1, 3))

            if msg == "CRASH":
                print(f"💥 {name} crashing intentionally!")
                # không ack, đóng connection => message sẽ requeue
                conn.close()
                return

            print(f"[{name}] Processed {msg}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"[{name}] Error: {e}")
            # gửi lại message cho queue
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    ch.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)
    try:
        ch.start_consuming()
    except Exception as e:
        print(f"❌ {name} died: {e}")


# ========================
#  Main
# ========================
if __name__ == "__main__":
    send_messages()

    # Tạo 3 thread consumer
    for i in range(1, 4):
        t = threading.Thread(target=worker, args=(f"Worker-{i}",), daemon=True)
        t.start()

    # Giữ chương trình chạy
    while True:
        time.sleep(1)
