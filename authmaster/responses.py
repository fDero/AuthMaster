from exceptions import *
from __init__ import *
from http import HTTPStatus
from flask import Response
import json


def response_account_verificaton_success_response(account : dict, jwt : str) -> Response:
    response_json = {
        'outcome': 'success',
        'message': 'Account successfully verified',
        'account': {
            'email': account['email'],
            'username': account['uname'],
            'id': str(account['_id']),
        }
    }
    response_headers = { 'X-JWT-Token': jwt }
    response_status = HTTPStatus.CREATED
    return Response(
        response=json.dumps(response_json),
        status=response_status,
        headers=response_headers,
        mimetype='application/json'
    )


def response_account_registration_init_success(email: str) -> Response:
    response_json ={
        'outcome': 'success',
        'message': f'An email has been sent to: {email}'
    }
    response_headers = {}
    response_status = HTTPStatus.OK
    return Response(
        response=json.dumps(response_json),
        status=response_status,
        headers=response_headers,
        mimetype='application/json'
    )


def response_oauth_token_recognized(user_info: dict, provider: str) -> Response:
    response_headers = {
        'X-OAuth-Provider': provider
    }
    response_status = HTTPStatus.ACCEPTED
    response_json = { 
        'email': user_info.get('email'),
        'name': user_info.get('name'),
        'id': user_info.get('id'),
        'picture': user_info.get('picture')
    }
    return Response(
        response=json.dumps(response_json),
        status=response_status,
        headers=response_headers,
        mimetype='application/json'
    )


def response_account_login_success_response(account: dict, jwt: str) -> Response:
    response_json = {
        'outcome': 'success',
        'message': 'Login successful',
        'account': {
            'email': account['email'],
            'username': account['uname'],
            'id': str(account['_id']),
        }
    }
    response_headers = { 'X-JWT-Token': jwt }
    response_status = HTTPStatus.OK
    return Response(
        response=json.dumps(response_json),
        status=response_status,
        headers=response_headers,
        mimetype='application/json'
    )