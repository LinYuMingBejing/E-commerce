from django.db.models import Count, Sum
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings

from datetime import datetime, timedelta
import csv
import os

from api.models import Order, Shop
from Urmart.celery import app

CSV_HEADER = ['shop_id', 'qty', 'price', 'total']
ATTACHMENT_NAME = f'{(datetime.now() - timedelta(days=1)).strftime("%Y%m%d")}銷售報告.csv'


def send():
    subject = ATTACHMENT_NAME
    message = '請查收，謝謝。如有任何問題，歡迎聯繫！'
    
    sender = settings.EMAIL_FROM
    receiver = [settings.EMAIL_TO]

    email = EmailMultiAlternatives(subject, message, sender, receiver)
    email.attach(ATTACHMENT_NAME, ATTACHMENT_NAME, 'text/csv')
    email.send()


@app.task(ignore_result=True)
def report():
    orders = Order.objects.filter(is_delete=False)\
                        .values('shop_id')\
                        .annotate(qty=Sum('qty'), price=Sum('price'), total=Count('shop_id'))\
                        .all()
        
    with open(ATTACHMENT_NAME, 'a', encoding='utf-8', newline='') as f:
        f_csv = csv.writer(f)
        f_csv = csv.DictWriter(f, CSV_HEADER)
        f_csv.writeheader()
        
        for order in orders:
            order['shop_id'] = Shop.objects.get(id=order['shop_id']).name
            f_csv.writerow(order)
    send()

