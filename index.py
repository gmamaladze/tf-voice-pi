from bottle import route, run, template
from bottle import static_file
from bottle import get, post, request
import time
import motors

@get('/<filepath:path>')
@get('/')
def server_static(filepath = 'index.html'):
    return static_file(filepath, root='./static/')

@post('/<motor>')
def server_static(motor):
    m = motors.Motor(motor,1)
    m.forward()
    time.sleep(2)
    m.stop()
    return



@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)
