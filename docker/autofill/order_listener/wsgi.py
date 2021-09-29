# Wait for incoming XML orders, then
# run autofill.py and forward to VNC

# For debugging:
import cgitb
cgitb.enable()

from cgi import FieldStorage

def application(environ, start_response):
    form = FieldStorage()
    print(form) # debug



    data = b"Hello, World!\n"
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])
