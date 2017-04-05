from sanic.response import json
from ezapi.api import api
from asyncpg import connect

from ezapi.envelop.response_envelop import (
    records_json_envelop,
    record_exists_envelop,
    record_json_envelop,
    record_created_envelop,
    record_notfound_envelop,
    record_updated_envelop,
    record_not_updated_env
)



#exceptiohns
from asyncpg.exceptions import UniqueViolationError

def jsonify(records):
    gen_exp = (dict(record) for record in records)
    return gen_exp



@api.route('/branches', methods=['GET'])
async def get_branches(request):
    async with request.app.pool.acquire() as connection:
        records = await connection.fetch('SELECT * from branches')
        
        #return json({'data': list(jsonify(records))})
        return records_json_envelop(records, code=200)


@api.route('/branches', methods=['POST'])
async def create_branch(request):
    async with request.app.pool.acquire() as connection:
        data = request.json
        try:
            result = await connection.fetch('''INSERT INTO branches(name, branch_code, address, remarks)
                                            values ($1, $2, $3, $4)''', data['name'], data['branch_code'], data['address'], data['remarks'], timeout=10.0)
            
            
        except UniqueViolationError as ue:
            return record_exists_envelop()
        else:
            #if everything went right
            return record_created_envelop(request.json)


@api.route('/branches/<id:int>', methods = ['GET'])
async def get_branch(request, id):
    '''This method returns the information for each branch.
        Example: > GET /branches/ HTTP/1.1
                 < {
                     data : [
                        branch_id : 1,
                        name : 'droes',
                        'address' : 'so',
                        ....
                     ],
                     code : '200', 
                     status : 'pass
                 }
    '''
    print(request.args)
    async with request.app.pool.acquire() as connection:
        try:
            record = await connection.fetchrow(''' SELECT id, name, branch_code, created_at, updated_at, verified, address, remarks
                                 FROM branches WHERE id = ($1)''', id, timeout=5.0)
        except Exception as e:
            print(e)
            return json({'code': '404', 'status' : 'fail'})
        
        else:
            if record:
                return record_json_envelop(record, code=200)
            else:
                return record_notfound_envelop()
    
    

@api.route('/branches/<id:int>', methods=['PUT'])
async def update_branch(request, id):
    async with request.app.pool.acquire() as connection:
        
        #generate the substring of the query 
        sub_string = ', '.join("{} = '{}'".format(key, val) for key, val in request.json.items())
        print(sub_string)
        
        query_string = '''Update branches SET {} , updated_at = Now() WHERE id= ($1)'''.format(sub_string)
        print(query_string)
        #now update the datbase as well as the set the verificatiion to false
        try:
            status = await connection.execute(query_string, id, timeout=10.0)
            print(status)
        except UniqueViolationError as ue:
            return record_exists_envelop()
            
        except Exception as e:
            print(e)

        else:
            if status:
                return record_updated_envelop(request.json)
            else:
                return record_not_updated_env()








