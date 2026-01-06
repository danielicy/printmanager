from django.shortcuts import render,get_object_or_404,HttpResponse
from watcher.wrapper import process
from datetime import datetime

# Create your views here.
def test(request):

    t=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        process(t)
    except Exception as e :
        return HttpResponse("Error: "+ str(e)  , content_type='text/html')
    else :
        return HttpResponse("OK", content_type='text/html')