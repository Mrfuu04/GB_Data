import requests
from pprint import pprint
from json import dump


response = requests.get('https://api.github.com/users/Mrfuu04/repos?type=owner')
response_json = response.json()

for i in response_json:
    print(i.get('name'), i.get('svn_url'), i.get('language'))


with open('task_1_result.json', 'w', encoding='utf-8') as f:
    dump(response_json, f)
