import argparse

def add_arguments() :
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', dest='url', required=True, help='target url')
    parser.add_argument('-U', '--URL', dest='U', required=False, action='store_true', help='injection on url paramters')
    parser.add_argument('-P', '--POST', dest='P', required=False, action='store_true', help='injection on data post')
    parser.add_argument('-param', '--param', dest='param', type=str, required=True, help='parameter used to be injected (json list)')
    parser.add_argument('-w', '--wordlist', dest='wordlist', required=False, help='wordlist of files that will be searched')
    parser.add_argument('-o', '--output', dest='output', required=False, help='file.txt where output is dump')
    parser.add_argument('-headers', '--headers', dest='headers', required=False, help='optional http headers on json dictionnay format')
    parser.add_argument('-c', '--cookies', dest='cookies', required=False, help='optionnal http cookies on json dictionnary format')
    parser.add_argument('-data', '--data', dest='data', required=False, help='optional http data on json dictionnary format')
    parser.add_argument('-p', '--post', dest='post', required=False, action='store_true', help='post request (get by default)')
    parser.add_argument('-f', '--find', dest='find', required=False, help='look for keywords in respone (-find \'[\'word1\',\'word2\']\')')
    parser.add_argument('-base64', '--base64', dest='base64', action="store_true", required=False, help='convert the response in base64 and search keyword in it (watch out to buffering)')
    parser.add_argument('-s', '--silent', dest='silent', required=False, action='store_true', help='silent mode, only print the output')
    parser.add_argument('-slow', '--slow', dest='slow', type=float, required=False, help='time to sleep beetwen two requests')
    parser.add_argument('-encode', '--encode', dest='encode', required=False, action='store_true', help='encode the wordlist in url')
    return parser

def error_args(parser, args) :
    if not (args.U or args.P) :
        parser.error("You need to choose beetwen -U (Url injection) and -P (data post injection)")
    if args.wordlist is None :
        parser.error("You need to provide a -w WORDLIST.txt") 
    if args.base64 and args.find is None :
        parser.error("-base64 paramter can't be used without -f parameter")
    if args.encode and args.U is None :
        parser.error("-encode paramter require the -U paramter")

def get_args() :
    parser = add_arguments()
    args = parser.parse_args()
    error_args(parser, args)
    return args

