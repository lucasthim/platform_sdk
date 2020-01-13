import os

from platform_sdk.utils.http import HttpClient

class SystemCore:

    def __init__(self,url,entity = None):
        if entity is None:
            self.entity = 'system'
        else:
            self.entity = entity
        self.url = url
        self.http_client = HttpClient()

    def create(self,mapping):
        if type(mapping) != list:
            mapping = [mapping]
            
        for m in mapping:
            m['_metadata'] = {
            'type':self.entity,
            'changeTrack':'create'
            }
        url = self.url + 'persist'
        return self.http_client.post(url,mapping)

    def find_by_id(self, id):
        url = self.url + self.entity + '?filter=byId' + '&id=' + id
        return self.http_client.get(url)