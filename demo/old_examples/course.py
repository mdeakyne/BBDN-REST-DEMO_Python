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

from demo.BBDNCore.rest import *


class Course():
    def __init__(self, target_url, token):
        self.target_url = target_url
        self.token = token

        # create(POST)/get(GET)
        self.courses_Path = '/learn/api/public/v1/courses'
        # If requesting a singer user, just append the ID: (/externalId:)
        self.course_Path = '/learn/api/public/v1/courses/externalId:'
        self.termId = None

    def execute(self, command, dsk, token):
        if "create" in command:
            print('[Course:execute] : ' + command)
            self.createCourse(dsk, token)
        elif "read" in command:
            print('[Course:execute] : ' + command)
            self.getCourse(token)
        elif "read_all" in command:
            print('[Course:execute] : ' + command + "not implemented on server")
            # self.getCourses(token)
        elif "update" in command:
            print('[Course:execute] : ' + command)
            self.updateCourse(dsk, token)
        elif "delete" in command:
            print('[Course:execute] : ' + command)
            self.deleteCourse(token)

    def getCourses(self, token):
        print('[Course:getCourses()] token: ' + token)
        # "Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Course:getCourses()] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter())  # remove for production
        print("[Course:getCourses()] GET Request URL: https://" + self.target_url + self.courses_Path)
        r = session.get("https://" + self.target_url + self.courses_Path, headers={'Authorization': authStr},
                        verify=False)
        print("[Course:getCourses()] STATUS CODE: " + str(r.status_code))
        print("[Course:getCourses()] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res, indent=4, separators=(',', ': ')))
        else:
            print("NONE")

    def createCourse(self, dsk, token):
        # "Authorization: Bearer $token"
        authStr = 'Bearer ' + token

        self.PAYLOAD = {
            "externalId": COURSEEXTERNALID,
            "dataSourceId": "externalId:%s" % DSKEXTERNALID,
            "courseId": COURSEEXTERNALID,
            "name": "Course used for REST demo",
            "description": "Course used for REST demo",
            "allowGuests": "true",
            "readOnly": "false",
            # "termId":constants.TERMEXTERNALID,
            "availability": {
                "duration": "continuous"
            }
        }

        session = requests.session()
        session.mount('https://', Tls1Adapter())  # remove for production with commercial cert
        print("[Course:createCourse()] POST Request URL: https://" + self.target_url + self.courses_Path)
        print("[Courses:createCourse()] JSON Payload: \n " + json.dumps(self.PAYLOAD, indent=4, separators=(',', ': ')))
        r = session.post("https://" + self.target_url + self.courses_Path, data=json.dumps(self.PAYLOAD),
                         headers={'Authorization': authStr, 'Content-Type': 'application/json'}, verify=False)
        print("[Course:createCourse()] STATUS CODE: " + str(r.status_code))
        print("[Course:createCourse()] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res, indent=4, separators=(',', ': ')))
        else:
            print("NONE")

    def getCourse(self, token):
        print('[Course:getCourse()] token: ' + token)
        # "Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Course:getCourses] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter())  # remove for production
        print("[Course:getCourse()] GET Request URL: https://" + self.target_url + self.course_Path + COURSEEXTERNALID)
        r = session.get("https://" + self.target_url + self.course_Path + COURSEEXTERNALID,
                        headers={'Authorization': authStr}, verify=False)

        print("[Course:getCourse()] STATUS CODE: " + str(r.status_code))
        print("[Course:getCourse()] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res, indent=4, separators=(',', ': ')))
        else:
            print("NONE")

    def updateCourse(self, dsk, token):
        # "Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print("[Course:updateCourse()] COURSEEXTERNALID: " + COURSEEXTERNALID)

        self.PAYLOAD = {
            "externalId": COURSEEXTERNALID,
            "dataSourceId": "externalId:%s" % DSKEXTERNALID,
            "courseId": COURSEEXTERNALID,
            "name": "Course used for REST Python demo",
            "description": "Course used for REST Python demo",
            "allowGuests": "true",
            "readOnly": "false",
            # "termId":constants.TERMEXTERNALID,
            "availability": {
                "available": "Yes",
                "duration": "continuous"
            }
        }
        session = requests.session()
        session.mount('https://', Tls1Adapter())  # remove for production with commercial cert
        print(
            "[Course:updateCourse()] PATCH Request URL: https://" + self.target_url + self.course_Path + COURSEEXTERNALID)
        print("[Courses:updateCourse()] Result: \n " + json.dumps(self.PAYLOAD, indent=4, separators=(',', ': ')))
        r = session.patch("https://" + self.target_url + self.course_Path + COURSEEXTERNALID,
                          data=json.dumps(self.PAYLOAD),
                          headers={'Authorization': authStr, 'Content-Type': 'application/json'}, verify=False)

        print("[Course:updateCourse()] STATUS CODE: " + str(r.status_code))
        print("[Course:updateCourse()] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res, indent=4, separators=(',', ': ')))
        else:
            print("NONE")

    def deleteCourse(self, token):
        # "Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print("[Course:deleteCourse()] COURSEEXTERNALID: " + COURSEEXTERNALID)

        session = requests.session()
        session.mount('https://', Tls1Adapter())  # remove for production with commercial cert
        print(
            "[Course:deleteCourse()] DELETE Request URL: https://" + self.target_url + self.course_Path + COURSEEXTERNALID)
        print("[Courses:deleteCourse()] JSON Payload: NONE REQUIRED")
        r = session.delete("https://" + self.target_url + self.course_Path + COURSEEXTERNALID,
                           headers={'Authorization': authStr}, verify=False)

        print("[Course:deleteCourse()] STATUS CODE: " + str(r.status_code))
        print("[Course:deleteCourse()] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res, indent=4, separators=(',', ': ')))
        else:
            print("NONE")
