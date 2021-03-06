from flask import Flask
from flask import render_template
import logging
import io
import random
from os.path import dirname, realpath, join, abspath
from flask import Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import hydrogeol_utils
import subprocess


logger = logging.getLogger(__name__)
APP_DIR = dirname(dirname(realpath(__file__)))
LOGFILE = APP_DIR + '/flask.log'
TEMPLATES_DIR = join(dirname(abspath(__file__)), 'view', 'templates')
BASE_URL = "http://ec2-13-211-162-222.ap-southeast-2.compute.amazonaws.com"
STATIC_DIR = join(dirname(abspath(__file__)), 'view', 'static')

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
print(TEMPLATES_DIR)
@app.route('/')
def home_page():
    return render_template('home_page.html', BASE_URL=BASE_URL)


@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


@app.route('/doathing')
def test_conn():
    print(TEMPLATES_DIR)
    print(APP_DIR)
    return render_template('hello.html', test=hydrogeol_utils.__name__)

@app.route('/jupyter')
def trigger_jupyter_notebooks():
    result = subprocess.run('./home/ubuntu/run_j.sh', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #result = subprocess.run('jupyter notebook', stdout=subprocess.PIPE)
    processed_result = result.stdout
    return render_template('hello.html', test=processed_result, test2=result, decode=result.stdout.decode()
                           )
#@app.route(':8888')
#def test_conn():
  # print(TEMPLATES_DIR)
    #print(APP_DIR)
    #return render_template('hello.html', test=hydrogeol_utils.__name__)

@app.route('/hello')
def hello():
    if request.method == 'GET':
        return Response(hydrogeol_utils.__name__)
        #return render_template('templates/result.html', test=hydrogeol_utils.__name__)
    elif request.method =="POST":
        logging.debug('request.form = {}'.format(request.form))
        return render_template('view/templates/result.html', test=hydrogeol_utils.__name__)


# run the Flask app
if __name__ == '__main__':
    logging.basicConfig(filename=LOGFILE,
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s')

    app.run(debug=True, threaded=True)
