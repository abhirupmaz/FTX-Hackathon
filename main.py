# Modules imported
from tkinter import *
import tkinter.font as font
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import json
from search import JsonSearch

# Colour palette
WHITE = "#FFFFFF"
BLUE = "#2B3372"
GREEN = "#228B22"
RED = "#8B0000"

emp_name=""
emp_id=0
contact=""
email=""
balance=0

# Tkinter object creation
window = Tk()
window.title("Infosys Cafeteria")
window.config(bg=WHITE, padx=40, pady=50)

cp = cv2.VideoCapture(0)
cp.set(3,640)
cp.set(4,480)

# Set minimum window size value
# window.minsize(820, 660) 
# Set maximum window size value
# window.maxsize(820, 660)

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
    global balance
    global email
    global contact
    employee_id=photoscan()
    emp_id=employee_id

    information=JsonSearch.Searching(emp_id)
    if len(information)>0:
        emp_name=information[1]
        customer_label.config(text=f"Name: {emp_name}\nEmployee ID: {emp_id}\nBalance: Rs.{balance}")
        statusbar_label.config(text=f"Match found! Welcome {emp_name}!")
    else:
        statusbar_label.config(text="Invalid QR code entry!")
    print(information)


# Labels
store_label=Label(text="Cafeteria 3rd Floor",bg=WHITE,font=title, pady=20)
store_label.grid(row=1, column=1, columnspan=2)
customer_label=Label(text="Name: ____________\nEmployee ID: _______\nBalance: Rs.________",fg=WHITE,bg=BLUE,font=customer_text, padx=20)
customer_label.grid(row=2, column=2)
amount_label=Label(text="Enter amount: Rs.",bg=WHITE,font=body_text,pady=10)
amount_label.grid(row=3, column=1)
statusbar_label=Label(text="Scan your QR code to avail the services!",bg=WHITE,fg=GREEN, font=body_text)
statusbar_label.grid(row=5, column=1, columnspan=2)


# Entries
amount_entry = Entry(width=25, bg=BLUE)
amount_entry.grid(row=3, column=2)


# Buttons
scan_button = Button(text="SCAN",pady=20,padx=35,font=customer_text,border=0,command=scan)
scan_button.grid(row=2, column=1)
pay_button = Button(text="PAY",pady=20,padx=30,font=customer_text,border=0)
pay_button.grid(row=4, column=1, columnspan=2)


window.mainloop()