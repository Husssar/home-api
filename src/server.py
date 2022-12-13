# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request, render_template
import backend_db_call
from flask_cors import CORS
# creating a Flask app
app = Flask(__name__)
CORS(app)
# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('index.html')

# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)


@app.route('/home/<int:num>', methods = ['GET'])
def disp(num):
    return jsonify({'data': num**2})


@app.route('/temperature/<int:num>/<value>', methods = ['GET'])
def temperature(num, value):
    temp = backend_db_call.get_temperature(num, value)
    return jsonify({"temperature": temp})


@app.route('/electricity/price', methods = ['GET'])
def electricity():
    response = backend_db_call.get_electricity_price()
    return jsonify({"price": response})


@app.route('/electricity/consuming/', methods = ['GET'])
def consuming():
    response = backend_db_call.get_electricity_consuming()
    return jsonify({"consuming": response})


@app.route('/electricity/added_power/', methods = ['GET'])
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