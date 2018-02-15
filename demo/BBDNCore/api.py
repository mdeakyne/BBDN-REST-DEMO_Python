"""

    Copyright (C) 2016, Blackboard Inc.
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:

        Redistributions of source code must retain the above copyright notice, this list of conditions and the following
        disclaimer.

        Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
        following disclaimer in the documentation and/or other materials provided with the distribution.

        Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products
        derived from this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
        BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
        EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
        LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
        IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
        OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
# TODO: Implement status codes for responses

from demo.BBDNCore.rest import *
from demo.BBDNCore.session import *


class Api:
    def __init__(self, rest_type, target_url, token, dsk=None):
        self.target_url = target_url
        # rest_type: courses, users, terms, dataSources, etc
        self.rest_type = rest_type
        self.token = token
        self.objects_path = rest.REST_TYPE[self.rest_type]
        self.session = BbSession()

        # remove for production
        self.session.mount('https://', Tls1Adapter())

        # If requesting a single object, just append the ID: (/externalId:)
        self.object_path = self.objects_path + '/externalId:'

        self.has_dsk = False
        self.data_source_pk1 = dsk
        if self.data_source_pk1:
            self.has_dsk = True

        self.term_id = None

        # Like in the init, is class global var really necessary?
        self.payload = {
            "objectType": self.rest_type,
            "externalId": OBJECTEXTERNALID,
            "dataSourceId": "externalId:%s" % DSKEXTERNALID,
            "objectId": OBJECTEXTERNALID,
            "name": self.rest_type.title() + " used for REST demo",
            "description": self.rest_type.title() + " used for REST demo",
            "allowGuests": "true",
            "readOnly": "false",

            # "termId":constants.TERMEXTERNALID,
            "availability": {
                "duration": "continuous"
            }
        }

    def execute(self, command):
        print('[' + self.rest_type + ':execute] : ' + command)

        if "create" in command:
            self.create_object(self.data_source_pk1, self.token)
        elif "read" in command:
            self.get_object()
        elif "read_all" in command:
            print('[' + self.rest_type + ':execute] : ' + command + "not implemented on server")
            self.get_objects()
        elif "update" in command:
            self.update_object()
        elif "delete" in command:
            self.delete_object()

    def create_object(self, is_update=False, create_dsk=False):
        auth_str, headers, path, verify = self.init_vars(is_update)
        headers.update({'Content-Type': 'application/json'})

        data = json.dumps(self.payload)
        r_type = 'post'

        if is_update:
            self.payload.get('availability').update({'available': 'Yes'})
            r_type = 'update'

        if create_dsk:
            self.payload = {"externalId": "%s" % DSKEXTERNALID, "description": "Data Source used for REST demo"}

        if self.rest_type == 'users':
            self.payload.update({"userName": "python_demo",
                                 "password": "python16",
                                 "availability": {
                                     "available": "Yes"
                                 },
                                 "name": {
                                     "given": "Python",
                                     "family": "BbDN",
                                     "middle": "Demo",
                                 },
                                 "contact": {
                                     "email": "no.one@ereh.won",
                                 }})

        if self.rest_type == 'memberships':
            path = path.replace("courseId", "externalId:" + OBJECTEXTERNALID).\
                replace("userId", "externalId:" + OBJECTEXTERNALID)
            self.payload.update({"courseRoleId": "Instructor"})

        r = self.session.rerieve(r_type, path, headers, verify, data=data)

        self.set_json(r)

    def update_object(self):
        # Technically not really needed, but left for semantics
        self.create_object(is_update=True)

    def get_objects(self, is_single=False):
        auth_str, headers, path, verify = self.init_vars(is_single)

        print('[' + self.rest_type + ':get_objects()] GET Request URL: ' + path)

        r = self.session.rerieve('get', path, headers, verify)

        print('[' + self.rest_type + ':get_objects()] STATUS CODE: ' + str(r.status_code))
        print('[' + self.rest_type + ':get_objects()] RESPONSE:')

        self.set_json(r)

    def get_object(self):
        # Technically not really needed, but left for semantics
        self.objects_path(is_single=True)

    def delete_object(self):
        auth_str, headers, path, verify = self.init_vars(is_single=True)

        r = self.session.rerieve('delete', path, headers=headers, verify=verify)

        self.set_json(r)

    def init_vars(self, is_single=False):
        print('[' + self.rest_type + ':get_objects()] token: ' + self.token)
        # "Authorization: Bearer $token"

        auth_str = 'Bearer ' + self.token
        print('[' + self.rest_type + ':get_objects()] authStr: ' + auth_str)

        path = "https://" + self.target_url

        # Can also be used to allow for multiple objects
        if is_single:
            path += self.object_path + OBJECTEXTERNALID
        else:
            path += self.objects_path

        headers = {'Authorization': auth_str, 'Content-Type': 'application/json'}
        verify = False

        return auth_str, headers, path, verify

    def set_json(self, response):
        print('[' + self.rest_type + ':createCourse()] STATUS CODE: ' + str(response.status_code))
        print('[' + self.rest_type + ':createCourse()] RESPONSE:')

        if response.text:
            res = json.loads(response.text)
            print(json.dumps(res, indent=4, separators=(',', ': ')))

            # TODO: Better implementation is needed to check against DSK
            # parsed_json = json.loads(response.text)
            # self.data_source_pk1 = parsed_json['id']

        else:
            print("NONE")

    def check_data_source(self):
        self.get_object()
        if not self.data_source_pk1:
            print("[datasource::checkDataSource] Data Source %s does not exist, creating." % OBJECTEXTERNALID)
            self.create_object(create_dsk=True)
