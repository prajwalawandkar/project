import mysql.connector as sqlt
import pandas as pd 
from tabulate import tabulate
import matplotlib.pyplot as plt
con = sqlt.connect(host = "localhost", user = "root", passwd = "123123123", database = "library")
cursor = con.cursor()
def book_input():
    bookid=input("Enter Book Id")
    bname = input("Enter Book Name")
    author = input("Enter Author Name")
    price = float(input("Enter Price"))
    copies = int(input("Enter No of Copies"))
    qry = "insert into book values({}, '{}', '{}', {}, {}, {});".format(bookid, bname, author, price, copies, copies)
    cursor.execute(qry)
    con.commit()
    print("The Book has been successfully")

def book_edit():
    x=int(input("Enter Book ID"))
    qry="select * from book where bookid = {};".format(x)
    cursor.execute(qry)
    r=cursor.fetchone()
    if r:
        y=float(input("Enter New Price"))
        qry = "Update book set price = {} where bookid = {};".format(y,x)
        cursor.execute(qry)
        con.commit()
        print("Edited Successfully ")
    else:
        print("Invalid Book ID")
def book_delete():
    x=int(input("Enter Book ID"))
    qry="select * from book where bookid = {};".format(x)
    cursor.execute(qry)
    r=cursor.fetchone()
    if r:
        qry = "Delete from book where bookid = {};".format(x)
        cursor.execute(qry)
        con.commit()
        print("Deleted Successfully ")
    else:
        print("Invalid Book ID")
def book_search():
    x=int(input("Enter Book ID"))
    qry="select * from book where bookid = {};".format(x)
    cursor.execute(qry)
    r=cursor.fetchone()
    if r:
        df = pd.read_sql(qry,con)
        print(tabulate(df, headers = 'keys', tablefmt = 'psql', showindex = False))

    else:
        print("Invalid Book ID")

def member_input():
    memberid=int(input("Enter Member Id"))
    mname = input("Enter Member Name")
    madd = input("Enter Member Address")
    phone = input("Enter Phone No")

    qry = "insert into member values ({}, '{}', '{}', '{}');".format(memberid, mname, madd, phone)
    cursor.execute(qry)
    con.commit()
    print("The Member has been successfully")

def member_edit():
    x=int(input("Enter Member ID"))
    qry="select * from member where memberid = {};".format(x)
    cursor.execute(qry)
    r=cursor.fetchone()
    if r:
        y=input("Enter New Address") 
        qry = "update member set madd = '{}' where memberid = {};".format(y,x)
        cursor.execute(qry)
        con.commit()
        print("Edited Successfully ")
    else:
        print("Invalid Member ID")
def member_delete():
    x=int(input("Enter Member ID"))
    qry="select * from member where memberid = {};".format(x)
    cursor.execute(qry)
    r=cursor.fetchone()
    if r:
        qry = "Delete from member where memberid = {};".format(x)
        cursor.execute(qry)
        con.commit()
        print("Deleted Successfully ")
    else:
        print("Invalid Member ID")
def member_search():
    x=int(input("Enter Member ID"))
    qry="select * from member where memberid = {};".format(x)
    cursor.execute(qry)
    r=cursor.fetchone()
    if r:
        df = pd.read_sql(qry,con)
        print(tabulate(df, headers = 'keys', tablefmt = 'psql', showindex = False))

    else:
        print("Invalid Member ID")
def book_output():
    df = pd.read_sql("select * from book", con)
    print(tabulate(df, headers = 'keys', tablefmt = 'psql', showindex = False))

def member_output():
    df = pd.read_sql("select * from member", con)
    print(tabulate(df, headers = 'keys', tablefmt = 'psql', showindex = False))

def return_output():
    df = pd.read_sql("select * from returns", con)
    print(tabulate(df, headers = 'keys', tablefmt = 'psql', showindex = False))

def issue_output():
    df = pd.read_sql("select * from issued", con)
    print(tabulate(df, headers = 'keys', tablefmt = 'psql', showindex = False))

def book_issued():
    q = "select max(issueid) from issued;"
    cursor.execute(q)
    r = cursor.fetchone() [0]
    if r:
        issueid = r+1
    else:
        issueid = 1
    x=int(input("Enter Member ID"))
    q1 = "select * from member where memberid = {};".format(x)
    cursor.execute(q1)
    r=cursor.fetchone()
    if r:
        y =int(input("Enter Book ID"))
        q2 = "select bookid, rem_copies from book where bookid = {};".format(y)
        cursor.execute(q2)
        r=cursor.fetchone()
        if r:
            if r[1] > 0:
                issuedate = input("Enter Issue Date")
                copies = int(input("Enter No of Copies"))
                remcopies = r[1] - copies
                q3 = "insert into issued values({}, '{}',{},{},{});".format(issueid, issuedate, x, y, copies)
                cursor.execute(q3)
                q4 = "update book set rem_copies = {} where bookid = {};".format(remcopies,y)
                cursor.execute(q4)
                con.commit()
                print("The Book Has Been Issued")
            else:
                print("The Book Is Unavailable")
        else:
            print("Invalid Book ID")
    else:
        print("Invalid Member ID")
def book_returns():
    q = "select max(issueid) from returns;"
    cursor.execute(q)
    r = cursor.fetchone() [0]
    if r:
        issueid = r+1
    else:
        issueid = 1
    x=int(input("Enter Member ID"))
    q1 = "select * from member where memberid = {};".format(x)
    cursor.execute(q1)
    r=cursor.fetchone()
    if r:
        y =int(input("Enter Book ID"))
        q2 = "select bookid, rem_copies from book where bookid = {};".format(y)
        cursor.execute(q2)
        r=cursor.fetchone()
        if r:
           
            issuedate = input("Enter Return Date")
            copies = int(input("Enter No of Copies"))
            remcopies = r[1] + copies
            q3 = "insert into returns values({}, '{}',{},{},{});".format(issueid, issuedate, x, y, copies)
            cursor.execute(q3)
            q4 = "update book set rem_copies = {} where bookid = {};".format(remcopies,y)
            cursor.execute(q4)
            con.commit()
            print("The Book Has Been Returned")
        else:
            print("Invalid Book ID")
    else:
        print("Invalid Member ID")
def col_chart():
    q = "select bookid, count(copies) as totalcopies from issued group by bookid;"
    df = pd.read_sql(q,con)
    print(df)
    plt.bar(df.bookid, df.totalcopies)
    plt.xlabel("BookID")
    plt.ylabel("Copies Issued")
    plt.title("Test Reading Book")
    plt.xticks(df.bookid)
    plt.show()
while(True):
    print("="*80)
    print("\t\t\t-----Library Management System-----\n")
    print("="*80)
    print("\t\t\t\tEnter Your Choice\n\t\t\t1.Book Details\n\t\t\t2.Member Details\n\t\t\t3.Transaction\n\t\t\t4.Report\n\t\t\t5.Exit")
    choice = int (input())
    if choice == 1:
        while(True):
            print("\t\t\t\tEnter Your Choice\n\t\t\t1.Add Book Details\n\t\t\t2.Edit Book Details\n\t\t\t3.Delete A Book\n\t\t\t4.Search A Book\n\t\t\t5.Back To Main Menu")
            ch = int(input())
            if ch==1:
                book_input()
            elif ch== 2:   
                book_edit()  
            elif ch== 3:
                book_delete()
            elif ch== 4:
                book_search()
            elif ch== 5:
                break 
    elif choice == 2:   
        while(True):
            print("\t\t\t\tEnter Your Choice\n\t\t\t1.Add Member Details\n\t\t\t2.Edit Member Details\n\t\t\t3.Delete A Member\n\t\t\t4.Search A Member\n\t\t\t5.Back To Main Menu")
            ch = int(input())
            if ch==1:
                member_input()
            elif ch== 2:   
                member_edit()
            elif ch== 3:
                member_delete()
            elif ch== 4:
                member_search()
            elif ch== 5:
                break 
    elif choice == 3:
        while(True):
            print("\t\t\t\tEnter Your Choice\n\t\t\t1.Issue A Book\n\t\t\t2.Return A Book\n\t\t\t3. Back To Main Menu")
            ch = int(input())
            if ch==1:
                book_issued()
            elif ch== 2:   
                book_returns()
            elif ch== 3:
                break 
    elif choice == 4:
        while(True):
            print("\t\t\t\tEnter Your Choice\n\t\t\t1.Book Details\n\t\t\t2.Member Details\n\t\t\t3. Issue Details\n\t\t\t4. Return Details\n\t\t\t5. Best Reading Book (Chart)\n\t\t\t6. Back To Main Menu")
            ch = int(input())
            if ch==1:
                book_output()
            elif ch== 2:   
                member_output()
            elif ch== 3:
                return_output()
            elif ch== 4:
                issue_output()
            elif ch== 5:
                col_chart()
            elif ch== 6:
                break
    elif choice == 5:
        break 