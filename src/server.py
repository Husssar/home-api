# Using flask to make an api
# import necessary libraries and functions
import os.path
from datetime import datetime

from flask import Flask, jsonify, request, render_template
import backend_db_call
from flask_cors import CORS
# creating a Flask app
app = Flask(__name__)
img = os.path.join('static', 'images')
CORS(app)
# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods = ['GET', 'POST'])
def home():
    return jsonify({'welcome': 1337})


@app.route('/home/<int:num>', methods = ['GET'])
def disp(num):
    return jsonify({'data': num**2})


@app.route('/temperature/<int:num>/<value>', methods = ['GET'])
def temperature(num, value):
    temp = backend_db_call.get_temperature(num, value)
    return jsonify({"temperature": temp})

@app.route('/date/', methods= ['GET'])
def get_date():
    now = datetime.now()

    return {
        "now": str(now),
        "now_date_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "now_date_time2": now.strftime("%Y-%m-%d %H:%M"),
        "now_time": now.strftime("%H:%M"),
        "now_time2": now.strftime("%H:%M:%S"),
        "now_date": now.strftime("%Y-%m-%d"),
        "now_date_text": now.strftime("%A %d %B"),
        "now_week": now.strftime("%W")
    }


@app.route('/electricity/graf', methods = ['POST'])
def upload():
    if not os.path.exists('static'):
        print("static folder doesn't exist'")
        os.mkdir('static')
    if not os.path.exists('static/images'):
        print("static/images folder doesn't exist'")
        os.mkdir('static/images')

    f = request.files['file']
    f.save('static/images/' + f.filename)
    print(os.listdir('static/images/'))
    return jsonify({'STATUS': 'File uploaded'})


@app.route('/images')
def show_images():
    file = os.path.join(img, 'test.png')
    print(file)
    return render_template("images.html", image=file)

@app.route('/schedule', methods = ['GET'])
def schedules():
    response = backend_db_call.get_schedule()
    return jsonify(response)


@app.route('/electricity/price', methods = ['GET'])
def electricity():
    response = backend_db_call.get_electricity_price()
    return jsonify(response)

@app.route('/electricity/now', methods = ['GET'])
def price_now():
    response = backend_db_call.get_electricity_price_now()
    return jsonify(response)


@app.route('/electricity/consuming', methods = ['GET'])
def consuming():
    response = backend_db_call.get_electricity_consuming()
    return jsonify(response)

@app.route('/electricity/consumed', methods = ['GET'])
def consumed():
    response = backend_db_call.get_electricity_consumed()
    return jsonify(response)


@app.route('/electricity/added_power', methods = ['GET'])
def added_power():
    response = backend_db_call.get_electricity_added_power()
    return jsonify({"added_power": response})



@app.route('/radiator/', methods=['GET'])
def radiator():
    out_rad = backend_db_call.get_radiator('condenser return')
    in_rad = backend_db_call.get_radiator('heat medium flow')
    pump_speed = backend_db_call.get_radiator('pump speed heating medium')
    return jsonify({"heat_out": out_rad,
                    "heat_in": in_rad,
                    "pump_speed": pump_speed})

@app.route('/citat/', methods=['GET'])
def citat():
    citatet = backend_db_call.get_citat()

    return jsonify({"citat": citatet })


# driver function
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)