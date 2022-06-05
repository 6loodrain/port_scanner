from aiohttp import web
import asyncio
import logging
import json


async def check_connection(ip, port, scan_loop, awaited_time):
    conn = asyncio.open_connection(ip, port, loop=scan_loop)
    try:
        await asyncio.wait_for(conn, awaited_time)
        return {"port": str(port), "state": "open"}
    except asyncio.TimeoutError:
        return {"port": str(port), "state": "closed"}


async def iterate(ip, begin_port, end_port, scan_loop, awaited_time):
    task = [check_connection(ip, port, scan_loop, awaited_time) for port in
            range(begin_port, end_port + 1)]
    response = await asyncio.gather(*task)
    return response


# validation
def check_input(request):
    try:

        ip = request.match_info.get('ip').split('.')

        if type(ip) != 'list' and len(ip) != 4:
            logging.error('IP is incorrect.')
            raise Exception()
        for item in ip:
            if not 0 <= int(item) <= 255:
                logging.error(f'({item}) in IP is incorrect.')
                raise Exception()

        begin_port = int(request.match_info.get('begin_port'))
        end_port = int(request.match_info.get('end_port'))

        if not 0 < begin_port <= 65535:
            logging.error(f'({begin_port}) - begin_port out of range.')
            raise Exception()
        if not 0 < end_port <= 65535:
            logging.error(f'({end_port}) - end_port out of range.')
            raise Exception()
        if not begin_port <= end_port:
            logging.error(f'begin_port ({begin_port}) is bigger than end_port ({end_port}).')
            raise Exception()

    except Exception:
        return False
    return True


async def handle(request):
    if check_input(request):

        ip = request.match_info.get('ip')
        begin_port = int(request.match_info.get('begin_port'))
        end_port = int(request.match_info.get('end_port'))

        awaited_time = 5  # in sec
        scan_loop = asyncio.get_running_loop()
        response = await iterate(ip, begin_port, end_port, scan_loop, awaited_time)

        return web.Response(text=json.dumps(response), status=200)
    else:
        return web.Response(text='400: Bad Request', status=400)


def create_app():
    app = web.Application()
    app.router.add_get('/scan/{ip}/{begin_port}/{end_port}', handle)
    return app


logger = logging.getLogger('aiohttp.access')
logger.setLevel(logging.DEBUG)
# default log in console
# logging.basicConfig(filename='syslog.log', encoding='utf-8', level=logging.DEBUG)  # log in file

if __name__ == '__main__':
    web.run_app(create_app())
