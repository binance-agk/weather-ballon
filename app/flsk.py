from os import path
from flask import Flask
from flask import request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from solution.downlaodapi import Dl
from solution.solution import Solution

app = Flask(__name__, static_url_path='')
CORS(app)
app.config['SECRET_KEY'] = 'secret1!'
socketio = SocketIO(app)
print(socketio)


@socketio.on('connect')
def e():
    print("hey connect in flask here")
    emit('after connect', {'data': 'Lets fuck'})


@socketio.on('my event')
def llp(message):
    print("hey connect in flask here", message)
    emit('my event', {'data': 'Lets dance'})


@socketio.on('after connect')
def afterconnect(message):
    print("hey connect in flask here")
    emit('my event', {'data': 'Lets dance'})


@socketio.on('dlevent')
def ll(message):
    def progressEmitter(msg): return emit('progressEmitter', {'data': msg})

    def errorEmitter(msg): return emit('errorEmitter', {'data': msg})

    def doneEmitter(msg): return emit('doneEmitter', {'data': msg})

    print('ll message: ', message)
    date = message['data']
    Dl(date['year'], date['month'], date['day'], date['hour']) \
        .dl(progressEmitter=progressEmitter, errorEmitter=errorEmitter, doneEmitter=doneEmitter)


@socketio.on('simulate')
def simulate(message):
    def anyerroremmiter(msg):
        return emit('anyerroremmiter', {'data': msg})

    def balloonEmitter(msg):
        return emit('balloonEmitter', {'data': msg})

    def parachuteEmitter(msg):
        return emit('parachuteEmitter', {'data': msg})

    def flightdoneemmitee(msg):
        return emit('flightdoneemmiter', {'data': msg})

    print('king message: ', message)
    spec = message['data']['spec']
    date = message['data']['date']
    blntype = spec['balloonType']
    lat = float(spec['lat'])
    lon = float(spec['lon'])
    nozzlelift = float(spec['nozzlelift'])
    chutetype = spec['chutetype']
    gasType = spec['gasType']
    payloadweight = float(spec['payloadweight'])
    if gasType == 'Helium':
        gasType = 1
    else:
        gasType = 0
    filename = "data/GFS_Global_0p5deg_ana_{0}{1}{2}_{3}00.grib2.nc" \
        .format(date['year'], date['month'], date['day'], date['hour'])

    sol = Solution(anyerroremmiter, balloonEmitter, parachuteEmitter, flightdoneemmitee, lat, lon, date['day'],
                   date['month'], date['year'], date['hour'],
                   0, filename, gasType, blntype, payloadweight, chutetype, nozzlelift, 22000, 15000)

    sol.solveballoonpart()
    sol.solveparachutepart()
    sol.exportKML()


@app.route("/2", methods=['GET', 'POST'])
def helloWorld():
    print(request.form)
    flightInfo_dateandtime = (request.form['flightInfo_dateandtime'])
    gasType = (request.form['gasType'])
    balloonType = (request.form['flightInfo_balloonweight'])
    payloadweight = (request.form['flightInfo_payloadweight'])
    chutetype = (request.form['flightInfo_chutetype'])
    nozzlelift = (request.form['flightInfo_nozzlelift'])
    lon = (request.form['launchSite_lon'])
    lat = (request.form['launchSite_lat'])

    (flightInfo_date, flightInfo_time) = flightInfo_dateandtime.split(' ')
    print(flightInfo_date, flightInfo_time)

    (day, month, year) = flightInfo_date.split("/")

    (hour, mins) = flightInfo_time.split(":")
    hour = int(hour)
    hrstr = ['00', '06', '12', '18']
    relhrs = [abs(0 - hour), abs(6 - hour), abs(12 - hour), abs(18 - hour)]
    mymin = min(relhrs)
    min_positions = [i for i, x in enumerate(relhrs) if x == mymin][0]
    print(min_positions)
    hour = hrstr[min_positions]

    filename = "GFS_Global_0p5deg_ana_{0}{1}{2}_{3}00.grib2.nc".format(year, month, day, hour)
    print(filename)

    if path.exists("data/" + filename):
        print('exists')
        return {'status': 'ok', 'description': 'file exists',
                'date': {'year': year, 'month': month, 'day': day, 'hour': hour},
                'spec': {'lat': lat, 'lon': lon, 'gasType': gasType, 'balloonType': balloonType,
                         'nozzlelift': nozzlelift, 'payloadweight': payloadweight, 'chutetype': chutetype}
                }
    else:
        return {'status': '9999', 'description': 'file not exists,start request download',
                'date': {'year': year, 'month': month, 'day': day, 'hour': hour}}

    print((day, month, year))

    return "Hello, cross-origin-world!"


@app.route("/l", methods=['GET'])
def dl():
    print(request.form)
    flightInfo_dateandtime = (request.form['flightInfo_dateandtime'])

    (flightInfo_date, flightInfo_time) = flightInfo_dateandtime.split(' ')
    print(flightInfo_date, flightInfo_time)

    (day, month, year) = flightInfo_date.split("/")

    (hour, mins) = flightInfo_time.split(":")
    hour = int(hour)
    hrs = [0, 6, 12, 18]
    hrstr = ['00', '06', '12', '18']
    relhrs = [abs(0 - hour), abs(6 - hour), abs(12 - hour), abs(18 - hour)]
    mymin = min(relhrs)
    min_positions = [i for i, x in enumerate(relhrs) if x == mymin][0]
    print(min_positions)
    hour = hrstr[min_positions]

    filename = "GFS_Global_0p5deg_ana_{0}{1}{2}_{3}00.grib2.nc".format(year, month, day, hour)
    print(filename)

    if path.exists("solution/" + filename):
        print('exists')
        return {'status': 'ok', 'description': 'file exists'}
    else:
        return ''


@app.route('/')
def root():
    print("here ")
    return send_from_directory('', 'index.html')


@app.route('/img/<path:path>')
def send_js1(path):
    return send_from_directory('img', path)


@app.route('/css/<path:path>')
def send_js11(path):
    return send_from_directory('css', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/favicon.ico')
def send_icon():
    return send_from_directory('', 'favicon.ico')


@app.route('/lmk.kml')
def send_kml():
    return send_from_directory('', 'lmk.kml', cache_timeout=0)


@app.route('/manifest.json')
def manifes():
    return send_from_directory('', 'manifest.json', cache_timeout=0)
