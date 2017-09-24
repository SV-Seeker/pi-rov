import logging

from gevent import monkey

from geventwebsocket import WebSocketServer, WebSocketApplication, Resource


logger = logging.getLogger(__name__)


monkey.patch_all()


class ROVApplication(WebSocketApplication):
    def on_open(self):
        logger.info('connection opened')

    def on_message(self, message):
        self.ws.send(message)

    def on_close(self, reason):
        logger.info('connection closed: %s', reason)


resource = Resource([
    ('^/rov', ROVApplication),
])


if __name__ == "__main__":
    server = WebSocketServer(('', 8000), resource, debug=True)
    server.serve_forever()
