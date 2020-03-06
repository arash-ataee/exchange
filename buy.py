#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel1 = connection.channel()

channel1.queue_declare(queue='buy_queue')


def buy(number):
    while number == 0:
        with open('data.txt', 'wr') as f:
            b = -number
            f.write(str(b))
        while b < 0:
            time.sleep(1)
            with open('data.txt', 'r') as f:
                a = f.read()
                b = int(a)

    print('ok')


channel1.basic_consume(queue='buy_queue', on_message_callback=buy)


print(" [x] Awaiting requests")
channel1.start_consuming()



