import requests
from pprint import pprint

# В целях безопасности ТОКЕН и ID не указал
TOKEN = 'МОЙ ТОКЕН'
id = 'МОЙ ID'

info = requests.get(f'https://api.vk.com/method/users.get?user_id={id}&extended=1&access_token={TOKEN}&v=5.131')
groups = requests.get(f'https://api.vk.com/method/users.getSubscriptions?user_id={id}&extended=1&access_token={TOKEN}&v=5.131')

pprint(info.json())
groups_json = groups.json()

for i in groups_json.get('response').get('items'):
    print(i.get('name'))