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

from demo.BBDNCore.api import *

import sys
import getopt


def main(argv):
    _target_url = ''
    _command = ''
    _all = False
    _auth = False
    _date_source = False
    _term = False
    _course = False
    _users = False
    _membership = False
    _cleanup = False

    _data_source_pk1 = None

    datasource_session = None
    course_session = None
    membership_session = None
    term_session = None
    user_session = None
    usage_str = ''.join(["\nrestdemo.py -t|--target <target root URL> -c|--command <command>\n",
                         "e.g restdemo.py -t www.myschool.edu -c create_course\n",
                         "command: <command>_<object> where <command> is one of the following:\n",
                         "\tcreate, read, read_all, update, delete\n",
                         "and <object> is one of the following:\n",
                         "\tdatasource, term, course, user, membership\n",
                         "-t is required; No -c args will run demo in predetermined order.\n",
                         "'-c authorize' demonstrates the authorization process and does not create objects.",
                         "-c commands require a valid datasource PK1 - \n",
                         "\ta datasource get will be run in these cases, defaulting to create\n",
                         "\tif the demo datasource does not exist."])

    if len(sys.argv) > 1:  # there are command line arguments
        try:
            opts, args = getopt.getopt(argv, "ht:c:", ["target=", "command="])
        except getopt.GetoptError:
            print(usage_str)
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print(usage_str)
                sys.exit()
            elif opt == '-d':
                print("Deleting at end of run.")
                _cleanup = True
            elif opt in ("-t", "--target"):
                _target_url = arg.lstrip()
            elif opt in ("-c", "--command"):
                _command = arg
            else:
                _command = "Run All"
        print('[main] Target is:', _target_url)
        print('[main] Command is:', _command)
    else:
        print(usage_str)
        sys.exit(2)

    # Set up some booleans for processing flags and order of processing
    if "course" in _command:
        print("[main] Run course command")
        _course = True
    elif "user" in _command:
        print("[main] Run user command")
        _users = True
    elif "membership" in _command:
        print("[main] Run membership command")
        _membership = True
    elif "term" in _command:
        print("[main] Run term command")
        _term = True
    elif "datasource" in _command:
        print("[main] Run datasource command")
        _date_source = True
    elif "authorize" in _command:
        print("[main] Run authorization command")
        _auth = True
    else:
        print("[main] Empty Command: Run All\n")
        _all = True

    print('\n[main] Acquiring auth token...\n')
    authorized_session = AuthToken(_target_url)
    authorized_session.set_token()
    print('\n[main] Returned token: ' + authorized_session.get_token() + '\n')

    if not _auth:
        # run commands in required order if running ALL
        if _date_source or _all:

            # process Datasource command
            print("\n[main] Run datasource command: " + ('ALL' if _all else _command) + '...')

            datasource_session = Api('dataSource', _target_url, authorized_session.get_token())

            if 'datasource' in _command:
                datasource_session.execute(_command)
            else:
                if not datasource_session:
                    datasource_session.get_object()
                    _data_source_pk1 = datasource_session.data_source_pk1
                datasource_session.create_object(create_dsk=True)
                datasource_session.get_object()
                datasource_session.get_objects()
                datasource_session.update_object()

        if _term or _all:
            term_session = Api('term', _target_url, authorized_session.get_token())
            # process term command
            print("\n[main] Run term command: " + ('ALL' if _all else _command) + '...')
            if 'term' in _command:
                if ('delete' in _command) or ('read' in _command):
                    print("[main] Deleting or getting does not require a datasource.")
                else:
                    if not _data_source_pk1:
                        print("[main] confirm datasource.")
                        datasource_session = Api('dataSource', _target_url, authorized_session.get_token())
                        datasource_session.check_data_source()

                term_session.execute(_command)
            else:
                term_session.get_objects()
                term_session.create_object()
                term_session.get_object()
                term_session.update_object()

        if _course or _all:
            course_session = Api('course', _target_url, authorized_session.get_token())
            # process course command
            print("\n[main] Run course command: " + ('ALL' if _all else _command) + '...')
            if 'course' in _command:
                if ('delete' in _command) or ('read' in _command):
                    print("[main] Deleting or getting does not require a datasource.")
                else:
                    if not _data_source_pk1:
                        print("[main] confirm datasource.")
                        datasource_session = Api('dataSource', _target_url, authorized_session.get_token())
                        datasource_session.check_data_source()

                course_session.execute(_command)
            else:
                course_session.get_objects(authorized_session.get_token())
                course_session.create_object()
                course_session.get_object()
                course_session.update_object()

        if _users or _all:
            user_session = Api('user', _target_url, authorized_session.get_token())
            # process user command
            print("\n[main] Run user command: " + ('ALL' if _all else _command) + '...')
            if 'user' in _command:
                if ('delete' in _command) or ('read' in _command):
                    print("[main] Deleting or getting does not require a datasource.")
                else:
                    if not _data_source_pk1:
                        print("[main] confirm datasource.")
                        datasource_session = Api('dataSource', _target_url, authorized_session.get_token())
                        datasource_session.check_data_source()

                user_session.execute(_command)
            else:
                user_session.get_objects()
                user_session.create_object()
                user_session.get_object()
                user_session.update_object()

        if _membership or _all:
            membership_session = Api('membership', _target_url, authorized_session.get_token())

            # process membership command
            print("\n[main] Run membership command: " + ('ALL' if _all else _command) + '...')
            if 'membership' in _command:
                if ('delete' in _command) or ('read' in _command):
                    print("[main] Deleting or getting does not require a datasource.")
                else:
                    if not _data_source_pk1:
                        print("[main] confirm datasource.")
                        datasource_session = Api('dataSource', _target_url, authorized_session.get_token())
                        datasource_session.check_data_source()

                membership_session.execute(_command)
            else:
                membership_session.get_object()
                membership_session.create_object()
                membership_session.get_object()
                membership_session.update_object()
                # membership_session.readUserMemberships(authorized_session.get_token())
    # clean up if not using individual commands
    if _all:
        print('\n[main] Completing Demo and deleting created objects...')
        print("[main] Deleting membership")
        membership_session.delete_object()
        print("[main] Deleting User")
        user_session.delete_object()
        print("[main] Deleting Course")
        course_session.delete_object()
        print("[main] Deleting Term")
        term_session.delete_object()
        print("[main] Deleting DataSource")
        datasource_session.delete_object()
    else:
        print("\nRemember to delete created demo objects!")

    print("[main] Processing Complete")

    # revoke issued Token
    # authorized_session.revokeToken()


if __name__ == '__main__':
    main(sys.argv[1:])
