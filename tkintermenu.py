# Import module
from tkinter import *
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from PIL import ImageTk, Image
import datetime as dt

# Code 1
dbcon=mysql.connector.connect(host='localhost',user='root',password='',database='hoteldb')
mycursor=dbcon.cursor()


def fun1():
    myconn = create_engine("mysql+mysqlconnector://root:""@localhost/hoteldb")
   
    df=pd.read_sql("select * from customer",myconn)
    df.loc[1]=['c2','Jeet','MMM6666','Pune',25,'2023-10-6']
    #df.to_sql("customer1",myconn)
    df=pd.read_sql("select * from customer",myconn)
    print(df)
    
    
    

def fun2():
    X=[1,2,3,4,5]
    Y=[87,90,95,85,43]
    plt.plot(X,Y,color="blue")
    plt.xlabel("Roll Number")
    plt.ylabel("Marks")
    plt.title("Result")
    plt.show()
    print("Function 2")
    
def addcustomer(): # Code 2
    print("Inside add customer")
    l1 = []
    cid = input("Enter Customer Id")
    l1.append(cid)
    cname = input("Enter Custome Name")
    l1.append(cname)
    adhaarid = input("Enter Adhaar Card Id")
    l1.append(adhaarid)
    address = input("Enter Address")
    l1.append(address)
    age = int(input("Enter Age"))
    l1.append(age)
    signindate = input("Enter Date for Booking")
    l1.append(signindate)
    roomno = int(input("Enter Room Number"))
    l1.append(roomno)
    
    query = "insert into customer values(%s,%s,%s,%s,%s,%s,%s)"
    val=(l1) # list we are converting to tuple it is part of syntax
    mycursor.execute(query,val)
    dbcon.commit() # to save changes in the mysql table
    df=pd.read_sql("SELECT * FROM customer",dbcon)
    print(df)

def funsqlalchemy():
    print("Using SQL Alchemy")
    con=sq.create_engine("mysql+mysqlconnector://root:""@localhost/school")
    print(con)
    df=pd.read_sql("select * from t1",con)
    print(df)

def updateroomstatus(): #Code 3
    rno=int(input("Enter Room Number"))
    print(rno)
    stat = input("Enter Status Available / Occupied ")
    query = "update rooms set status = %s where roomno = %s"
    val=([stat,rno])
    mycursor.execute(query,val)
    if mycursor.rowcount == 1:
        print("Room staus updated for Room No",rno)
    else:
        print("Failed to update Status Please check Room Number  ",rno)
    dbcon.commit()
    
def placeorder(): # Code 4
    
    df = pd.read_sql("select * from food",dbcon)
    df.set_index('foodid',inplace = True)
    print(df)
    orders = ""
    totalbill = 0
    total_per_item_price = 0
    l1 = []
    l2 = []
    
    cid = input("Enter Customer ID  ")
    l1.append(cid)
    
    choice = 'y'
    while(choice == 'y' or choice == 'Y'):
        total_per_item_price = 0
        foodid = int(input("Enter Food ID  "))
        qty = int(input("Enter Quantity  "))
        foodname = df.at[foodid,'foodname']
        orders = orders + "  " +((foodname+"-"+str(qty)))  # Join Strings to get all the orders    
        totalbill = totalbill + (df.at[foodid,'price'] * qty)
        total_per_item_price = total_per_item_price + (df.at[foodid,'price'] * qty)
        foodtype = df.at[foodid,'type']

        # To add records into Table to generate graph as per Food Popularity
        
        l2.clear()
        l2.append(foodid)
        l2.append(foodname)
        l2.append(foodtype)
        l2.append(qty)
        l2.append(int(total_per_item_price))
        val = (l2)
        print(val)
        query = "insert into tableorderedfood values(%s,%s,%s,%s,%s)"
        mycursor.execute(query,val)
        dbcon.commit()
        
        c = input("Press Y for next N for Stop ")
        choice = c
        
    
    l1.append(orders)
    l1.append(int(totalbill)) #Amount is coming from the dataframe which is int64 and sql column types is int (11) typecasting to int
    orderdate = (input("enter Date in this format yyyy-mm-dd "))
    l1.append(orderdate)
  
    val = (l1)
    query = "insert into transaction values(%s,%s,%s,%s)"
    mycursor.execute(query,val)
    if mycursor.rowcount == 1:
        print("Order placed Successfully")
    else:
        print("Please check Customer Id or Foodid ")
    dbcon.commit()

def generatebill():
    l1=[]
    cid=input("Enter Customer ID")
    l1.append(cid)
    val=(l1)
    
    mycursor.execute("select custname from customer where custid = %s",val)
    cname=mycursor.fetchone()
    print(cname)
    
# Create object
root = Tk()
 
# Adjust window size
root.geometry("600x600")

#window bg color
root.configure(bg='blue')


    

user_name = Label(root,text = "Hotel Managements System",width=40,height=2,bg='yellow').place(x = 140, y = 20)

B1 = Button(root, text ="Add Record", command = fun1,bg = 'red',bd=3,height=2,width=15,highlightcolor='green')
B1.place(x=50,y=80)

B2 = Button(root, text ="Search a Record", command = fun2,bg = 'red',bd=3,height=2,width=15,highlightcolor='green')
B2.place(x=50,y=160)

B3 = Button(root, text ="Add New Customer", command = addcustomer,bg = 'red',bd=3,height=2,width=15,highlightcolor='green')
B3.place(x=50,y=240)

B4 = Button(root, text ="Select Record", command = funsqlalchemy,bg = 'red',bd=3,height=2,width=15,highlightcolor='green')
B4.place(x=50,y=320)

B5 = Button(root, text ="Change Room Status", command = updateroomstatus,bg = 'red',bd=3,height=2,width=15,highlightcolor='green')
B5.place(x=50,y=400)

B6 = Button(root, text ="Place Order", command = placeorder,bg = 'green',bd=3,height=2,width=15,highlightcolor='green')
B6.place(x=50,y=480)

B7 = Button(root, text ="Generate Bill", command = generatebill,bg = 'yellow',bd=3,height=2,width=15,highlightcolor='green')
B7.place(x=50,y=560)

 
# Execute tkinter
root.mainloop()
