from flask import Flask, jsonify, request

from models.schemas import LoginInputSchema, GetProductInputSchema, CheckTokenValidityInputSchema, PostDonationInputSchema, GetDonationsInputSchema, GetAllergensInputSchema, PostArticlesInFridgeInputSchema, GetArticlesInFridgeInputSchema
from apiConfig import APIException, InputAPIException, apiResponse

from views.register.login import f as register_login
from views.register.checkTokenValidity import f as register_checkTokenValidity
from views.food.getByBarCode import f as food_getByBarCode
from views.food.postDonation import f as food_postDonation
from views.food.getDonations import f as food_getDonations
from views.food.getAllergens import f as food_getAllergens
from views.food.postArticlesInFridge import f as food_postArticlesInFridge
from views.food.getArticlesInFridge import f as food_getArticlesInFridge

app = Flask(__name__)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.response())
    response.status_code = error.status_code
    return response

def checkInputAPI(Schema, args):
    try:
        Schema().load(args)
    except Exception as e:
        raise InputAPIException(str(e), str(e), request)


@app.route('/test', methods=['GET'])
def test():
    data = {"toto":  ["tata", "titi"]}
    return jsonify(apiResponse(request, data))


@app.route('/register/login', methods=['POST'])
def login_endpoint():
    checkInputAPI(LoginInputSchema, request.json)
    data = register_login(request)
    return jsonify(apiResponse(request, data))

@app.route('/register/checkTokenValidity', methods=['GET'])
def checkTokenValidity_endpoint():
    checkInputAPI(CheckTokenValidityInputSchema, request.args)
    data = register_checkTokenValidity(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/getProduct', methods=['GET'])
def getProduct_endpoint():
    checkInputAPI(GetProductInputSchema, request.args)
    data = food_getByBarCode(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/postDonation', methods=['POST'])
def postDonation_endpoint():
    checkInputAPI(PostDonationInputSchema, request.json)
    data = food_postDonation(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/getDonations', methods=['GET'])
def getDonations_endpoint():
    checkInputAPI(GetDonationsInputSchema, request.args)
    data = food_getDonations(request)
    return jsonify(apiResponse(request, data))
    
@app.route('/food/getAllergens', methods=['GET'])
def getAllergens_endpoint():
    checkInputAPI(GetAllergensInputSchema, request.args)
    data = food_getAllergens(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/postArticlesInFridge', methods=['POST'])
def postArticlesInFridge_endpoint():
    checkInputAPI(PostArticlesInFridgeInputSchema, request.json)
    data = food_postArticlesInFridge(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/getArticlesInFridge', methods=['GET'])
def getArticlesInFridge_endpoint():
    checkInputAPI(GetArticlesInFridgeInputSchema, request.args)
    data = food_getArticlesInFridge(request)
    return jsonify(apiResponse(request, data))

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0")
    #app.run(debug=True, host = "0.0.0.0", ssl_context='adhoc')

