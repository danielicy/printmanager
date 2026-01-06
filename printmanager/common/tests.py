from django.test import TestCase
#from common.functions import bvp_api_create_content,bvp_api_update_content





def call_mana_api():
    values = { "request" : {"UnitId" : "1234" , "Content" : {"ID":"1","Name":"2","requestId":"XXX","Status":2,"Files":[{"FileID":"1234"}] } }}

 
    #result = bvp_api_create_content(values)
    #bvp_api_update_content(values)
    result = ''
    return result
