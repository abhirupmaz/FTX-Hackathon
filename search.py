import json
class JsonSearch:
    def __init__(self,n) :
        self.n=n
    def Searching():
        customerData=open("data.json")
        customer=json.load(customerData)
        f=0
        n=int(input("Enter The Employee ID:"))
        for code in customer["people"]:
            if (int(code["Employee_id"])==n):
                print(code["Employee_id"])
                print(code["name"])
                print(code["Balance"])
                f=1
        if(f==0):
            print("I AM NOOB :)")
        customerData.close()