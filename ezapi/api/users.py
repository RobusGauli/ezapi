import os
import sys


from sanic.response import json
from ezapi.envelop.response_envelop import (
    records_json_envelop,
    record_exists_envelop, 
    record_json_envelop, 
    record_created_envelop, 
    record_notfound_envelop,
    record_updated_envelop, 
    record_not_updated_env, 
    fatal_error_envelop
)

from ezapi.pqb import QueryBuilder as qb
from ezapi.models import Teller
from ezapi.api import api
from ezapi.utils import hash_password

from asyncpg.exceptions import UniqueViolationError


@api.route('/users', methods=['POST'])
async def register_user(request):
    #check to see if all the keys existst
    if not set(request.json.keys()) == {'teller_id', 'password', 'expiry_date', 'branch_id'}:
        return json({'message' : 'Missing Keys'})

    #check to see of all the values in the json fields has lenght more than 5
    if any(len(val) < 5 for val in request.json.values()):
        return json({'message' : 'Not adequate length of the values'})
    
    #now if everything is okay, we will grab the password field and hash it
    #try generating access token , store them in database and if successfull
    #return the access token in the returned field 

    sha_hash  = hash_password(request.json.get('password').strip().encode())
    #now generate the access_token based
    return json({'sha_hash' : sha_hash})



