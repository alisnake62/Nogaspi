from . import InputAPIException

def checkInputAPI(Schema, request):

    args=request.args if request.method == "GET" else request.json
    try:
        Schema().load(args)
    except Exception as e:
        raise InputAPIException(str(e), str(e), request)

def getArgs(request, args):
    if request.method == "GET":
        return (request.args.get(arg) for arg in args) if len(args) > 1 else request.args.get(args[0])
    else:
        return (request.json[arg] for arg in args) if len(args) > 1 else request.json[args[0]]