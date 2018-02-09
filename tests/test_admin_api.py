# Copyright (C) 2016 University of Zurich.  All rights reserved.
#
# This file is part of MSRegistry Backend.
#
# MSRegistry Backend is free software: you can redistribute it and/or
# modify it under the terms of the version 3 of the GNU Affero General
# Public License as published by the Free Software Foundation, or any
# other later version.
#
# MSRegistry Backend is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the version
# 3 of the GNU Affero General Public License for more details.
#
# You should have received a copy of the version 3 of the GNU Affero
# General Public License along with MSRegistry Backend.  If not, see 
# <http://www.gnu.org/licenses/>.

__author__ = "Filippo Panessa <filippo.panessa@uzh.ch>"
__copyright__ = ("Copyright (c) 2016 S3IT, Zentrale Informatik,"
" University of Zurich")


import unittest
import requests
import json
import urlparse

TESTS = [("get","/admin/survey"),
         ("get","/admin/survey/user/{0}"),
         ("post","/admin/survey/{0}"),
         ("delete","/admin/survey/{0}")]

class AdminAPIsTestCase(unittest.TestCase):
    userID = 'd4c74594d841139328695756648b6bd6'
    surveyID = '57631e93ec71bc7d2337482e'
    username = "testme"
    password = "letmein"
    url_prefix = "http://130.60.24.94:5001/api/v1.0/{0}"
    survey = {'survey': {'sectionA': 'ALL REMOVED', 'sectionB': '', 'sectionC': 1}, 'tags': ['layer2'], 'ongoing': True}

    def get_response(method,request,payload=None):
        method_to_call = getattr(requests,method)
        return method_to_call(url_prefix.format(request),
                              auth=(username,
                                    password),
                              data=payload
                              )
        
    def test_addByUniqueID(self):
        r = get_response("get","/admin/survey")
        print r.status_code
        if r.status_code != 200:
            print r.text
        r = get_response("get","/admin/survey/user/{0}".format(userID))
        print r.status_code
        if r.status_code != 200:
            print r.text
        r = get_response("post",
                         "/admin/survey/{0}".format(surveyID),
                         payload=json.dumps(survey))
        print r.status_code
        if r.status_code != 200:
            print r.text
        # r = get_response("delete","/admin/survey/{0}".format(surveyID))

        
