from config import config
from curio import network, run
from logs import setup_logging

logger = setup_logging(__name__)


async def main(host, port):
    try:
        sock = await network.open_connection(host, port)
    except ConnectionRefusedError:
        return False
    else:
        data = b'wat\n'
        await sock.sendall(data)
        resp = await sock.recv(4096)
        return resp


if __name__ == '__main__':
    # from curio.debug import schedtrace
    # run(main('', 9000), with_monitor=True, debug=schedtrace)
    back = run(main('localhost', config.get('port')))
    logger.info(back)
