import analyzer
import arg_parser
import requestor
import visual
import sys
import time
import datetime
import json
import urllib.parse

def get_wordlist_list(args) : #Récupère la wordlist dans le fichier et la renvoie sous forme de list python
    try :
        with open(args.wordlist, "r") as file :
            words = [word.rstrip('\n') for word in file.readlines()]
            return words
    except Exception as e:
        print(visual.error(str(e)))
        sys.exit()

def get_nb_to_found(args) : 
    try : 
        to_found = json.loads(args.find)
    except Exception as e :
        print(visual.error("find argument need to be a json list"))
        sys.exit()
    return len(to_found)

def print_found(args, found) :
    number = get_nb_to_found(args)#comptage du nombre de keywords à trouver pour embellir l'affichage en cas de 1
    if number == 1  :
        if len(found["body"]) == 1 :
            print("\t Found in " + visual.green("Body"), end=" ")
        if len(found["headers"]) == 1 :
            print("\t Found in " + visual.green("Headers"), end=" ")
    else :
        if len(found["body"]) > 0 :
            to_print = ""
            for i in range(0, len(found["body"])) :
                if i < len(found["body"]) - 1 :
                    to_print+=visual.green(found["body"][i]) + " | "
                else :
                    to_print+=visual.green(found["body"][i])
            print("\t Found in Body : " + to_print, end=" ")
        if len(found["headers"]) > 0 :
            to_print = ""
            for i in range(0, len(found["headers"])) :
                if i < len(found["headers"]) - 1 :
                    to_print+=visual.green(found["headers"][i]) + " | "
                else :
                    to_print+=visual.green(found["headers"][i])[i]
            print("\t Found in Headers : " + to_print, end=" ") 


def print_request_data_injection(args, found, response, word) : #Affiche le retour d'une requête et cherche les mots-clés dans le cas d'une data_injection
    heure_actuelle = datetime.datetime.now().time()
    if response.status_code >= 400 :
        print("[" + visual.blue(heure_actuelle.strftime('%H:%M:%S'))+"]" + "[" + visual.red(str(response.status_code)) + "] : " + word, end=" ")
    if response.status_code < 400 :
        print("[" + visual.blue(heure_actuelle.strftime('%H:%M:%S'))+"]" + "[" + visual.green(str(response.status_code)) + "] " + word, end=" ")
    if args.find is not None :
        print_found(args, found)
    print()

def print_request_url_injection(args, found, url, response) : #Affiche le retour d'une requête et cherche les mots-clés dans le cas d'une url_injection
    heure_actuelle = datetime.datetime.now().time()
    if response.status_code >= 400 :
        print("[" + visual.blue(heure_actuelle.strftime('%H:%M:%S'))+"]" + "[" + visual.red(str(response.status_code)) + "] : " + url, end=" ")
    if response.status_code < 400 :
        print("[" + visual.blue(heure_actuelle.strftime('%H:%M:%S'))+"]" + "[" + visual.green(str(response.status_code)) + "] " + url, end=" ")
    if args.find is not None :
        print_found(args, found)
    print()

def concat_output(args, url, response, to_dump) : #Concatène la réponse dans le dictionnaire python to_dump
    new = {args.param:response.text}
    to_dump.update(new)
    return to_dump

def add_param_data(args, word) : #ajoute le mot dans args.data
    new = {args.param:word}
    if args.data is None :
        new = json.dumps(new)
        args.data = new
    else :
        try :
            data = json.loads(args.data)
            data.update(new)
            args.data = json.dumps(data)
        except Exception as e :
            print(visual.error(e))
    return args.data

def found_keyword(args, response) :
    if args.find is not None :
        if args.base64 :
            found = analyzer.find_response_base64(args, response)
        else :
            found = analyzer.find_response(args, response)
    else :
        found = None
    return found

def data_injection(args) : # Performe l'injection POST
    words = get_wordlist_list(args)
    to_dump = {}
    while(len(words)>0) :
        word = words.pop(0)
        args.data = add_param_data(args, word)
        response = requestor.send(args, args.url)
        found = found_keyword(args, response)
        if args.silent is not None :
            print_request_data_injection(args, found, response, word)
        to_dump[word] = response.text
        if args.slow is not None :
            time.sleep(float(args.slow))
    return to_dump

def prepare_url(args, origin, param, word) : #Ajoute le paramètre à la fin de l'url
    if args.encode :
        word_url = urllib.parse.quote(word)
    else :
        word_url = word
    if "?" in origin :
        origin = origin+"&"+param+"="+word_url
    else :
        origin = origin+"?"+param+"="+word_url
    return origin

def url_injection(args) : #Performe l'injection d'URL
    words = get_wordlist_list(args)
    to_dump = {}
    while(len(words)>0) :
        word = words.pop(0)
        current_url = prepare_url(args, args.url, args.param, word)
        response = requestor.send(args, current_url)
        found = found_keyword(args, response)
        if args.silent is not None :
            print_request_url_injection(args, found, current_url, response)
        to_dump[word] = response.text
        if args.slow is not None :
            time.sleep(float(args.slow))
    return to_dump

def main() :
    args = arg_parser.get_args()
    if args.P :
        to_dump = data_injection(args)
    if args.U :
        to_dump = url_injection(args)


if __name__ == '__main__' :
    main()