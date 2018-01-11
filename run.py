#!/usr/bin/env python3

from ibuk.main import app
from ibuk.common import config


app.config.from_object(config.Configuration)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
