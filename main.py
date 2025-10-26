import json 
import random
import string 
from pathlib import Path 


class Bank:
    # 👇 This ensures data.json is created inside the same folder as your .py file
    BASE_DIR = Path(__file__).parent
    database = BASE_DIR / 'data.json'
    data = []
    
    try:
        if database.exists():
            with open(database, 'r') as fs:
                try:
                    data = json.load(fs)
                except json.decoder.JSONDecodeError:
                    data = []
        else:
            print("No such file exist — creating new data.json file.")
            with open(database, 'w') as fs:
                json.dump([], fs)
    except Exception as err:
        print(f"An exception occured as {err}")
    
    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            json.dump(Bank.data, fs, indent=4)

    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)

    def Createaccount(self):
        info = {
            "name": input("Tell your name :- "),
            "age": int(input("tell your age :- ")),
            "email": input("tell your email :- "),
            "pin": int(input("tell your 4 number pin :- ")),
            "accountNo.": Bank.__accountgenerate(),
            "balance": 0
        }
        if info['age'] < 18 or len(str(info['pin'])) != 4:
            print("sorry you cannot create your account")
        else:
            print("account has been created successfully")
            for i in info:
                print(f"{i} : {info[i]}")
            print("please note down your account number")

            Bank.data.append(info)
            Bank.__update()
        
    def depositmoney(self):
        accnumber = input("please tell your account number: ")
        pin = int(input("please tell your pin: "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if not userdata:
            print("sorry no data found")
        else:
            amount = int(input("how much you want to deposit: "))
            if amount > 10000 or amount <= 0:
                print("sorry, you can deposit below 10000 and above 0")
            else:
                userdata[0]['balance'] += amount
                Bank.__update()
                print("Amount deposited successfully!")

    def withdrawmoney(self):
        accnumber = input("please tell your account number: ")
        pin = int(input("please tell your pin: "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if not userdata:
            print("sorry no data found")
        else:
            amount = int(input("how much you want to withdraw: "))
            if userdata[0]['balance'] < amount:
                print("sorry, you don't have that much money")
            else:
                userdata[0]['balance'] -= amount
                Bank.__update()
                print("Amount withdrew successfully!")

    def showdetails(self):
        accnumber = input("please tell your account number: ")
        pin = int(input("please tell your pin: "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]
        if not userdata:
            print("no such account found")
        else:
            print("\nYour information:\n")
            for i in userdata[0]:
                print(f"{i} : {userdata[0][i]}")

    def updatedetails(self):
        accnumber = input("please tell your account number: ")
        pin = int(input("please tell your pin: "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if not userdata:
            print("no such user found")
        else:
            print("you cannot change the age, account number, or balance")
            print("Fill details for change or leave empty if no change")

            newdata = {
                "name": input("please tell new name or press enter: "),
                "email": input("please tell your new Email or press enter to skip: "),
                "pin": input("enter new Pin or press enter to skip: ")
            }

            if newdata["name"] == "":
                newdata["name"] = userdata[0]['name']
            if newdata["email"] == "":
                newdata["email"] = userdata[0]['email']
            if newdata["pin"] == "":
                newdata["pin"] = userdata[0]['pin']
            else:
                newdata["pin"] = int(newdata["pin"])

            newdata['age'] = userdata[0]['age']
            newdata['accountNo.'] = userdata[0]['accountNo.']
            newdata['balance'] = userdata[0]['balance']

            index = Bank.data.index(userdata[0])
            Bank.data[index] = newdata
            Bank.__update()
            print("details updated successfully!")

    def Delete(self):
        accnumber = input("please tell your account number: ")
        pin = int(input("please tell your pin: "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if not userdata:
            print("sorry no such data exist")
        else:
            check = input("press y if you actually want to delete the account or press n: ")
            if check.lower() == 'y':
                Bank.data.remove(userdata[0])
                Bank.__update()
                print("account deleted successfully!")
            else:
                print("deletion cancelled")


# ---------------- Menu ----------------
user = Bank()
print("press 1 for creating an account")
print("press 2 for depositing the money in the bank")
print("press 3 for withdrawing the money")
print("press 4 for details")
print("press 5 for updating the details")
print("press 6 for deleting your account")

check = int(input("tell your response :- "))

if check == 1:
    user.Createaccount()
elif check == 2:
    user.depositmoney()
elif check == 3:
    user.withdrawmoney()
elif check == 4:
    user.showdetails()
elif check == 5:
    user.updatedetails()
elif check == 6:
    user.Delete()
else:
    print("invalid choice")
