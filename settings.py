# utf-8

import os

MYSQL_DATABASE = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': '123456',
        'db': 'pyblog',
}

settings = {
        "static_path": os.path.join(os.path.dirname(__file__), 'static'), 
        "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
        "cookie_secret": "adefMnxO",
#        "login_url": "/login",
        "xsrf_cookies": True,
}

