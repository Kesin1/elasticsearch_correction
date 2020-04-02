import pandas as pd
from elasticsearch6 import Elasticsearch
from elasticsearch6.helpers import bulk
import copy

kb = pd.read_excel("fichier_import_MACIF.xlsx")

json_model = {
    "questionId": None,
    "title": None,
    "titleReword": None,
    "responses": [
        {
            "body": None
        }
    ]
}

requests = []
for row in kb.iterrows():
    request = json_model
    request["questionId"] = row[0]
    request["title"] = row[1][0]
    request["responses"][0]["body"] = row[1][1]
    request["_index"] = "macif"
    request["_type"] = "question"
    request["_op_type"] = "create"
    request["_id"] = row[0]
    requests.append(copy.deepcopy(request))

# import json
# def filewriter(request):
#     with open('kb_bulk.json', 'a+') as f:
#         if len(f.read()) == 0:
#             f.write(json.dumps(request, ensure_ascii=False))
#         else:
#             f.write(',\n' + json.dumps(request))

# for request in requests:
#     filewriter(request)
    
client = Elasticsearch()

# Delete Index
client.indices.delete(index="macif", ignore=[404])

# Create Index
with open("index.json") as index_file:
    source = index_file.read().strip()
    client.indices.create(index="macif", body=source)


# bulk index
bulk(client, requests)
