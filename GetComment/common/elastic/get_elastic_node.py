from elasticsearch import Elasticsearch
import yaml
import requests

class Elanode():

    @classmethod
    def getElaInstance(cls):
        try:

            f=open("../conf/elastic_connect_info.yml", "r", encoding="utf-8")
        except FileNotFoundError as E:
            print(E)
            exit(1)
        else:

            ela = yaml.safe_load(f)
            server = ela.get("elahost")[0]

            try:

                html = requests.get("http://"+ server)
            except requests.exceptions.ConnectionError as E:
                print(E)
                exit(1)
            else:

                if html.status_code == 200:
                    elaInstance = Elasticsearch(hosts=ela.get("elahost"))
                    h = elaInstance.cluster.health()

                    if h["status"] == "yellow" or h["status"] == "green":
                        print("elastic instance good !!!")
                        return elaInstance
                    else:
                        exit(1)
                else:
                    exit(1)