from flask import Flask, jsonify, request

from models.schemas import (
    LoginInputSchema,
    GetProductInputSchema,
    CheckTokenValidityInputSchema,
    PostDonationFromScanInputSchema,
    PostDonationFromFridgeInputSchema,
    DeleteMyDonationsInputSchema,
    GetDonationsInputSchema,
    GetDonationsByRegularPathInputSchema,
    GetAllergensInputSchema,
    PostArticlesInFridgeInputSchema,
    DeleteArticlesInFridgeInputSchema,
    GetArticlesInFridgeInputSchema,
    TakeDonationInputSchema,
    GetDonationCodeInputSchema,
    GetFavoriteDonationsInputSchema,
    ToggleDonationInMyFavoriteInputSchema,
    GetMyDonationCodeInputSchema,
    PostRegularPathInputSchema,
    GetRegularPathInputSchema
)

from apiConfig import APIException, InputAPIException, apiResponse

from views.register.login import f as register_login
from views.register.checkTokenValidity import f as register_checkTokenValidity
from views.food.getByBarCode import f as food_getByBarCode
from views.food.postDonationFromScan import f as food_postDonationFromScan
from views.food.postDonationFromFridge import f as food_postDonationFromFridge
from views.food.deleteMyDonations import f as food_deleteMyDonations
from views.food.getDonations import f as food_getDonations
from views.food.getDonationsByRegularPath import f as food_getDonationsByRegularPath
from views.food.getAllergens import f as food_getAllergens
from views.food.postArticlesInFridge import f as food_postArticlesInFridge
from views.food.deleteArticlesInFridge import f as food_deleteArticlesInFridge
from views.food.getArticlesInFridge import f as food_getArticlesInFridge
from views.food.takeDonation import f as food_takeDonation
from views.food.getDonationCode import f as food_getDonationCode
from views.food.getFavoriteDonations import f as food_getFavoriteDonations
from views.food.toggleDonationInMyFavorite import f as food_toggleDonationInMyFavorite
from views.food.getMyDonations import f as food_getMyDonations
from views.user.postRegularPath import f as user_postRegularPath
from views.user.getRegularPath import f as user_getRegularPath

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

@app.route('/food/postDonationFromScan', methods=['POST'])
def postDonationFromScan_endpoint():
    checkInputAPI(PostDonationFromScanInputSchema, request.json)
    data = food_postDonationFromScan(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/postDonationFromFridge', methods=['POST'])
def postDonationFromFridge_endpoint():
    checkInputAPI(PostDonationFromFridgeInputSchema, request.json)
    data = food_postDonationFromFridge(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/deleteArticlesInFridge', methods=['POST'])
def deleteArticlesInFridge_endpoint():
    checkInputAPI(DeleteArticlesInFridgeInputSchema, request.json)
    data = food_deleteArticlesInFridge(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/deleteMyDonations', methods=['POST'])
def deleteMyDonations_endpoint():
    checkInputAPI(DeleteMyDonationsInputSchema, request.json)
    data = food_deleteMyDonations(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/getDonations', methods=['GET'])
def getDonations_endpoint():
    checkInputAPI(GetDonationsInputSchema, request.args)
    data = food_getDonations(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/getDonationsByRegularPath', methods=['GET'])
def getDonationsByRegularPath_endpoint():
    checkInputAPI(GetDonationsByRegularPathInputSchema, request.args)
    data = food_getDonationsByRegularPath(request)
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

@app.route('/food/takeDonation', methods=['POST'])
def takeDonation_endpoint():
    checkInputAPI(TakeDonationInputSchema, request.json)
    data = food_takeDonation(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/getDonationCode', methods=['GET'])
def getDonationCode_endpoint():
    checkInputAPI(GetDonationCodeInputSchema, request.args)
    data = food_getDonationCode(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/getFavoriteDonations', methods=['GET'])
def getFavoriteDonations_endpoint():
    checkInputAPI(GetFavoriteDonationsInputSchema, request.args)
    data = food_getFavoriteDonations(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/toggleDonationInMyFavorite', methods=['POST'])
def toggleDonationInMyFavorite_endpoint():
    checkInputAPI(ToggleDonationInMyFavoriteInputSchema, request.json)
    data = food_toggleDonationInMyFavorite(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/getMyDonations', methods=['GET'])
def getMyDonations_endpoint():
    checkInputAPI(GetMyDonationCodeInputSchema, request.args)
    data = food_getMyDonations(request)
    return jsonify(apiResponse(request, data))
    
@app.route('/user/postRegularPath', methods=['POST'])
def postRegularPath_endpoint():
    checkInputAPI(PostRegularPathInputSchema, request.json)
    data = user_postRegularPath(request)
    return jsonify(apiResponse(request, data))

@app.route('/user/getRegularPath', methods=['GET'])
def getRegularPath_endpoint():
    checkInputAPI(GetRegularPathInputSchema, request.args)
    data = user_getRegularPath(request)
    return jsonify(apiResponse(request, data))

if __name__ == '__main__':
    #app.run(debug=True, host = "0.0.0.0")
    app.run(debug=True, host = "0.0.0.0", ssl_context='adhoc')

