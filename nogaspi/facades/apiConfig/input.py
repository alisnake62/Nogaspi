from . import InputAPIException

def checkInputAPI(Schema, request):

    test = request
    
    args=request.args if request.method == "GET" else request.json
    try:
        Schema().load(args)
    except Exception as e:
        raise InputAPIException(str(e), str(e), request)

def checkInputFileAPI(Schema, request):

    test = request
    #test2 = request.files.filename
    
    try:
        Schema().load(request.files)
    except Exception as e:
        raise InputAPIException(str(e), str(e), request)

def getArgs(request, args):
    if request.method == "GET":
        return (request.args.get(arg) for arg in args) if len(args) > 1 else request.args.get(args[0])
    else:
        return (request.json[arg] for arg in args) if len(args) > 1 else request.json[args[0]]

def getFiles(request, files):
    return (request.files.get(file) for file in files) if len(files) > 1 else request.files.get(files[0])