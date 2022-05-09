from . import InputAPIException

def checkInputAPI(Schema, request):
    
    if len(request.form): args = request.form
    elif(request.method == "GET"): args=request.args
    else: args = request.json
    
    try:
        Schema().load(args)
    except Exception as e:
        raise InputAPIException(str(e), str(e), request)

def checkInputFileAPI(Schema, request):
    
    try:
        Schema().load(request.files)
    except Exception as e:
        raise InputAPIException(str(e), str(e), request)

def getArgs(request, args):
    if len(request.form):
        return (request.form.get(arg) for arg in args) if len(args) > 1 else request.form.get(args[0])
    if request.method == "GET":
        return (request.args.get(arg) for arg in args) if len(args) > 1 else request.args.get(args[0])
    
    return (request.json[arg] for arg in args) if len(args) > 1 else request.json[args[0]]

def getFiles(request, files):
    return (request.files.get(file) for file in files) if len(files) > 1 else request.files.get(files[0])