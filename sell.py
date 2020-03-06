#!/usr/bin/env python
import pika
import time


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel1 = connection.channel()

channel1.queue_declare(queue='sell_queue')


def sell(ch, method, props, number):
    number = int(number)
    while number == 0:
        with open('data.txt', 'wr') as f:
            a = f.read()
            b = int(a)
        while b < 0:
            time.sleep(1)
            with open('data.txt', 'wr') as f:
                a = f.read()
                b = int(a)

        if number > -b:
            number = number + b
            with open('data.txt', 'wr') as f:
                f.write('0')
        else:
            with open('data.txt', 'wr') as f:
                f.write(str(b + number))
            number = 0

    print('ok')


channel1.basic_consume(queue='sell_queue', on_message_callback=sell)


print(" [x] Awaiting requests")
channel1.start_consuming()
