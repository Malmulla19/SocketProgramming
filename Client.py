'''
University of Bahrain.
College of Information Technology
ITCE320: Network Programing
Course Project.
Done By:
-Mahdi Abbas Mulla Ali
'''
import socket
import pickle
#Creating a socket for client.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Server's address: currently, client and server will both be working on the same machine.
address =("localhost", 4999)
#Connecting to the server
client.connect(address)
#Greeting message from server"
print(client.recv(1204).decode('ascii'))
print("*****************************")
#Login Function, first thing to be executed.
def login():
    print("============================================")
    print("Login to your account.")
    print("============================================")
    while True:
        username = input("Username: ")
        password = input("Password: ")
        client.send(username.encode('ascii'))
        client.send(password.encode('ascii'))
        result = client.recv(1024).decode('ascii')
        if result == "True":
            print("Login successful!")
            print("============================================")
            main()
            break
        elif result == "False":
            print("Wrong username or password, please try again.")
            print("============================================")
            login()
            break
        else:
            print("Wrong input, please try again.")
            print("============================================")
            login()
            break
#Searching for a book based on book title, author name, or original year of publication.
def search():
    client.send("SEARCH".encode('ascii'))
    while True:
        print('You can search for a book by'
              ' Book Title'
              ' Author Name'
              ' Original Year of Publication.')
        #Searching method is selected by the user.
        searchMethod = input('Search By: \n'
                             ' 1: Search by book title.\n'
                             ' 2: Search by Author name.\n'
                             ' 3: Search by Original year of publication.\n'
                             ' Your Choice: ')
        if searchMethod == '1' or searchMethod =='2' or searchMethod == '3':
            client.send(searchMethod.encode('ascii'))
            break
    #Taking input and receiving the search result from the server.
    search = input("Search for: ")
    client.send(search.encode('ascii'))
    print("=========================================")
    print("Search Results: ")
    print("=========================================")
    result = client.recv(8192)
    deSerialized_Result = pickle.loads(result)
    for y, l in deSerialized_Result.items():
        for x, z in l.items():
            if x =="ï»¿book_id":
                print("Book ID:",z)
            elif x == "books_count":
                print("Quantity Available:", z)
            elif x == "isbn":
                print("ISBN:", z)
            elif x == "authors":
                print("Author(s):", z)
            elif x == "original_publication_year":
                print("Year:", z)
            elif x == "title":
                print("Title:", z)
            elif x== "language_code":
                print("Language:", z)
            elif x == "price_bd":
                print("Price in BD:", z)
            elif x == "average_rating":
                if float(z) >= 4.3:
                    print("Rating:", z+"*")
                else:
                    print("Rating:",z)
        print("==========================================")
    main()
#Cart created at client's side.
#Adding books to the cart based on book's ID.
def cart():
    client.send("CART".encode('ascii'))
    print('You are viewing your cart. Choose an ID to be added to your cart. ')
    IDs = client.recv(1024)
    dIDs = pickle.loads(IDs)
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    for i in dIDs:
        print("Book ID:",i)
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    bool = True
    while bool:
        choice = input("Choose in ID to be added: ")
        for c in dIDs:
            if int(choice) == int(c) :
                client.send(choice.encode('ascii'))
                bool = False
                break
    result = client.recv(8192)
    deSerialized_Result = pickle.loads(result)
    bool = True
    for k, y in deSerialized_Result.items():
        for x, z in y.items():
            if z == "OUT OF STOCK":
                bool=False
                break

    if bool:
        #cart1.append(deSerialized_Result)
        print("Item has been added successfully!")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    else:
        print("Out of Stock!")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    main()
#List items on the cart, and in case of successful check ot, decrement request for each item on the cart.
def checkOut():
    total = 0
    list_of_books = []
    client.send("CheckOut".encode('ascii'))
    CartReceived = client.recv(1024)
    deSentralizedCart = pickle.loads(CartReceived)
    for i in deSentralizedCart:
        for x, z in i.items():
            for k, y in z.items():
                if k == "ï»¿book_id":
                    print("Book ID:", y)
                    list_of_books.append(y)
                elif k == "books_count":
                    print("Quantity Available:", y)
                elif k == "isbn":
                    print("ISBN:", y)
                elif k == "authors":
                    print("Author(s):", y)
                elif k == "original_publication_year":
                    print("Year:", y)
                elif k == "title":
                    print("Title:", y)
                elif k == "language_code":
                    print("Language:", y)
                elif k == "price_bd":
                    total+= float(y)
                    print("Price in BD:", y)
                elif k == "average_rating":
                    if float(y) >= 4.3:
                        print("Rating:", y + "*")
                    else:
                        print("Rating:", y)
                    print("==========================================")
    print("Total cost in BD:", total, "BD")
    print("==========================================")
    confirm = input("Confirm purchase: Y|N:")
    if confirm.lower() == 'y':
        client.send(pickle.dumps(list_of_books))
        print("Purchase Confirmed! Have a nice day.")
    elif confirm.lower() == 'n':
        client.send(pickle.dumps(list_of_books))
        print("Continue shopping!")
        main()
    else:
        print("Take this answer as a no")
        main()

def deleteItem():
    client.send('DeleteItem'.encode('ascii'))
    cart = pickle.loads(client.recv(1024))
    print("Cart items: ")
    print('------------------------------------')
    counter = 0
    for i in cart:
        counter += 1
        for x, z in i.items():
            for k, y in z.items():

                if k == "ï»¿book_id":
                    print("Book ID:", y)
                elif k == "books_count":
                    print("Quantity Available:", y)
                elif k == "isbn":
                    print("ISBN:", y)
                elif k == "authors":
                    print("Author(s):", y)
                elif k == "original_publication_year":
                    print("Year:", y)
                elif k == "title":
                    print("Title:", y)
                elif k == "language_code":
                    print("Language:", y)
                elif k == "price_bd":
                    print("Price in BD:", y)
                elif k == "average_rating":
                    if float(y) >= 4.3:
                        print("Rating:", y + "*")
                    else:
                        print("Rating:", y)
                    print("==========================================")
    print("")
    deleted = []
    while True:
        if counter > 0:
            x = input('Enter an ID for a book to be deleted: ')
            print(x, 'removed from your cart.')
            deleted.append(x)
            counter-=1
            if counter > 0:
                y = input("Type anything to continue, N to stop.")
                if y.lower() == 'n':
                    break
        elif counter == 0:
            break


    client.send(pickle.dumps(deleted))
    main()
#Main menu.
def main():
    msg = input('Choose an option, \n'
               ' 1: Search for a book, and display book\'s details.\n'
               ' 2: Adding a book by its ID.\n'
               ' 3: Checkout.\n'
                ' 4: Delete items from your cart.\n'
               ' 5: Q|q to terminate the connection.\n'
               ' Your choice: ')
    print("============================================")
    if msg.upper() == "Q":
        client.send(msg.encode('ascii'))
    elif msg == '1':
        search()
    elif msg == '2':
        cart()
    elif msg == '3':
        checkOut()
    elif msg == '4':
        deleteItem()
    else:
        print("Wrong input, please enter a valid option.")
        main()
login()
#Sending the message to the client.
print("<<<---Client is Closing--->>>")
client.send('Q'.encode('ascii'))
client.close()
