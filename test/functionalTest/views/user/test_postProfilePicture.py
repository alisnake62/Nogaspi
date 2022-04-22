from nogaspi.views.user.postProfilePicture import postProfilePicture
from test.functionalTest.dbMagement import sqlQuerysWithCommit
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_user_postProfilePicture():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0', NULL, NULL, NULL, NULL, NULL);"]
    sqlQuerysWithCommit(querys)

    # from werkzeug.utils import secure_filename
    # request = FakeRequest({"token":"token_toto"}, file=True)
    # f = request.files['toto']
    # f.save(secure_filename('titi.jpg'))


    funcRtr = postProfilePicture(FakeRequest({"token":"token_toto"}, file='img.jpg', keyFile='profilePicture'))


    assert type(funcRtr) == dict