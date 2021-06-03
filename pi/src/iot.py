import requests
import json
import time


class Client:
    def __init__(self, device_id, url='http://185.252.30.176/'):
        self.url = url
        self.device_id = device_id
        self.access_token = None

    def send_request(self, req_type, **kwargs):
        req_url = self.url + req_type
        return requests.post(req_url,
                             json=kwargs,
                             headers={'Content-Type': 'application/json'})

    def hello(self):
        result = self.send_request('hello/', device_id=self.device_id)
        if result.json()['message'] == 'Device is yet to be claimed by a user':
            return -1
        while not result.json()['ok']:
            time.sleep(1)
            result = self.send_request('hello/', device_id=self.device_id)
        else:
            self.access_token = result.json()['response']['token']
        return 0

    def fetch(self):
        result = self.send_request('fetch/', token=self.access_token)
        encodings = [json.loads(result.json()['response']['faces'][i]['embedding'])
                     for i in range(len(result.json()['response']['faces']))]
        ids = [result.json()['response']['faces'][i]['face_id']
               for i in range(len(result.json()['response']['faces']))]
        in_count = result.json()['response']['in_count']
        return encodings, ids, in_count

    def introduce(self, pic, embedding):
        introduce_url = self.url + 'introduce/'
        result = requests.post(introduce_url,
                               data={'token': self.access_token, 'embedding': json.dumps(embedding)},
                               files={'image': pic})

        if result.json()['ok']:
            return {'ok': True, 'face_id': result.json()['response']['face_id']}
        else:
            return {'ok': False}

    def log(self, face_id, enter):
        result = self.send_request('log/', token=self.access_token, face_id=face_id, kind='E' if enter else 'L')
        return result.json()
