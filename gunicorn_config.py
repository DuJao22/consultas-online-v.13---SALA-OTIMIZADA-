import os

bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"

worker_class = 'gthread'

workers = 1

threads = 100

timeout = 300

keepalive = 5

max_requests = 1000
max_requests_jitter = 50

preload_app = False

accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
