bind = "0.0.0.0:8000"
workers = 3
accesslog = "/home/ubuntu/studio/gunicorn.access.log"
errorlog = "/home/ubuntu/studio/gunicorn.error.log"
capture_output = True
loglevel = "debug"