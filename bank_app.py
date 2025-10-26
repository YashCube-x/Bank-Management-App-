import json
import random
import string
from pathlib import Path
import streamlit as st


class Bank:
    BASE_DIR = Path(__file__).parent
    database = BASE_DIR / 'data.json'
    data = []

    # Load JSON data
    try:
        if database.exists():
            with open(database, 'r') as fs:
                try:
                    data = json.load(fs)
                except json.decoder.JSONDecodeError:
                    data = []
        else:
            with open(database, 'w') as fs:
                json.dump([], fs)
    except Exception as err:
        st.error(f"Error while loading data: {err}")

    # Save JSON data
    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            json.dump(Bank.data, fs, indent=4)

    # Generate account number
    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_uppercase, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)
        acc = alpha + num + spchar
        random.shuffle(acc)
        return "".join(acc)

    # Create account
    def Createaccount(self, name, age, email, pin):
        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo": Bank.__accountgenerate(),
            "balance": 0
        }

        if info['age'] < 18 or len(str(info['pin'])) != 4:
            st.error("❌ Age must be 18+ and PIN must be 4 digits.")
            return

        Bank.data.append(info)
        Bank.__update()
        st.success("✅ Account created successfully!")
        st.info(f"Your Account Number: **{info['accountNo']}**")

    # Deposit
    def depositmoney(self, accnumber, pin, amount):
        user = next((i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin), None)
        if not user:
            st.error("❌ No such account found.")
            return
        if amount > 10000 or amount <= 0:
            st.warning("⚠️ Deposit amount must be between ₹1 and ₹10,000.")
            return

        user['balance'] += amount
        Bank.__update()
        st.success(f"✅ ₹{amount} deposited successfully!")

    # Withdraw
    def withdrawmoney(self, accnumber, pin, amount):
        user = next((i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin), None)
        if not user:
            st.error("❌ No such account found.")
            return
        if amount > user['balance']:
            st.warning("⚠️ Insufficient balance.")
            return

        user['balance'] -= amount
        Bank.__update()
        st.success(f"✅ ₹{amount} withdrawn successfully!")

    # Show details
    def showdetails(self, accnumber, pin):
        user = next((i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin), None)
        if not user:
            st.error("❌ Account not found.")
            return

        st.subheader("📄 Account Details:")
        st.json(user)

    # Update details
    def updatedetails(self, accnumber, pin, new_name, new_email, new_pin):
        user = next((i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin), None)
        if not user:
            st.error("❌ No such user found.")
            return

        user['name'] = new_name or user['name']
        user['email'] = new_email or user['email']
        user['pin'] = int(new_pin) if new_pin else user['pin']
        Bank.__update()
        st.success("✅ Account details updated successfully!")

    # Delete
    def delete(self, accnumber, pin):
        user = next((i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin), None)
        if not user:
            st.error("❌ Account not found.")
            return
        Bank.data.remove(user)
        Bank.__update()
        st.success("✅ Account deleted successfully!")


# ---- Streamlit UI ----
st.title("🏦 Suyash Bank Management System")

bank = Bank()
menu = ["Create Account", "Deposit", "Withdraw", "Show Details", "Update Details", "Delete Account"]
choice = st.sidebar.radio("Select an Option", menu)

# ---- Create Account ----
if choice == "Create Account":
    st.subheader("🧾 Create New Account")
    name = st.text_input("Enter your Name")
    age = st.number_input("Enter your Age", min_value=1)
    email = st.text_input("Enter your Email")
    pin = st.text_input("Enter 4-digit PIN", type="password")
    if st.button("Create Account"):
        if not all([name, age, email, pin]):
            st.warning("⚠️ Please fill all fields.")
        else:
            bank.Createaccount(name, age, email, int(pin))

# ---- Deposit ----
elif choice == "Deposit":
    st.subheader("💰 Deposit Money")
    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")
    amt = st.number_input("Enter Deposit Amount", min_value=0)
    if st.button("Deposit"):
        bank.depositmoney(acc, int(pin), amt)

# ---- Withdraw ----
elif choice == "Withdraw":
    st.subheader("🏧 Withdraw Money")
    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")
    amt = st.number_input("Enter Withdraw Amount", min_value=0)
    if st.button("Withdraw"):
        bank.withdrawmoney(acc, int(pin), amt)

# ---- Show Details ----
elif choice == "Show Details":
    st.subheader("📄 Show Account Details")
    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")
    if st.button("Show"):
        bank.showdetails(acc, int(pin))

# ---- Update ----
elif choice == "Update Details":
    st.subheader("✏️ Update Account Details")
    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter Current PIN", type="password")
    new_name = st.text_input("Enter New Name (optional)")
    new_email = st.text_input("Enter New Email (optional)")
    new_pin = st.text_input("Enter New PIN (optional)")
    if st.button("Update"):
        bank.updatedetails(acc, int(pin), new_name, new_email, new_pin)

# ---- Delete ----
elif choice == "Delete Account":
    st.subheader("🗑️ Delete Account")
    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")
    if st.button("Delete Account"):
        bank.delete(acc, int(pin))
