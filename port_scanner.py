from aiohttp import web
import asyncio
import logging
import json


# create connection with ip, port, event loop, awaited_time
async def check_connection(ip, port, scan_loop, awaited_time):
    conn = asyncio.open_connection(ip, port, loop=scan_loop)
    try:
        # wait for response for awaited_time
        await asyncio.wait_for(conn, awaited_time)
        # receive response
        return {"port": str(port), "state": "open"}
    except asyncio.TimeoutError:  # use awaited_time to start async timer
        # not receive response in awaited_time
        return {"port": str(port), "state": "closed"}


# iterator
async def iterate(ip, begin_port, end_port, scan_loop, awaited_time):
    # create task with ip, port range, awaited_time
    task = [check_connection(ip, port, scan_loop, awaited_time) for port in
            range(begin_port, end_port + 1)]
    # await fulfilling
    response = await asyncio.gather(*task)
    return response


# validation
def check_input(request):
    try:
        # split and check ip
        ip = request.match_info.get('ip').split('.')
        if type(ip) != 'list' and len(ip) != 4:
            raise ValueError('IP is incorrect.')
        for item in ip:
            if not 0 <= int(item) <= 255:
                raise Exception(f'({item}) in IP is incorrect.')
        # check begin_port and end_port
        begin_port = int(request.match_info.get('begin_port'))
        end_port = int(request.match_info.get('end_port'))
        if not 0 < begin_port <= 65535:
            raise ValueError(f'({begin_port}) - begin_port out of range.')
        if not 0 < end_port <= 65535:
            raise ValueError(f'({end_port}) - end_port out of range.')
        if not begin_port <= end_port:
            raise ValueError(f'begin_port ({begin_port}) is bigger than end_port ({end_port}).')
    except Exception as e:
        print(e)
        # with error
        return False
    # without any errors
    return True


# handler
async def handle(request):
    if check_input(request):  # validation is OK
        ip = request.match_info.get('ip')
        begin_port = int(request.match_info.get('begin_port'))
        end_port = int(request.match_info.get('end_port'))
        # param = request.match_info.get('param')
        # print(request)
        # print(type(request))
        awaited_time = 5  # in sec, duration of connection
        scan_loop = asyncio.get_running_loop()  # IDK, but in some wrote it should speed up program
        response = await iterate(ip, begin_port, end_port, scan_loop, awaited_time)
        # print(results)
        # buffer = []
        # if param == 'open':
        #    [buffer.append(item) for item in results if item['state'] == 'open']
        #    response = buffer
        # elif param == 'closed':
        #    [buffer.append(item) for item in results if item['state'] == 'closed']
        #    response = buffer

        return web.Response(text=json.dumps(response), status=200)  # format to json
    else:  # request is NOT OK
        return web.Response(text='400: Bad Request', status=400)  # format to json


# initializing app
def create_app():
    app = web.Application()
    # choose specific listening route, start handler
    app.router.add_get('/scan/{ip}/{begin_port}/{end_port}', handle)
    # app.router.add_get('/scan/{ip}/{begin_port}/{end_port}/{param}', handle)
    return app


# logger
logger = logging.getLogger('aiohttp.access')
logger.setLevel(logging.DEBUG)  # aiohttp.access time GMT+0000 request + HTTP1.1 IDK Browser version
# logger.addHandler(logging.StreamHandler()) # log in console
logging.basicConfig(filename='syslog.log', encoding='utf-8', level=logging.DEBUG)  # log in file

# start program
if __name__ == '__main__':
    web.run_app(create_app())
