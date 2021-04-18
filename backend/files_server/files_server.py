from flask import Flask
from werkzeug.middleware.http_proxy import ProxyMiddleware

app_name = 'files_server'
app_files = Flask(app_name)

# 代理到当前hot-update
app = ProxyMiddleware(app_files, {
    '/': {
        "target": "http://localhost:3000/"
    },
    '/static': {
        "target": "http://localhost:3000/"
    }
})
