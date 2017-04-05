import os
import asyncio

from ezapi.app_config import create_app
from asyncpg import connect, create_pool

DB_CONFIG = {
    'host' : 'localhost',
    'user' : 'user',
    'password' : 'postgres',
    'port' : '5432',
    'database' : 'easydeposit'

}
app = create_app()

@app.listener('before_server_start')
async def resgister_db(app, loop):
    app.pool = await create_pool(**DB_CONFIG, loop=loop, max_size=300)


if __name__ =='__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)