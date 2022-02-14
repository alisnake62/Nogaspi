from flask import jsonify, request, send_file
from facades.apiConfig import getArgs
from models.schemas import *
from views import *
from facades.apiConfig import apiResponse, checkInputAPI

def route(app):
    @app.route('/test', methods=['GET'])
    def test():
        data = {"toto":  ["tata", "tito"]}
        return jsonify(apiResponse(request, data))

    @app.route('/tools/getProfilePicture', methods=['GET'])
    def getProfilePicture_endpoint():
        checkInputAPI(GetProfilePictureInputSchema, request)
        filename = tools_getProfilePicture(request)["picturePath"]
        return send_file(filename, mimetype='image/jpg')

    @app.route('/register/login', methods=['POST'])
    def login_endpoint():
        checkInputAPI(LoginInputSchema, request)
        data = register_login(request)
        return jsonify(apiResponse(request, data))

    @app.route('/register/logout', methods=['POST'])
    def logout_endpoint():
        checkInputAPI(LogoutInputSchema, request)
        data = register_logout(request)
        return jsonify(apiResponse(request, data))

    @app.route('/register/checkTokenValidity', methods=['GET'])
    def checkTokenValidity_endpoint():
        checkInputAPI(CheckTokenValidityInputSchema, request)
        data = register_checkTokenValidity(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/getProduct', methods=['GET'])
    def getProduct_endpoint():
        checkInputAPI(GetProductInputSchema, request)
        data = food_getByBarCode(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/postDonationFromScan', methods=['POST'])
    def postDonationFromScan_endpoint():
        checkInputAPI(PostDonationFromScanInputSchema, request)
        data = food_postDonationFromScan(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/postDonationFromFridge', methods=['POST'])
    def postDonationFromFridge_endpoint():
        checkInputAPI(PostDonationFromFridgeInputSchema, request)
        data = food_postDonationFromFridge(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/deleteArticlesInFridge', methods=['POST'])
    def deleteArticlesInFridge_endpoint():
        checkInputAPI(DeleteArticlesInFridgeInputSchema, request)
        data = food_deleteArticlesInFridge(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/deleteMyDonations', methods=['POST'])
    def deleteMyDonations_endpoint():
        checkInputAPI(DeleteMyDonationsInputSchema, request)
        data = food_deleteMyDonations(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/getDonations', methods=['GET'])
    def getDonations_endpoint():
        checkInputAPI(GetDonationsInputSchema, request)
        data = food_getDonations(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/getDonationById', methods=['GET'])
    def getDonationById_endpoint():
        checkInputAPI(GetDonationByIdInputSchema, request)
        data = food_getDonationById(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/getDonationsByRegularPath', methods=['GET'])
    def getDonationsByRegularPath_endpoint():
        checkInputAPI(GetDonationsByRegularPathInputSchema, request)
        data = food_getDonationsByRegularPath(request)
        return jsonify(apiResponse(request, data))
        
        
    @app.route('/food/getAllergens', methods=['GET'])
    def getAllergens_endpoint():
        checkInputAPI(GetAllergensInputSchema, request)
        data = food_getAllergens(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/postArticlesInFridge', methods=['POST'])
    def postArticlesInFridge_endpoint():
        checkInputAPI(PostArticlesInFridgeInputSchema, request)
        data = food_postArticlesInFridge(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/getArticlesInFridge', methods=['GET'])
    def getArticlesInFridge_endpoint():
        checkInputAPI(GetArticlesInFridgeInputSchema, request)
        data = food_getArticlesInFridge(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/takeDonations', methods=['POST'])
    def takeDonations_endpoint():
        checkInputAPI(TakeDonationsInputSchema, request)
        data = food_takeDonations(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/generateDonationsCode', methods=['POST'])
    def generateDonationsCode_endpoint():
        checkInputAPI(GenerateDonationsCodeInputSchema, request)
        data = food_generateDonationsCode(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/getFavoriteDonations', methods=['GET'])
    def getFavoriteDonations_endpoint():
        checkInputAPI(GetFavoriteDonationsInputSchema, request)
        data = food_getFavoriteDonations(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/toggleDonationInMyFavorite', methods=['POST'])
    def toggleDonationInMyFavorite_endpoint():
        checkInputAPI(ToggleDonationInMyFavoriteInputSchema, request)
        data = food_toggleDonationInMyFavorite(request)
        return jsonify(apiResponse(request, data))

    @app.route('/food/getMyDonations', methods=['GET'])
    def getMyDonations_endpoint():
        checkInputAPI(GetMyDonationsInputSchema, request)
        data = food_getMyDonations(request)
        return jsonify(apiResponse(request, data))
        
    @app.route('/user/postRegularPath', methods=['POST'])
    def postRegularPath_endpoint():
        checkInputAPI(PostRegularPathInputSchema, request)
        data = user_postRegularPath(request)
        return jsonify(apiResponse(request, data))

    @app.route('/user/getRegularPath', methods=['GET'])
    def getRegularPath_endpoint():
        checkInputAPI(GetRegularPathInputSchema, request)
        data = user_getRegularPath(request)
        return jsonify(apiResponse(request, data))

    @app.route('/user/postFireBaseToken', methods=['POST'])
    def postFireBaseToken_endpoint():
        checkInputAPI(PostFireBaseTokenInputSchema, request)
        data = user_postFireBaseToken(request)
        return jsonify(apiResponse(request, data))

    @app.route('/messaging/initiateConversation', methods=['POST'])
    def initiateConversation_endpoint():
        checkInputAPI(InitiateConversationInputSchema, request)
        data = messaging_initiateConversation(request)
        return jsonify(apiResponse(request, data))

    @app.route('/messaging/acknowledgeMessagesOnConversation', methods=['POST'])
    def acknowledgeMessagesOnConversation_endpoint():
        checkInputAPI(AcknowledgeMessagesOnConversationInputSchema, request)
        data = messaging_acknowledgeMessagesOnConversation(request)
        return jsonify(apiResponse(request, data))

    @app.route('/messaging/postMessage', methods=['POST'])
    def postMessage_endpoint():
        checkInputAPI(PostMessageInputSchema, request)
        data = messaging_postMessage(request)
        return jsonify(apiResponse(request, data))
        
    @app.route('/messaging/getMyConversations', methods=['GET'])
    def getMyConversations_endpoint():
        checkInputAPI(GetMyConversationsInputSchema, request)
        data = messaging_getMyConversations(request)
        return jsonify(apiResponse(request, data))

    @app.route('/messaging/getConversation', methods=['GET'])
    def getConversation_endpoint():
        checkInputAPI(GetConversationInputSchema, request)
        data = messaging_getConversation(request)
        return jsonify(apiResponse(request, data))

    @app.route('/messaging/getConversationsByDonation', methods=['GET'])
    def getConversationsByDonation_endpoint():
        checkInputAPI(GetConversationsByDonationInputSchema, request)
        data = messaging_getConversationsByDonation(request)
        return jsonify(apiResponse(request, data))