from flask import Flask, jsonify
from route import route
from facades.apiConfig import APIException

app = Flask(__name__)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.response())
    response.status_code = error.status_code
    return response

route(app)

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", ssl_context='adhoc')