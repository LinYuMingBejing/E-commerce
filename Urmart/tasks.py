from django.db.models import Count, Sum
from datetime import datetime
import os
import pandas as pd

from api.models import Order, Product, Shop
from Urmart.celery import app

from django.core.mail import (
    EmailMultiAlternatives,
    send_mail
)
from django.conf import settings
from django.template.loader import get_template


def send_report():
    subject = f'Sale Report {datetime.now().strftime('%Y%m%d')}'

    template = get_template('mail/order.html')
    data = {
        'WEBSITE_URL': settings.WEBSITE_URL,
        'name': order.first_name,
        'id': order.id
    }
    html_email = template.render(data)

    msg = EmailMultiAlternatives(
        subject,
        settings.EMAIL_HOST_USER,
        to=[order.email]
    )
    msg.attach_alternative(html_email, "text/html")
    res = msg.send()


@app.task(ignore_result=True)
def profit():
    nowaday = datetime.now().strftime('%Y%m%d')
    orders = Order.objects.filter(is_delete=False)\
                        .values('shop_id')\
                        .annotate(qty=Sum('qty'), price=Sum('price'), total=Count('shop_id'))\
                        .all()

    is_exist = os.path.exists(f'./result_{nowaday}.csv')
    with open(filename, 'a', encoding='utf-8', newline='') as f:
        for order in orders:
            order['shop_id'] = Shop.objects.get(id=order['shop_id']).name
            f_csv = csv.writer(f)
            f_csv = csv.DictWriter(f, order.keys())
            if not is_exist:
                f_csv.writeheader()
            f_csv.writerow(order)

