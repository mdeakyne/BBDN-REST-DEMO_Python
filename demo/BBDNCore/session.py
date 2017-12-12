import requests


class BbSession(requests):
    def __init__(self):
        self.method = None

    def retrieve(self, method, path, headers, verify, data=None):
        self.method = method.lower()

        if self.r_type == 'get':
            self.get(path, headers, verify)
        elif self.r_type == 'post':
            self.post(path, data=data, headers=headers, verify=verify)
        elif self.r_type == 'patch':
            self.patch(path, data=data, headers=headers, verify=verify)
        elif self.r_type == 'delete':
            self.delete(path, headers, verify)