from nogaspi.views.user.generateRegularPath import generateRegularPath
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest

def test_user_generateRegularPath():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `lastPathType`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0', NULL, NULL, NULL, NULL, NULL, NULL);"]
    sqlQuerysWithCommit(querys)

    latitudeStart = 44.5
    longitudeStart = 1.5
    latitudeEnd = 44.6
    longitudeEnd = 1.6
    
    funcRtr = generateRegularPath(FakeRequest({
        "token":"token_toto",
        "latitudeStart": latitudeStart,
        "longitudeStart": longitudeStart,
        "latitudeEnd": latitudeEnd,
        "longitudeEnd": longitudeEnd,
        "pathType": "car"
    }))

    assert funcRtr['isPosted']
    assert funcRtr['regularPath']['latitudeStart'] == latitudeStart
    assert funcRtr['regularPath']['longitudeStart'] == longitudeStart
    assert funcRtr['regularPath']['latitudeEnd'] == latitudeEnd
    assert funcRtr['regularPath']['longitudeEnd'] == longitudeEnd
    assert funcRtr['regularPath']['latitudeStart'] == sqlSelect(table='userNogaspi', conditions="WHERE id = 1")[0]['regularPathLatitudeStart']
    assert funcRtr['regularPath']['longitudeStart'] == sqlSelect(table='userNogaspi', conditions="WHERE id = 1")[0]['regularPathLongitudeStart']
    assert funcRtr['regularPath']['latitudeEnd'] == sqlSelect(table='userNogaspi', conditions="WHERE id = 1")[0]['regularPathLatitudeEnd']
    assert funcRtr['regularPath']['longitudeEnd'] == sqlSelect(table='userNogaspi', conditions="WHERE id = 1")[0]['regularPathLongitudeEnd']
    assert funcRtr['regularPath']['pathPoints'] == sqlSelect(table='userNogaspi', conditions="WHERE id = 1")[0]['regularPathPoints']
    assert funcRtr['regularPath']['pathType'] == sqlSelect(table='userNogaspi', conditions="WHERE id = 1")[0]['lastPathType']
    assert funcRtr['regularPath']['pathType'] == "car"