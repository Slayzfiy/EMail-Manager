import requests
import json


class Query:
    def __init__(self):
        self.headers = {"Authorization": "Bearer 25ad9e51-ce4d-4bcb-b15f-b8dbd2779ca0"}
        self.url = "https://api.testmail.app/api/graphql"

    def getEmailBody(self, reciever):
        query = """
            {
              inbox (
                namespace: "ui38k"
                tag: "%s"
                livequery: true
              ) 
              {
                emails {
                    text
                }
              }
            }
        """ % reciever
        request = requests.post(self.url, json={'query': query}, headers=self.headers)
        if request.status_code == 200:
            temp = json.loads(str(request.json()).replace("'", '"'))
            return temp["data"]["inbox"]["emails"][0]["text"]
