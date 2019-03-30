"""     Production Server Settings      """

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','192.168.1.5'
                 'localhost',
                 'elms.pythonanywhere.com',
                 'www.icts-learninganalytics.com',
                 'icts-learninganalytics-env.bfm8ehhfbp.us-east-1.elasticbeanstalk.com',]