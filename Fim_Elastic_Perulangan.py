from elasticsearch import Elasticsearch
import time, yaml

def load_yaml(path):
    with open(path, 'r') as file:
        data = yaml.safe_load(file)
    return data
fileyaml=load_yaml('./fim_config.yaml')
def tele_init():
    from telethon.sync import TelegramClient, events
    # from telethon import GetAuthorizationsRequest
    api_id = fileyaml['api_id']
    api_hash = fileyaml['api_hash']

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()
    return client

elastic_url=fileyaml['elastic_url']
tele_url=fileyaml['telegram_url']
es = Elasticsearch(elastic_url, verify_certs=False)

while True:
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
    resp = es.search(index="*", query=query,size=1000, from_=0)


    client=tele_init()
    for i in resp['hits']['hits']:
        index=i['_index']
        _id=i['_id']
        pesan="Telah terjadi event "+str(i['_source']['event']['action'])+" pada mesin file "+str(i['_source']['file']['path']) + " pada mesin dengan hostname "+ str(i['_source']['agent']['name'])+ "\n\nDalam waktu "+ str(i['_source']['@timestamp']+"\n\nHarap cek mesin tersebut, kemungkinan terjadi indikasi Web Defacement")
        print(pesan)
        client.send_message(tele_url, pesan)
        es.update(index=index, id=_id, body={"doc": {"notif": "sudah"}})
        time.sleep(1)
    
    time.sleep(30)