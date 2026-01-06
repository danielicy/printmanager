from django.shortcuts import render,HttpResponse
from common.tests import call_mana_api
#from common.functions import AESCipher

def test(reguest):
    call_mana_api()
    return HttpResponse("1", content_type='text/html')

#This URL gets password  and returns the password encrypted
def getpass(reguest, password):
    #h = AESCipher().encrypt(password)
    h=''
    d=''
    #d = AESCipher().decrypt(h)
    return HttpResponse(h + ";" + d, content_type='text/html')