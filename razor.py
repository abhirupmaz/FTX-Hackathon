import razorpay
import json
import urllib   
import webbrowser
from time import sleep
import os
from flask import Flask, render_template, request
class payment:

    app=Flask(__name__,static_folder="static",static_url_path='',template_folder='templates')
        

    # def app_create():
    #     return render_template('scratch.html')

    # @app.route('/pay',methods=['POST']) 
    @app.route('/')
    def pay():
        global payment,name
        name=request.form.get('username')
        client = razorpay.Client(auth=("rzp_test_FkZvMExgTSe05S", "PQdBLPdJ2HCSV4devmbiav7y"))
        data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)

        return render_template('pay.html',payment=payment)

    @app.route("/shutdown", methods=['GET'])
    def shutdown():
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func is None:
            raise RuntimeError('Not running werkzeug')
        shutdown_func()
        return "Payment Complete. Return to main screen."


    # def start():
    #     app.run(host='0.0.0.0', threaded=True, port=5001)


    def stop():
        import requests
        resp = requests.get('http://localhost:5000/shutdown')

    if __name__=='__main__':
        webbrowser.open(url="http://localhost:5000/",new=0)
        app.debug=True

        app.run(use_reloader=False)
        #sleep brother


