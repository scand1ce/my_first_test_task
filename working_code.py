__autor__ = 'Serhii Tomchuk'

'''
This is not an ideal code, but the task was solved, thanks to it.
'''

import requests
from bs4 import BeautifulSoup as bs
import shutil
from PIL import Image, ImageDraw, ImageFont

name = 'Serhii Tomchuk'
email = 'stomchuk34@gmail.com'
IMAGE_OLD = 'image_.jpeg'

url = 'https://www.proveyourworth.net/level3'

start = '/start'
payload = '/payload'
activate = '/activate'
reaper = '/reaper'

r = requests.get(url + start)
page = r.content

cookie = r.cookies["PHPSESSID"]  # --> value

soup = bs(page, 'html.parser')
login = soup.find('div', class_='sqllogin').find('input')

token = login.get('value')  # --> hash

r = requests.get(url + activate, params={'statefulhash': token, "username": name},
                 cookies={"PHPSESSID": cookie})

print('Status code --> {}'.format(r.status_code))  # test message
r = requests.get(url + payload, stream=True, cookies={"PHPSESSID": cookie})
cookie = r.cookies["PHPSESSID"]

image_from_payload = IMAGE_OLD

if r.status_code == 200:
    r.raw.decode_content = True
    with open(image_from_payload, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    print('Downloaded: ', image_from_payload)  # test message

    font = ImageFont.truetype("arial.ttf", 24)
    text_position = (0, 0)
    text_color = (255, 0, 0)  # red RGB
    text = name
    IMAGE_NEW = Image.open(IMAGE_OLD)
    draw = ImageDraw.Draw(IMAGE_NEW)
    draw.text(text_position, text, text_color, font)
    IMAGE_NEW.save('image.jpeg')
    print('Image signed and ready to send')  # test message

else:
    print('payload not download --> {}'.format(r.status_code))

with open('letter.txt', 'r') as f:
    txt_from_letter = f.read()
    print(txt_from_letter)  # test print

box_files = {
    'image': ('image.jpeg', open('image.jpeg', 'rb'), 'image/jpeg'),
    'resume': ('resume.pdf', open('resume.pdf', 'rb'), 'application/pdf'),
    'code': ('code_.py', open('code_.py', 'rb'), 'text/plain'),
}  # MIME types + binary read for files

data = {
    'email': email,
    'name': name,
    'aboutme': txt_from_letter,
}  # data for send

request = requests.Request('POST', url + reaper,
                           files=box_files, data=data, cookies={"PHPSESSID": cookie})
preparation = request.prepare()

session = requests.Session()
response = session.send(preparation)
print(response.status_code)
print(response.text)
