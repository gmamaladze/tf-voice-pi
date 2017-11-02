from bottle import route, run, template
from bottle import static_file
from bottle import get, post, put, request
import time
import os

isRaspberryPi = ( os.uname()[4][:3] == 'arm' )
print(isRaspberryPi)

if isRaspberryPi:
    import robot
else:
    import robot_mock as robot

@get('/<filepath:path>')
@get('/')
def server_static(filepath = 'index.html'):
    return static_file(filepath, root='./static/')

@put('/forward')
def server_static():
    print("FWD")
    r = robot.Robot()
    r.forward

@put('/backward')
def server_static():
    print("BWD")
    r = robot.Robot()
    r.backward()

@put('/left')
def server_static():
    print("LEFT")
    r = robot.Robot()
    r.left()

@put('/right')
def server_static():
    print("RIGHT")
    r = robot.Robot()
    r.right()

@put('/stop')
def server_static():
    print("STOP")
    r = robot.Robot()
    r.stop()


try:
    run(host='0.0.0.0', port=80)
except PermissionError:
    print("Warning: Need sudo to listen on 0.0.0.0")
    run(host='localhost', port=8080)
