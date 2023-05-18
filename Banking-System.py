import sqlite3


def cust_id_generator():
    mydb = sqlite3.connect('bank_data.db')
    my_cursor = mydb.cursor()

    my_cursor.execute("""SELECT cust_id FROM customer""")
    Data = my_cursor.fetchall()
    mydb.close()
    if len(Data) == 0:
        return 0

    else:
        id_ = Data[-1]
        print(id_)

        last_id = id_[-1]
        print(last_id)
        return last_id


def all_client():
    mydb = sqlite3.connect('bank_data.db')
    my_cursor = mydb.cursor()

    my_cursor.execute("""SELECT name FROM customer WHERE status = 'Active'""")
    data = my_cursor.fetchall()
    client_name = []
    mydb.close()

    for i in data:
        for j in i:
            client_name.append(j)

    return client_name


def all_balance():
    mydb = sqlite3.connect('bank_data.db')
    my_cursor = mydb.cursor()

    my_cursor.execute("""SELECT balance FROM customer WHERE status = 'Active'""")
    data = my_cursor.fetchall()
    _all_balance = []
    mydb.close()

    for i in data:
        for j in i:
            _all_balance.append(j)

    return _all_balance


def client_finder(c_name, c_pin):
    mydb = sqlite3.connect('bank_data.db')
    my_cursor = mydb.cursor()

    my_cursor.execute(f"""SELECT cust_id FROM customer where name = '{c_name}' and client_pin = {c_pin} and status = 'Active'""")
    data = my_cursor.fetchall()
    mydb.close()
    if data is None:
        return 'Not Exist'

    else:
        client_id = []

        for i in data:
            for j in i:
                client_id.append(j)

        balance_ = balance_check(client_id[0])

        return balance_, client_id[0]


def balance_check(c_id):
    mydb = sqlite3.connect('bank_data.db')
    my_cursor = mydb.cursor()

    my_cursor.execute(f"""SELECT balance FROM customer WHERE cust_id = {c_id}""")
    data = my_cursor.fetchall()
    mydb.close()

    balance_ = []

    for i in data:
        for j in i:
            balance_.append(j)

    return balance_[0]


def balance_update(c_id, c_balance):
    mydb = sqlite3.connect('bank_data.db')
    my_cursor = mydb.cursor()

    try:
        my_cursor.execute(f"""UPDATE customer SET balance = {c_balance}
                                                WHERE cust_id = {c_id}""")

        mydb.commit()
        mydb.close()

    except Exception as e:
        mydb.close()
        return e

    my_cursor.execute(f"""SELECT balance FROM customer WHERE cust_id = {c_id}""")
    data = my_cursor.fetchall()

    bal_ = []
    mydb.close()

    for i in data:
        for j in i:
            bal_.append(j)

    return bal_[0]


def client_status(c_id):
    mydb = sqlite3.connect('bank_data.db')
    my_cursor = mydb.cursor()

    my_cursor.execute(f"""UPDATE customer SET status = 'InActive' WHERE cust_id = {c_id}""")
    mydb.commit()
    mydb.close()


mydb = sqlite3.connect('bank_data.db')
my_cursor = mydb.cursor()

my_cursor.execute("""CREATE TABLE if not exists customer(cust_id integer primary key unique,
                                                                    name text,
                                                                    client_pin text,
                                                                    balance integer,
                                                                    status text)""")

mydb.commit()


NamesOFClients = all_client()

my_cursor.execute("""SELECT client_pin FROM customer""")
ClientPins = my_cursor.fetchall()

ClientBalances = all_balance()

ClientDeposition = 0
ClientWithdrawal = 0
ClientBalance = 0
disk1 = 1
disk2 = 7
u = 0
while True:
    # os.system("cls")
    print("************************************************************")
    print("========== WELCOME TO ITSOURCECODE BANKING SYSTEM ==========")
    print("************************************************************")
    print("==========     (a). Open New Client Account     ============")
    print("==========     (b). The Client Withdraw a Money ============")
    print("==========     (c). The Client Deposit a Money  ============")
    print("==========     (d). Check Clients & Balance     ============")
    print("==========     (e). Close Client Account        ============")
    print("==========     (f). Quit                        ============")
    print("************************************************************")

    EnterLetter = input("Select a Letter from the Above Box menu : ")
    if EnterLetter == "a":
        print(" Letter a is Selected by the Client")
        name = input("Write Your Fullname : ")
        pin = str(input("Please Write a Pin to Secure your Account : "))
        ClientDeposition = eval(input("Please Insert a Money to Deposit to Start an Account : "))
        balance = ClientDeposition

        Client_ID = (int(cust_id_generator()) + 1)
        my_cursor.execute("""INSERT INTO customer VALUES (
                                            :cust_id,
                                            :name,
                                            :client_pin,
                                            :balance,
                                            :status)""",
                          {
                              'cust_id': Client_ID,
                              'name': name,
                              'client_pin': pin,
                              'balance': ClientDeposition,
                              'status': 'Active'
                          })

        mydb.commit()

        print("\nName=", end=" ")
        print(name)
        print("Pin=", end=" ")
        print(pin)
        print("Balance=", "P", end=" ")
        print(balance, end=" ")
        print("\nYour name is added to Client Table")
        print("Your pin is added to Client Table")
        print("Your balance is added to Client Table")
        print("----New Client account created successfully !----")
        print("\n")
        print("Your Name is Available on the Client list now : ")
        NamesOFClients = all_client()
        print(NamesOFClients)
        print("\n")
        print("Note! Please remember the Name and Pin")
        print("========================================")

        mainMenu = input(" Press Enter Key to go Back to Main Menu to Conduct Another Transaction or Quit_")

    elif EnterLetter == "b":
        print(" letter b is Selected by the Client")
        name = input("Please Insert a name : ")
        pin = input("Please Insert a pin : ")
        balance, customer_id = client_finder(name, pin)
        if balance == 'Not Exist':
            print("Customer Not Exists")

        else:
            print("Your Current Balance:", "P", end=" ")
            print(balance, end=" ")
            print("\n")
            ClientBalance = balance
            ClientWithdrawal = eval(input("Insert value to Withdraw : "))
            if ClientWithdrawal > ClientBalance:
                deposition = eval(input("Please Deposit a higher Value because your Balance mentioned above is not enough : "))
                ClientBalance = ClientBalance + deposition
                final_balance = balance_update(customer_id, ClientBalance)
                print("Your Current Balance:", "P", end=" ")
                print(final_balance, end=" ")
                ClientBalance = ClientBalance - ClientWithdrawal
                print("-\n")
                print("----Withdraw Successfully!----")
                final_balance = balance_update(customer_id, ClientBalance)
                print("Your New Balance: ", "P", final_balance, end=" ")
                print("\n\n")
            else:
                ClientBalance = ClientBalance - ClientWithdrawal
                print("\n")
                print("----Withdraw Successfully!----")
                final_balance = balance_update(customer_id, ClientBalance)
                print("Your New Balance: ", "P", final_balance, end=" ")
                print("\n")
        mainMenu = input(" Press Enter Key to go Back to Main Menu to Conduct Another Transaction or Quit_")

    elif EnterLetter == "c":
        print("Letter c is selected by the Client")
        name = input("Please Insert a name : ")
        pin = input("Please Insert a pin : ")
        balance, customer_id = client_finder(name, pin)
        if balance == 'Not Exist':
            print("Customer Not Exists")

        else:
            print("Your Current Balance: ", "P", end=" ")
            print(balance, end=" ")
            ClientBalance = balance
            print("\n")
            ClientDeposition = eval(input("Enter the value you want to deposit : "))
            ClientBalance = ClientBalance + ClientDeposition
            final_balance = balance_update(customer_id, balance)
            print("\n")
            print("----Deposition successful!----")
            print("Your New Balance: ", "P", ClientBalance, end=" ")
            print("\n")
            mydb.close()

        mainMenu = input(" Press Enter Key to go Back to Main Menu to Conduct Another Transaction or Quit_")
    elif EnterLetter == "d":
        print("Letter d is selected by the Client")
        print("Client name list and balances mentioned below : ")
        NamesOFClients = all_client()
        ClientBalances = all_balance()
        print("->.Customer =", NamesOFClients)
        print("->.Balance =", "P", ClientBalances, end=" ")

        print("\n")
        mydb.close()
        mainMenu = input(" Press Enter Key to go Back to Main Menu to Conduct Another Transaction or Quit_ ")

    elif EnterLetter == "e":
        print(f"Letter {EnterLetter} is Selected by the Client")
        name = input("Please Insert a name : ")
        pin = input("Please Insert a pin : ")
        balance, customer_id = client_finder(name, pin)
        if balance == 'Not Exist':
            print("Customer Not Esists")

        elif balance == 0:
            print("Your Available Balance is 0")
            client_status(customer_id)
            print("Your Account has been Closed Successfully")

        elif balance > 0:
            print(f"Your Available Balance is {balance}")
            print("Please Withdraw before Account Closing")
            input_val = input("Do you want to Withdraw all. Type Yes/No")
            if input_val.lower() == 'yes':
                ClientBalance = balance
                print("\n")
                ClientBalance = ClientBalance - balance
                final_balance = balance_update(customer_id, ClientBalance)
                print("\n")
                print("----Withdraw successful!----")
                client_status(customer_id)
                print("Your Account has been Closed Successfully")
                mydb.close()

            else:
                mainMenu = input(" Press Enter Key to go Back to Main Menu to Conduct Another Transaction or Quit_")

        mainMenu = input(" Press Enter Key to go Back to Main Menu to Conduct Another Transaction or Quit_")

    elif EnterLetter == "f":
        print("Letter e is selected by the Client")
        print("Thank you for using our banking system!")
        print("\n")
        print("Thank You and Come again")
        print("God Bless")

        mydb.close()
        break
    else:
        print("Invalid option selected by the Client")
        print("Please Try again!")

        mainMenu = input("Press Enter Key to go Back to Main Menu to Conduct Another Transaction or Quit_")
        mydb.close()
