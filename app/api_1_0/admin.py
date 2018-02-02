# Copyright (C) 2018, 2019 University of Zurich.  All rights reserved.
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

__author__ = "Sergio Maffioletti <sergio.maffioletti@uzh.ch>"
__copyright__ = ("Copyright (c) 2018, 2019 S3IT, Zentrale Informatik,"
" University of Zurich")


from flask import jsonify, request
from flask import _app_ctx_stack as stack
from flask_httpauth import HTTPBasicAuth
from flask import current_app

from . import api
from app.models.role import Role
from app.models.survey import Survey

from app import db
from app import localauth
from app.auth.decorators import requires_auth, requires_roles, requires_consent

from app.exceptions import SurveyNotFound, MethodNotAllowed

from jsonschema import validate, ValidationError

from app import inputs
from app import utils


# Simple username/password authentication.
@localauth.get_password
def get_pw(username):
    app = current_app._get_current_object()
    if username == app.config['AUTH_USER']:
        return app.config['ACCESS_KEY']
    return None


# Admin endpoints for Survey management

## GET operations

@api.route('/admin/survey', methods=['GET'])
@localauth.login_required
def get_all_surveys():
    """
    Get all surveys for all users.
    """
    survey = Survey()
    try:
        return jsonify(surveys=[ob.serialize() for ob in survey.getAll()])
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except db.BadValueException as error:
        raise MethodNotAllowed(error.message)


@api.route('/admin/survey/user/<string:_uid>', methods=['GET'])
@localauth.login_required
def get_all_surveys_by_user(_uid):
    """
    Get all surveys for a given user
    """
    survey = Survey()
    try:
        return jsonify(surveys=[ob.serialize() for ob in survey.getAllByUniqueID(_uid,
                                                                                 utils.Time.Iso8601ToDatetime(request.args.get('from', None)),
                                                                                 utils.Time.Iso8601ToDatetime(request.args.get('until', None)),
                                                                                 request.args.get('tags').split(',') if request.args.get('tags', None) is not None else None,
                                                                                 utils.json.Json._getJSONBool(request.args.get('ongoing', None)),
                                                                                 )])
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except db.BadValueException as error:
        raise MethodNotAllowed(error.message)


## POST operations

@api.route('/admin/survey/<string:_id>', methods=['POST'])
@localauth.login_required
@requires_consent
def update_user_survey_by_id(_id):
    """
    Update/replace existing survey by _id
    """
    survey = Survey()
    consent = request.get_json(silent=True, force=True)

    try:
        return jsonify(success=bool(survey.updateByUniqueID(_id,
                                                            consent['survey'],
                                                            consent['tags'],
                                                            consent['ongoing'])))
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except db.BadValueException as error:
        raise MethodNotAllowed(error.message)

## DELETE operations

@api.route('/admin/survey/<string:_id>', methods=['DELETE'])
@localauth.login_required
def delete_survey_by_id(_id):
    """
    Update/replace existing survey by _id
    """
    survey = Survey()
    try:
        return jsonify(success=bool(survey.deleteByUniqueID(_id)))
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except db.BadValueException as error:
        raise MethodNotAllowed(error.message)
