from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from config import Constants
from apis.apis import app as app_api
from files_server.files_server import app as app_file

# 中间件：路由合并
dm = DispatcherMiddleware(app_file, {Constants.API_PATH: app_api})
# dm = app_api


if __name__ == '__main__':
    run_simple(Constants.RUN_LISTENING, Constants.RUN_PORT, dm, use_reloader=Constants.RUN_USE_RELOAD, threaded=True)
