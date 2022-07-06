import requests
import smtplib
import time
from bs4 import BeautifulSoup
from keep_alive import keep_alive

url = 'https://www.hepsiburada.com/apple-macbook-air-m1-cip-8gb-256gb-ssd-macos-13-qhd-tasinabilir-bilgisayar-gumus-mgn93tu-a-p-HBV0000130VNJ?magaza=Hepsiburada&wt_gl=cpc.6802.shop.elk.it-ssc&isFashion=true&gclid=CjwKCAjwtdeFBhBAEiwAKOIy57jgnYrSbgVDOpq0afjNiB45KAH_7VZF7YxEV-S6d4iEPXvEyUZ2cxoC8qEQAvD_BwE'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}


def check_price():
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id='product-name').text.strip()
    title = title[0:20]
    span = soup.find(id='offering-price')
    price = span.attrs.get('content')
    price = float(price)
    print(price)
    # print(title)
    if (price < 18000):
        send_mail(title)



def send_mail(title):
    sender = 'alpersln23@gmail.com'
    receiver = 'alpersln23@gmail.com'
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender, 'kceabkuuxsltbbbr')
        subject = title + 'istedigin  fiyata dustu!!!'
        body = 'Bu linkten  gidebilirsin =>' + url
        mailContent = f'To:{receiver}\nFrom:{sender}\nSubject:{subject}\n\n{body}'
        server.sendmail(sender, receiver, mailContent)
        print('Mail sent')
    except smtplib.SMTPException as e:
        print(e)
    finally:
        server.quit()


while (1):
    check_price()
    time.sleep(60 * 60)

keep_alive()