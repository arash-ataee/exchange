#!/usr/bin/env python
import pika
import asyncio


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)


channel1 = connection.channel()

channel1.queue_declare(queue='sell_queue')


for_sell = {}


def buy(stock, number):
    if stock not in for_sell:
        for_sell[stock] = number
    else:
        for_sell[stock] = for_sell[stock] + number
    print(for_sell)


def check_state(stock, number):
    if stock not in for_sell:
        return False
    elif for_sell[stock] < number:
        return False
    else:
        return True


def sell(stock, number):
    if stock not in for_sell:
        for_sell[stock] = -number
    else:
        for_sell[stock] = for_sell[stock] - number
    print(for_sell)


def select(ch, method, props, body):
    a = body.split()
    sell_buy = a[0].decode()
    stock = a[1].decode()
    number = int(a[2])
    if sell_buy == 'sell':
        sell(stock, number)
    elif sell_buy == 'buy':
        print('ok')
        buy(stock, number)


channel1.basic_consume(queue='sell_queue', on_message_callback=select, auto_ack=True)


print(" [x] Awaiting requests")
channel1.start_consuming()
