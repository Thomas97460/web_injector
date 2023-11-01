import json
import visual
import sys
import base64

def encode_base64(html_content):
    try :
        b64 = base64.b64encode(html_content.encode('utf-8')).decode("utf-8")
    except Exception as e :
        print(e)
        sys.exit()
    return b64

def get_keywords(args) : 
    try :
        words = json.loads(args.find)
    except Exception as e :
        print(visual.error("find argument : "+ str(e)))
        sys.exit()
    return words    

def find_response(args, response) :
    retour = {}
    retour["body"] = []
    retour["headers"] = []
    words = get_keywords(args)
    for word in words :
        if word in response.text :
            retour["body"].append(word)
        for key in response.headers :
            if word in key or word in response.headers[key] :
                retour["headers"].append(word)
    return retour

def find_response_base64(args, response) :
    retour = {}
    retour["body"] = []
    retour["headers"] = []
    words = get_keywords(args)
    response_text_base64 = encode_base64(str(response.text))
    for word in words :
        if word in response_text_base64 :
            retour["body"].append(word)
        for key in response.headers :
            if word in key or word in response.headers[key] :
                retour["headers"].append(word)
    return retour