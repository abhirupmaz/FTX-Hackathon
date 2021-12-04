# Modules imported
from tkinter import *
import tkinter.font as font
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from search import JsonSearch
import os
from time import sleep

# Colour palette
WHITE = "#FFFFFF"
BLUE = "#2B3372"
GREEN = "#228B22"
RED = "#8B0000"

emp_name=""
emp_id=""
amount=""
email=""
contact=""

# Tkinter object creation
window = Tk()
window.title("Infosys Cafeteria")
window.config(bg=WHITE, padx=40, pady=50)

cp = cv2.VideoCapture(0)
cp.set(3,640)
cp.set(4,480)

# Font
title = font.Font(family='Microsoft YaHei', size=20, weight='bold')
customer_text = font.Font(family='Microsoft YaHei', size=10)
body_text = font.Font(family='Microsoft YaHei', size=12, weight='bold')

# Scanning QR Code to get the unique employee id
def photoscan():
    global cp
    decoded_txt=[]
    while True:

        success, img = cp.read()
        for barcode in decode(img):
            if barcode.data.decode('utf-8') in decoded_txt:
                pass
            else:
                decoded_txt=[]
                decoded_txt.append(barcode.data.decode('utf-8'))
            
            pts = np.array([barcode.polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(img,[pts],True,(255,0,255),5)
            
        print(decoded_txt)

        cv2.imshow("QRDecoder",img)
        cv2.waitKey(1)
        if len(decoded_txt)>0:
            return decoded_txt[0]

def scan():
    global emp_name
    global emp_id
    global contact
    global email
    employee_id=photoscan()
    emp_id=employee_id

    information=JsonSearch.Searching(emp_id)
    if len(information)>0:
        emp_name=information[1]
        contact=information[2]
        email=information[3]
        customer_label.config(text=f"Name: {emp_name}\nEmployee ID: {emp_id}\nContact: {contact}")
        statusbar_label.config(text=f"Match found! Welcome {emp_name}!")
    else:
        statusbar_label.config(text="Invalid QR code entry!")
        customer_label.config(text="Name: ____________\nEmployee ID: _______\nContact: _________")
    print(information)

def testfunc():
    amount=amount_entry.get()
    if(amount!="" and int(amount)>0):
        with open('amount.txt','w') as amt:
            amt.write(amount)
        with open('templates/pay.html','w') as file:
            file.write(f"<html lang=\"en\"><head><meta charset=\"UTF-8\"><title> Payment Portal </title><style>p{{margin-top:300px;}}body{{background-image: url(\'page.png\');background-repeat: no-repeat;    background-attachment: fixed;    background-size: cover;    }}    </style>    </head>    <body>    <form action = \"pay\" method = \"POST\">    <h1><center><font color=\"FFFFFF\"><font face = \"Helvetica\"><font size=\"17\"><u>Payment Gateway</u></center></font></font></font size></h1>    <p align=\"center\"><font color=\"000000\"><font face=\"Helvetica\"><font size=\"14\"> <br> Name : {emp_name} <br> ID: {emp_id} <br> Amount (in Rupees) : {amount} </font></font></font size></p> <center><button id=\"rzp-button1\" onclick = \"alert(\'Details confirmed\')\"><h1>    Confirm and Proceed to Pay</h1>    </button></center><br>    </form>    <form action=\"shutdown\" method=\"GET\"><center><button> Exit </center></button></form></head><body>    <script src=\"https://checkout.razorpay.com/v1/checkout.js\"></script>    <script>    var options = {{        \"key\": \"rzp_test_T5vYP0nM4e2TR6\",        \"amount\": \"{amount}\",        \"currency\": \"INR\",        \"name\": \"Cafetaria \",        \"description\": \"Test Transaction\",        \"image\": \"https://images-platform.99static.com//JEOcS6bbb-re8Levu6-yR3cfXgc=/1003x1003:1999x1999/fit-in/500x500/99designs-contests-attachments/112/112513/attachment_112513661\",        \"order_id\": \"{{{{payment[\'id\']}}}}\",          \"handler\": function (response){{            alert(response.razorpay_payment_id);            alert(response.razorpay_order_id);            alert(response.razorpay_signature)        }},        \"prefill\": {{            \"name\": \"{emp_name}\",            \"email\": \" {email} \",            \"contact\": \" {contact} \"        }},        \"notes\": {{           \"address\": \"Razorpay Corporate Office\"        }},        \"theme\": {{            \"color\": \"#3399cc\"        }}    }};    var rzp1 = new Razorpay(options);    rzp1.on(\'payment.failed\', function (response){{            alert(response.error.code);            alert(response.error.description);            alert(response.error.source);            alert(response.error.step);            alert(response.error.reason);            alert(response.error.metadata.order_id);            alert(response.error.metadata.payment_id);    }});    document.getElementById(\'rzp-button1\').onclick = function(e){{        rzp1.open();        e.preventDefault();    }}    </script></body></html>")
        os.system('python razor.py')
    else:
        statusbar_label.config(text="Enter a valid amount.")

# Labels
store_label=Label(text="Cafeteria 3rd Floor",bg=WHITE,font=title, pady=20)
store_label.grid(row=1, column=1, columnspan=2)
customer_label=Label(text="Name: ____________\nEmployee ID: _______\nContact: _________",fg=WHITE,bg=BLUE,font=customer_text, padx=20)
customer_label.grid(row=2, column=2)
amount_label=Label(text="Enter amount: Rs.",bg=WHITE,font=body_text,pady=10)
amount_label.grid(row=3, column=1)
statusbar_label=Label(text="Scan your QR code to avail the services!",bg=WHITE,fg=GREEN, font=body_text)
statusbar_label.grid(row=5, column=1, columnspan=2)


# Entries
amount_entry = Entry(width=25, bg=BLUE, fg=WHITE)
amount_entry.grid(row=3, column=2)


# Buttons
scan_button = Button(text="SCAN",pady=20,padx=35,font=customer_text,border=0,command=scan)
scan_button.grid(row=2, column=1)
pay_button = Button(text="PAY",pady=20,padx=30,font=customer_text,border=0, command=testfunc)
pay_button.grid(row=4, column=1, columnspan=2)

window.mainloop()


