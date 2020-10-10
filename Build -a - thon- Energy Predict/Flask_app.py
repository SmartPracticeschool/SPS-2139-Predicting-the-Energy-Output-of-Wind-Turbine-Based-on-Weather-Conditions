from flask import Flask,render_template,redirect,url_for,request
import requests


url = "https://e4o4v3xaag.execute-api.us-east-1.amazonaws.com/TurboStage_01"


headers = {
  'X-Amz-Content-Sha256': 'beaead3198f7da1e70d03ab969765e0821b24fc913697e929e726aeaebf0eba3',
  'X-Amz-Date': '20201009T163758Z',
  'Authorization': 'AWS4-HMAC-SHA256 Credential=ASIAXCW7ZNDIQM3O434I/20201009/us-east-1/execute-api/aws4_request, SignedHeaders=host;x-amz-content-sha256;x-amz-date, Signature=5648e4ad98f8bb5799e069ce0fac7e720687b44f8f71ff3d3cb613cd3c939409',
  'Content-Type': 'text/plain'
}



s=""

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        windspeed = str(float(request.form["Wind Speed"]))
        tpower =str(float(request.form["Theoretical_Power"]))
        wind_direction = str(float(request.form['Wind Direction']))
        s=windspeed+','+tpower+','+wind_direction

        payload = "{\r\n    \"data\" : \""+s+"\""+"\r\n}"
        

        
        response = requests.request("POST", url, headers=headers, data = payload)   

        r=response.text.encode('utf8')
        r=float(r)
        
        return render_template('Turbo.html',content=r)
    else:
        return render_template('Turbo.html')

if __name__ == "__main__":
    app.run(debug=True)