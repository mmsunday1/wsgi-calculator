import os
import logging
"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home pa,ge (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!
"""


def add(args):
    """ Returns a STRING with the sum of the arguments """
    sum = int(args[0]) + int(args[1])
    body = "<h1>{}</h1>"
    return body.format(str(sum))


def multiply(args):
    """ Returns a STRING with the multiplication of the arguments """
    mult = int(args[0]) * int(args[1])
    body = "<h1>{}</h1>"
    return body.format(str(mult))


def divide(args):
    """ Returns a STRING with the division of the arguments """
    div = int(args[0]) / int(args[1])
    body = "<h1>{}</h1>"
    return body.format(str(int(div)))


def subtract(args):
    """ Returns a STRING with the subtraction the arguments """
    sub = int(args[0]) - int(args[1])
    body = "<h1>{}</h1>"
    return body.format(str(sub))


def home(args):
    page = """
<h1>Instructions on using this calculator</h1>
<table>
    <tr><th>Addition:</th><td>append the following text after the localhost
    url: /add/X/Y to add values X and Y (example: 
    http://localhost:8080/add/5/7 results in 12)</td></tr><p>  </p>
    <tr><th>Multiplication:</th><td>append the following text after the
    localhost url: /multiply/X/Y to multiply values X and Y (example: 
    http://localhost:8080/multiply/5/7 results in 35)</td></tr><p></p>
    <tr><th>Division:</th><td>append the following text after the localhost
    url: /divide/X/Y to divide value X by Y (example: 
    http://localhost:8080/divide/35/7 results in 5)</td></tr><p></p>
    <tr><th>Subtraction:</th><td>append the following text after the
localhostcurl: /subtract/X/Y to subtract value Y from X (example: 
    http://localhost:8080/subtract/35/7 results in 28)</td></tr>
</table>
"""
    return page


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    function_dict = {
        '': home,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide}

    path = path.strip("/").split("/")
    function = path[0]
    args = path[1:]

    try:
        func = function_dict[function]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1> Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
