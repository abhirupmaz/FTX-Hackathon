import razorpay
import json
from flask import Flask, render_template, request
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

if __name__=='__main__':
    app.debug=True
    app.run()
