from flask import Flask, jsonify, request

from models.schemas import LoginInputSchema, GetArticleInputSchema, CheckTokenValidityInputSchema, PostDonationWithBarCodeInputSchema, GetDonationsInputSchema
from apiConfig import APIException, InputAPIException, apiResponse

from views.register.login import f as register_login
from views.register.checkTokenValidity import f as register_checkTokenValidity
from views.food.getByBarCode import f as food_getByBarCode
from views.food.postDonationWithBarCode import f as food_postDonationWithBarCode
from views.food.getDonations import f as food_getDonations

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
        message = ", ".join([str(k) + " : " + " ".join(v) for k,v in e.messages.items()])
        raise InputAPIException(message, str(e), request)


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


@app.route('/food/getArticle', methods=['GET'])
def getArticle_endpoint():
    checkInputAPI(GetArticleInputSchema, request.args)
    data = food_getByBarCode(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/postDonationWithBarCode', methods=['POST'])
def postDonationWithBarCode_endpoint():
    checkInputAPI(PostDonationWithBarCodeInputSchema, request.json)
    data = food_postDonationWithBarCode(request)
    return jsonify(apiResponse(request, data))

@app.route('/food/getDonations', methods=['GET'])
def getDonations_endpoint():
    checkInputAPI(GetDonationsInputSchema, request.args)
    data = food_getDonations(request)
    return jsonify(apiResponse(request, data))
    


context = ('../cert.pem', '../key.pem')
if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0")
    #app.run(debug=True, host = "0.0.0.0", ssl_context=context)

