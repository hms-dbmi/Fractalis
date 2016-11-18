"""Initalize Fractalis Flask app and configure it.

Modules in this package:
    - config -- Manages Fractalis Flask app configuration
"""
import logging

from flask import Flask

from fractalis.session import RedisSessionInterface
from fractalis.analytics.controllers import analytics_blueprint


app = Flask(__name__)
app.config.from_object('fractalis.config')
try:
    app.config.from_envvar('FRACTALIS_CONFIG')
except RuntimeError:
    app.logger.warning("FRACTALIS_CONFIG is not set. Using defaults.")

app.session_interface = RedisSessionInterface(app.config)
app.register_blueprint(analytics_blueprint, url_prefix='/analytics')

if __name__ == '__main__':
    handler = logging.handlers.TimedRotatingFileHandler('fractalis.log',
                                                        when='midnight',
                                                        backupCount=14)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
