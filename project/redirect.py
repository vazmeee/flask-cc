from flask import Flask, redirect
import requests
import os


app=Flask(__name__)


@app.route("/<path>")
def redirect_other(path):
#    r=request.url()
#    print(r)
#    return redirect('0.0.0.0:80/'+str(r), code=302)
#    return redirect('0.0.0.0:80/'+"path", code=302)
    r=requests.get("http://0.0.0.1:80/categories").json()
    return json.dumps(r)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 100))
    app.run(host="0.0.0.0",port=port)
