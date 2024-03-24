import os
import logging
import requests
from flask import Flask, request, jsonify



app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.get_json()
    logging.info('Received data: %s', data)

    filename = data.get('file')
    if not filename:
        logging.error("Invalid JSON input: 'file' key is missing.")
        return jsonify(file=None, error="Invalid JSON input."), 400

    file_data = data.get('data')
    if not file_data:
        logging.error("Invalid JSON input: 'data' key is missing.")
        return jsonify(file=None, error="Invalid JSON input."), 400

    file_path = f'/parth_PV_dir/{filename}'
    try:
        with open(file_path, mode='w') as file:
            file.write(file_data)
        logging.info("File stored successfully: %s", file_path)
        return jsonify(file=filename, message="Success.")

    except Exception as err:
        logging.error("Error while storing the file: %s", err)
        return jsonify(file=filename, error=str(err)), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    logging.info('Received data: %s', data)

    filename = data.get('file')
    product = data.get('product', '')
    if not filename:
        logging.error("Invalid JSON input: 'file' key is missing.")
        return jsonify(file=None, error="Invalid JSON input."), 400

    file_path = f'/parth_PV_dir/{filename}'
    if not os.path.isfile(file_path):
        logging.warning("File not found: %s", file_path)
        return jsonify(file=filename, error="File not found."), 404

    try:
        response = requests.post('http://container2.parth-kubes/calculate', json={'file': filename, 'product': product})
        logging.info("Response received from Container 2: %s", response.json())
        return response.json()

    except requests.HTTPError as http_err:
        logging.error("HTTP error occurred: %s", http_err)
        return jsonify(error=str(http_err)), 500

    except requests.RequestException as conn_err:
        logging.error("Request error occurred: %s", conn_err)
        return jsonify(error=str(conn_err)), 500

    except Exception as err:
        logging.error("An unexpected error occurred: %s", err)
        return jsonify(error=str(err)), 500



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=6000)
