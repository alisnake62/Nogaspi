from flask import Flask, jsonify, request

from models.schemas import LoginInputShema, GetArticleInputShema
from apiConfig import APIException, InputAPIException, apiResponse

from views.register.login import f as register_login
from views.food.getByBarCode import f as food_getByBarCode
app = Flask(__name__)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.response())
    response.status_code = error.status_code
    return response

def checkInputAPI(Schema, request):
    try:
        Schema().load(request.json)
    except Exception as e:
        raise InputAPIException(str(e), str(e), request)





@app.route('/test', methods=['GET'])
def test():
    data = {"toto":  ["tata", "titi"]}
    return jsonify(apiResponse(request, data))


@app.route('/register/login', methods=['POST'])
def login_endpoint():
    checkInputAPI(LoginInputShema, request)
    data = register_login(request)
    return jsonify(apiResponse(request, data))


@app.route('/food/getArticle', methods=['GET'])
def getArticle_endpoint():
    checkInputAPI(GetArticleInputShema, request)
    data = food_getByBarCode(request)
    return jsonify(apiResponse(request, data))
    

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0")

