import json
class JsonSearch:
    def __init__(self,n) :
        self.n=n
    def Searching(n):
        customerData=open("data.json")
        customer=json.load(customerData)
        f=0
        information=[]
        for code in customer["people"]:
            if code["Employee_id"]==n:
                information.append(code["Employee_id"])
                information.append(code["name"])
                information.append(code["Contact"])
                information.append(code["Email"])
                print(code["Employee_id"])
                print(code["name"])
                print(code["Contact"])
                print(code["Email"])
                f=1
        if(f==0):
            print("Invalid Entry!")
        customerData.close()
        return information