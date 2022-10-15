'''
University of Bahrain.
College of Information Technology
ITCE320: Network Programing
Course Project.
Done By:
-Mahdi Abbas Mulla Ali
'''
import socket
import threading
import csv
from datetime import datetime
import re
import pickle

#By Default it will run on IPv4 and TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#IP & port number
IP, PORT = "localhost", 4999
#Binding the server with th address
server.bind((IP,PORT))
# Class: Creating a cart object for each client.
class Cart:
    def __init__(self, sock):
        self.sock = sock
        self.cart = {}
        self.total = 0
        self.counter = 0

    def add(self, id):
        with open('books - 20211.csv', 'r') as f:
            reader = csv.DictReader(f)
            for i in reader:
                if int(i["ï»¿book_id"]) == id:
                    self.cart[self.counter] = i
                    self.counter += 1
                    self.total += float(i["price_bd"])

    def remove(self, id):
        with open('books - 20211.csv', 'r') as f:
            reader = csv.DictReader(f)
            for i in reader:
                if int(i["ï»¿book_id"]) == id:
                    for x in self.cart:
                        if self.cart[x]["ï»¿book_id"] == i["ï»¿book_id"]:
                            self.total -= float(i["price_bd"])
                            self.cart.pop(x)
                            break

    def getCart(self):
        return self.cart

    def getTotal(self):
        return self.total

    def getCounter(self):
        return self.counter
#Removing ordered items
fnames = ["ï»¿book_id","books_count","isbn","authors","original_publication_year","title",
          "language_code","price_bd","average_rating","ratings_count"]
#Remove a book from the database
def rmv(id):
    temp_file = open('temp.csv', 'w', newline='')
    with open('books - 20211.csv', 'r') as f:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(temp_file, fieldnames=fnames)
        writer.writeheader()
        for row in reader:
            y = int(row['ï»¿book_id'])
            if y == id:
                x = int(row['books_count'])
                print(x)
                x-=1
                writer.writerow({'ï»¿book_id': row['ï»¿book_id'], 'books_count': str(x), 'isbn': row['isbn'],
                                 'authors': row['authors'],
                                 'original_publication_year': row['original_publication_year'],
                                 'title': row['title'], 'language_code': row['language_code'],
                                 'price_bd': row['price_bd'],
                                 'average_rating': row['average_rating'], 'ratings_count': row['ratings_count']})
            else:
                writer.writerow(row)
        temp_file.close()
    with open('books - 20211.csv', 'w', newline='') as new:
        temp_file = open('temp.csv', 'r')
        reader2 = csv.DictReader(temp_file)
        writer1 = csv.DictWriter(new, fieldnames=fnames)
        writer1.writeheader()
        for row in reader2:
            writer1.writerow(row)

#Creating a login function.
def login(usrname, passw):
#CSV file that contains login information. Username and password.
    with open('MEMBERS.csv', 'r') as f:
        reader = csv.DictReader(f)
        for x in reader:
            if x["username"]== usrname:
                if x["password"] == passw:
                    print("Access granted for ", usrname, "on ", datetime.now().strftime("%H:%M:%S"))
                    return True
#Processing Client's request.
def addRequest(id):
    choice = id
    with open('books - 20211.csv', 'r') as f:
        reader = csv.DictReader(f)
        book_requested = {}
        for i in reader:
            if int(i["ï»¿book_id"]) == choice:
                if int(i["books_count"]) >0:
                    book_requested[0] = i
                    return book_requested
                else:
                    error = {1: {"Error: ": "OUT OF STOCK"}}
                    return error
#Searching Algorithm.
def search(sock, inp, inp2):
    print("From", sock, "Received a search request")
    with open('books - 20211.csv', 'r') as f:
        reader = csv.DictReader(f)
        bool = False
        counter = 1
        response = {}
        for i in reader:
            if inp == '1':
                By_Title = re.findall(inp2.lower(), i["title"].lower())
                if len(By_Title) > 0:
                    bool = True
                    response[counter] = i
                    counter += 1
            elif inp == '2':
                By_Author = re.findall(inp2.lower(), i["authors"].lower())
                if len(By_Author) > 0:
                    bool = True
                    response[counter] = i
                    counter += 1
            elif inp == '3':
                By_Year = re.findall(inp2.lower(), i["original_publication_year"].lower())
                if len(By_Year) > 0:
                    bool = True
                    response[counter] = i
                    counter += 1

        if not bool:
            error = {1:{"Error: ": "Nothing Found!"}}
            serialize_response = pickle.dumps(error)
        elif bool:
            serialize_response = pickle.dumps(response)
        return serialize_response
#Getting all Books ID's
def getID():
    with open('books - 20211.csv', 'r') as f:
        IDS = []
        reader = csv.DictReader(f)
        for i in reader:
            IDS.append(i["ï»¿book_id"])
        serializedID = pickle.dumps(IDS)
        return serializedID

#Creting a thread function:
def connection_thread(sock, id):
    print("<<<---Start of thread id No.: ",id," --->>>")
    #Sending a greeting message to the client.
    greeting = "Hi, from server!".encode('ascii')
    sock.send(greeting)
    CCart = Cart(sock)
    while True:
        usern = sock.recv(1024).decode('ascii')
        passw = sock.recv(1024).decode('ascii')
        if login(usern, passw):
            sock.send("Welcome".encode('ascii'))
            break
        sock.send("Try again ".encode('ascii'))
    while True:
        data = sock.recv(1024).decode('ascii')
        if data == "SEARCH":
            inp = sock.recv(1024).decode('ascii') #Search Method
            inp2 = sock.recv(1024).decode('ascii') #Search for
            result = search(sock, inp, inp2)
            sock.send(result)
        elif data == "CART":
            items = getID()
            sock.send(items)
            bookID=sock.recv(1024).decode('ascii')
            check_return = addRequest(int(bookID))
            sResult = pickle.dumps(check_return)
            sock.send(sResult)
            add = True
            for k, y in check_return.items():
                for x, z in y.items():
                    if z == "OUT OF STOCK":
                        add =False
                        print("OUT OF STOCK")
            if add:
                CCart.addBook(check_return)
                print("Book added successfully for, ",sock)
        elif data == "CheckOut":
            CartToClient = pickle.dumps(CCart.sendCart())
            sock.send(CartToClient)
            Books_to_buy = pickle.loads(sock.recv(1024))
            for i in Books_to_buy:
                rmv(int(i))
        elif data == 'DeleteItem':
            sock.send(pickle.dumps(CCart.sendCart()))
            deleted = pickle.loads(sock.recv(1024))
            for i in deleted:
                CCart.rmvBook(i)
        elif data.upper() == "Q":
            print("<<<---End of thread id No.: ", id, "at",datetime.now().strftime("%H:%M:%S")," --->>>")
            Clients.remove(id)
            break
#Keeping 3 in waiting
server.listen(4)
#Printing a greeting message
print("<<<---Server has started!--->>>")
counter = 0
#Looping 4 times, receiving one message from 4 different clients.
Thread_Counter =[]
Clients = []
while len(Clients)<4:
    server.listen(5)
    sock_a, sockname = server.accept()
    t = threading.Thread(target=connection_thread,args=(sock_a, len(Thread_Counter)+1), daemon=False)
    Thread_Counter.append(t)
    print("New Connection is here, current threads: ")
    for i in Thread_Counter:
        print(i)
    print("------------------------------------------------------")
    #Will assign an ID for each client based on the length of the threads.
    Clients.append(len(Thread_Counter))
    print(len(Clients))
    t.start()
print("\n<<<---Server is Closing!--->>>")
server.close()
