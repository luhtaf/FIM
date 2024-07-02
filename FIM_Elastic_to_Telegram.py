from datetime import datetime
from elasticsearch import Elasticsearch
import time

def tele_init():
    from telethon.sync import TelegramClient, events
    from telethon import GetAuthorizationsRequest
    api_id = '# your api id'
    api_hash = '# your api hash'

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()
    return client

username="admin"
passw="admin123"
es = Elasticsearch("https://10.12.10.159:9200", basic_auth=(username, passw), verify_certs=False)


query={
        "bool": {
            "must": [
                {
                    "match": {
                        "event.module": "file_integrity"
                    }
                }
            ],
            "must_not": [
                {
                    "match": {
                        "event.action": "initial_scan"
                    }
                },
               {
                    "match": {
                        "notif": "sudah"
                    }
                }
                
            ]

        }
    }
resp = es.search(index="auditbeat*", query=query,size=1000, from_=0)


client=tele_init()
for i in resp['hits']['hits']:
    index=i['_index']
    _id=i['_id']
    pesan="Telah terjadi event "+str(i['_source']['event']['action'])+" pada mesin file "+str(i['_source']['file']['path']) + " pada mesin dengan hostname "+ str(i['_source']['agent']['name'])+ "\n\nDalam waktu "+ str(i['_source']['@timestamp']+"\n\nHarap cek mesin tersebut, kemungkinan terjadi indikasi Web Defacement")
    print(pesan)
    client.send_message('https://t.me/joinchat/3t06ll3bnKJjNjg1', pesan)
    es.update(index=index, id=_id, body={"doc": {"notif": "sudah"}})
    time.sleep(1)
    
    # break
print("tilan")