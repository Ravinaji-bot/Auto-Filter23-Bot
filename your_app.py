def wsgi(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [b"Bot is Running"]

import subprocess
subprocess.Popen(["python", "main.py"])
