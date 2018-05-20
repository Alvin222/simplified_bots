from flask import Flask, jsonify,request
from bs4 import BeautifulSoup as bSoup
import requests as uReq
import urllib
from linepy import*
from getQrV2 import*

app = Flask(__name__)
listQr = []

@app.route('/')
def index():
    return "Welcome to alvin api :v"
@app.route('/qr/<string:appName>')
def generateQr(appName):
       if appName == '':
           token = TokenGenerator().getQr()
       else:
           appName =appName.upper() +'\t8.3.1AVNRDM-2K18\t11.2.5'
           token = TokenGenerator(appName=appName).getQr()
       verifier = token[len('line://au/q/'):]
       return jsonify({'qr' : token, 'verifier' : verifier})
@app.route('/token/<string:appName>',methods=['POST'])
def genToken(appName):
       jsons = request.get_json(force=True)
       result = {'token' : '', 'error' : ''}
       if 'verifier' not in jsons:
           result['error'] = 'Invalid post'
           return jsonify(result)
       if appName == '':
           token = TokenGenerator().getToken(jsons['verifier'])
       else:
           appName =appName.upper() +'\t8.3.1AVNRDM-2K18\t11.2.5'
           token = TokenGenerator(appName=appName).getToken(jsons['verifier'])
       result['token'] = token.authToken
       return jsonify(result)
@app.route('/google',methods=['POST'])
def googlesearch():
    a = request.get_json(force=True)
    if 'quote' not in a:
       return jsonify({'error': 'Invalid Data','result' : []})
    text = a['quote']
    with uReq.session() as web:
        web.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        web = web.get("https://www.google.co.id/search?q={}".format(urllib.parse.quote(text)))
        data = bSoup(web.content, "html5lib")
        result = []
        for getdatafirst in data.findAll("div", {"class":"g"}):
              for getdatatwo in getdatafirst.findAll("div", {"class":"rc"}):
                     for geturlandtitle in getdatatwo.findAll("h3", {"class":"r"}):
                            title = geturlandtitle.a.text
                            url = geturlandtitle.a["href"]
                            result.append({'title' : title, 'url' : url})
        return jsonify({"result": result,'error' : None})
		
if __name__ == '__main__':
    app.run(debug=True)