from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer

from app import app, create_app

http_server = WSGIServer(("", 5000), create_app(app))
http_server.serve_forever()
