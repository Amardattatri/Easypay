import mysql.connector as a
import PySimpleGUI as sg
import smtplib
con=a.connect(host="localhost",user="root",passwd="root123",database="sbi")

def create_acc():
    layoutc=[
        [sg.Text("Enter the details here:")],
        [sg.Text('name',size=(15,1)),sg.InputText()],
         [sg.Text('accno',size=(15,1)),sg.InputText()],
         [sg.Text('Open_bal',size=(15,1)),sg.InputText()],
         [sg.Text('adds',size=(15,1)),sg.InputText()],
         [sg.Text('userid',size=(15,1)),sg.InputText()],
         [sg.Text('passwd',size=(15,1)),sg.InputText()],
        [sg.Submit(),sg.Cancel()]
        ]
    windowc=sg.Window('Create',layoutc)
    eventc,valuec=windowc.read()
    data1=(valuec[0],valuec[1],valuec[2],valuec[3],valuec[4],valuec[5])
    data2=(valuec[0],valuec[1],valuec[2])
    sql1='insert into account values(%s,%s,%s,%s,%s,%s)'
    sql2='insert into amount values(%s,%s,%s)'
    c=con.cursor()
    c.execute(sql1,data1)
    c.execute(sql2,data2)
    con.commit()
    windowc.close()
    
def sendMailc(reciver,amount):
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login("chaitukd0@gmail.com","indraJEt@4356(py.)!$")
    msg='Your account has been creited with '+amount
    server.sendmail("chaitukd0@gmail.com",str(reciver),msg)
    server.quit()
    
def sendMailr(reciver,amount):
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login("chaitukd0@gmail.com","indraJEt@4356(py.)!$")
    msg='Your account has been debited for '+amount
    server.sendmail("chaitukd0@gmail.com",str(reciver),msg)
    server.quit()
    
def EasyPay():
    layoutep=[
        [sg.Text("USER ID",size=(15,1)),sg.InputText()],
        [sg.Text("PASSWORD",size=(15,1)),sg.InputText()],
        [sg.Submit(),sg.Cancel()]
        ]
    layoute2=[
        [sg.Text("RECIVER USERID",size=(15,1)),sg.InputText()],
        [sg.Text("Pay $",size=(15,1)),sg.InputText()],
        [sg.Submit(),sg.Cancel()]
       # [sg.Text("RECIVER ACCOUNT NO.",size=(15,1)),sg.InputText()]
        ]  
    windowep=sg.Window("Login",layoutep)
    eventep,valueep=windowep.read()
    a='select accno,obal from account where userid=%s and passwd=%s'
    data=(valueep[0],valueep[1])
    c=con.cursor()
    c.execute(a,data)
    myresult=c.fetchone()
    if myresult is not None:
        window2=sg.Window("PaySecure",layoute2)
        event2,value2=window2.read()
        b='select obal,accno from account where userid=%s'
        bata=(value2[0],)
        c2=con.cursor()
        c2.execute(b,bata)
        result=c2.fetchone()
        if result is not None:
            tm=int(result[0]) + int(value2[1])
            tm1=int(myresult[1]) -int(value2[1])
            sql1='update account set obal=%s where accno=%s'
            sql2='update account set obal=%s where accno=%s'
            sendMailc(value2[0],value2[1])
            sendMailr(valueep[0],value2[1])
            d=(tm,result[1])
            d1=(tm1,myresult[0])
            c.execute(sql1,d)
            c.execute(sql2,d1)
            con.commit()
    
def deposit():
    am=int(input("Enter the deposit Amount:"))
    ac=input("Enter the account no:")
    a="select obal from amount where accno=%s"
    data=(ac,)
    c=con.cursor()
    c.execute(a,data)
    myresult=c.fetchone()
    tam= int(myresult[0]) + am
    sql='update amount set obal = %s where accno=%s'
    d=(tam,ac)
    c.execute(sql,d)
    con.commit()
   # login()

def withdraw():
    am=int(input("enter the ammount:"))
    ac=input("Enter the account number:")
    if(am<int(ac)):
        a='select obal from amount where accno =%s'
        ac=str(ac)
        data=(ac,)
        c=con.cursor()
        c.execute(a,data)
        myresult=c.fetchone()
        tam=int(myresult[0]) - am
        sql ='update amount set obal=%s where accno=%s'
        d=(tam,ac)
        c.execute(sql,d)
        con.commit()
    #login()

def chk_bal():
    ac=input("enter account number to check balance:")
    a='select obal from amount where accno=%s'
    data=(ac,)
    c=con.cursor()
    c.execute(a,data)
    myresult=c.fetchone()
    print("Your Balance in account no>:",ac,"is",myresult[0])
    #login()

def dispacc():
    ac=input("Enter the account number:")
    a='select * from account where accno=%s'
    data=(ac,)
    c=con.cursor()
    c.execute(a,data)
    myresult=c.fetchone()
    for i in myresult:
        print(i,end=" ")
   # login()

def close():
    ac=input("Enter the account No.:>")
    sql1='delete from account where accno=%s'
    sql2='delete from amount where accno=%s'
    data=(ac,)
    c=con.cursor()
    c.execute(sql1,data)
    c.execute(sql2,data)
    con.commit()
    print("The account is deleted .....!")
    login()
    
def login():
    sg.theme('SandyBeach')
    layout=[
        [sg.Button('Create Account',size=(15,2))],
        [sg.Button("Display Details",size=(15,2))],
        [sg.Button("Check Balance",size=(15,2))],
        [sg.Button("Transfer",size=(15,2))],
        [sg.Button("WithDraw Money",size=(15,2))],
        [sg.Button("Make Deposit",size=(15,2))],
        [sg.Button("Close Account",size=(15,2))]
        ]
    window =sg.Window("PAYPAL PAGE",layout,background_color='Skyblue',margins=(90,70),resizable=True)
    while True:
        event,value=window.read()
        if event=="Create Account":
            create_acc()
        elif event =="Display Details":
            dispacc()
        elif event=="Transfer":
            EasyPay()
    window.close()

login()