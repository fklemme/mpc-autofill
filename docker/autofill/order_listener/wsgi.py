# Wait for incoming XML orders, then
# run autofill.py and forward to VNC

from os import mkdir
from os.path import dirname
from secrets import token_urlsafe
from subprocess import Popen, PIPE, STDOUT
from werkzeug.wrappers import Request, Response

def application(environ, start_response):
    request = Request(environ)
    print(request) # debug

    if request.method == 'POST':
        # Get the XML order
        xml = request.form['xml']

        # Store to new folder
        xml_path = '/mpc_orders/order_{}/cards.xml'.format(token_urlsafe(8))
        mkdir(dirname(xml_path))
        with open(xml_path, 'w') as xml_file:
            xml_file.write(xml)

        # Environment needed for Google Chrome
        autofill_env = {
            'USER': 'mpcautofill',
            'HOME': '/home/mpcautofill',
        }

        # TODO: below not yet working...
        # Run autofill
        autofill_process = Popen(
            ['python3', '/MPCAutofill/autofill.py'],
            env=autofill_env,
            cwd=dirname(xml_path),
            stdout=PIPE,
            stderr=STDOUT)
        # Do not wait for anything, just continue...

        # Redirect to VNC client
        response = Response('Thank you for traveling with MPCAutofill!')
        response.status_code = 302
        response.location = 'http://localhost:8000/vnc'
        return response(environ, start_response)

    # Not POSTed!
    response = Response(
        'Make sure to reach this page from the MPCAutofill web application!')
    response.status_code = 400
    return response(environ, start_response)
