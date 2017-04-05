import os
import sys

from ezapi.api import api
from asyncpg import connect
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

from ezapi.models import Denomination
#exeception
from asyncpg.exceptions import UniqueViolationError

@api.route('/denominations', methods=['GET'])
async def get_denominations(request):
    q = qb().select(Denomination.id, Denomination.denomination_unit, Denomination.remarks)
    q._from(Denomination)
    async with request.app.pool.acquire() as connection:
        try:
            records = await connection.fetch(q())
        #return the response
        except Exception as e:
            print(e)
            return fatal_error_envelop()
        else:
            return records_json_envelop(records)


@api.route('/denominations', methods=['POST'])
async def create_denomination(request):
    try:
        denom_unit = request.json['denomination_unit'].strip()
    except Exception:
        return fatal_error_envelop()
    
    q = qb().insert(Denomination, Denomination.denomination_unit)
    q.values(denom_unit)
            
    async with request.app.pool.acquire() as connection:
        try:
            status = await connection.execute(q())
        except UniqueViolationError as ue:
            return record_exists_envelop()
        except Exception as e:
            print(e)
            return fatal_error_envelop()
        else:
            return record_created_envelop(request.json)



@api.route('/denominations/<id:int>', methods=['PUT'])
async def update_denomination(request, id):
    #generate the substring of the query 
        sub_string = ', '.join("{} = '{}'".format(key, val) for key, val in request.json.items())
        
        
        query_string = '''Update denominations SET {}  WHERE id= ($1)'''.format(sub_string)
        
        #now update the datbase as well as the set the verificatiion to false
        async with request.app.pool.acquire() as connection:
            try:
                status = await connection.execute(query_string, id, timeout=10.0)
            
            except UniqueViolationError as ue:
                return record_exists_envelop()
            
            except Exception as e:
                return fatal_error_envelop()

            else:
                if status:
                    return record_updated_envelop(request.json)
                else:
                    return record_not_updated_env()
    