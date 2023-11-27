import base64
import requests
import json

from requests import Response


def pubsub_to_backend(event):
    print(event['data'])
    message = base64.b64decode(event['data']).decode('utf-8')
    message_data = json.loads(message)
    # Construct PUT request payload
    payload = message_data
    # Make PUT request to backend endpoint
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMDc5ODk5NSwianRpIjoiZWNkNjYwYmQtNDUwMS00ZTNmLTkxZDEtOGExMTcxMGE1NDY4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjU0ZmUyMjUxLWIxYzAtNGE1Yy1iZDc4LTAzMjliOTQzZTFjZSIsIm5iZiI6MTcwMDc5ODk5NSwiZXhwIjoxNzAwNzk5ODk1fQ.RWBxiRZnpp-RjvGgNVlQgIC6ymukzcM1_3fqJA54LE4'}
    # response = requests.put('https://34.171.225.63.nip.io/assignments', json=payload, verify=False, headers=headers)
    # print(response.json())
    # print(response.status_code)
    # return response
    return message_data