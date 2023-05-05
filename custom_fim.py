import hashlib, os, time, custom_library
from datetime import datetime



def tele_init():
    from telethon.sync import TelegramClient, events
    # from telethon import GetAuthorizationsRequest
    api_id = 2490290
    api_hash = 'f5c895f410966b84ec5e5c63a2d2e92e'

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()
    return client


client=tele_init()
# DIR='./target'
fim_config=custom_library.load_yaml('./fim_config.yaml')
dirs=fim_config['dir']
walk=fim_config['walk']
db_folder=fim_config['db_folder']
time_interval=fim_config['time_interval']
telegram_url=fim_config['telegram_url']
hostname=custom_library.hostname
ip_address=custom_library.ip_address


while True:
    now=datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    print(f"Starting at {now}")
    for DIR in dirs:
        sha256_of_target_dir=custom_library.sha256(DIR)
        db_file=f"{sha256_of_target_dir}.txt"
        db_file=os.path.join(db_folder,db_file)

        if not walk:
            files = custom_library.list_file(DIR)
        elif walk:
            files=custom_library.walk(DIR)

        
        if not os.path.exists(db_file):
            with open(db_file, 'a'):
                os.utime(db_file, None)
            initial_scan=True
        else:
            initial_scan=False
        with open(db_file,"r") as fr:
            lines=fr.readlines()
        
        pesan=""
        target={}
        if initial_scan:
            for file in files:          
                with open(file,"rb") as f:
                    data=f.read(4096)
                    md5=hashlib.md5()
                    while len(data)>0:
                        md5.update(data)
                        data=f.read(4096)
                hasil=md5.hexdigest()
                target[file]=hasil
            
        elif not initial_scan:
            for line in lines:
                sub_line=line.replace("\n","").split("==")
                
                if sub_line[0] not in files:
                    ### Disini ada yang kehapus
                    pesan=f"Terdeteksi event: \nhost {hostname}\nip {ip_address}\n\nTelah terjadi penghapusan file {sub_line[0]}"
                else:
                    target[str(sub_line[0])]=sub_line[1]
                    

            for file in files:          
                with open(file,"rb") as f:
                    data=f.read(4096)
                    md5=hashlib.md5()
                    while len(data)>0:
                        md5.update(data)
                        data=f.read(4096)
                hasil=md5.hexdigest()
                if file in target:
                    if target[file]!=hasil:
                        target[file]=hasil
                        ### Disini ada File Diubah
                        pesan=f"Terdeteksi event: \nhost {hostname}\nip {ip_address}\n\nTelah terjadi Perubahan file {file}"
                    else:
                        pass
                elif (file not in target):
                    ### Disini ada File Baru
                    pesan=f"Terdeteksi event: \nhost {hostname}\nip {ip_address}\n\nTelah terjadi Pembuatan file {file}"
                    target[file]=hasil
            if pesan!="":
                client.send_message(telegram_url, pesan)
        with open(db_file,"w") as fs:
            for line in target:
                fs.write(f"{line}=={target[line]}\n")

            
    time.sleep(time_interval)