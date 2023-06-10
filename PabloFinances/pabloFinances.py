#A BANKING DATABASE SIMULATION BY Daksh Thakur

#importing modules

from random import *
from pickle import*
from time import *
import mysql.connector as msq
import os
import csv
import keyboard

#setting up sql connection and cursor object

with open(r'mysqCreds.txt','rb') as hostobj:
    
    lHost = load(hostobj)
    uName = load(hostobj)
    pWord = load(hostobj)
    dBase = load(hostobj)



testcon= msq.connect(host= lHost,username = uName, passwd = pWord, database = dBase)

csr  = testcon.cursor(buffered = True)


#generates a random ID of form YYXXXXX where Y is an alphabet and x is a number
#returns the generated ID

def idGenerator():
    
    numFinal = ''
    charFinal = ''
        
    for i in range(2):
        charChoice = choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        charFinal += charChoice
                
    for j in range(5):
        numChoice = randint(0,9)
        numChoice = str(numChoice)
        numFinal += numChoice
        
    randomId = charFinal + numFinal
    
    return randomId


#uses the idGenerator() function to generate an ID
#iterates through the database to confirm that the new ID is unique
#generates a new ID untill it confirms that the ID is unique
#returns the new unique ID

def newIdConfirm():
    csr.execute('select ID from tBankDb')
    idlist = csr.fetchall()
     
    while True:
        genid = idGenerator()
         
        for i in idlist:
            if genid == i:
                break
            
        else:
            
            print('Your ID is: ', genid)
            
            print('''Caution: It Cannot Be Retrieved If Lost
and is Required to Log into Your Account''')
            
            return genid
            
 
#login prompt for administrator: asks for admin password
#gives admin access if admin password matches

def adminLogin():
    with open('adminCreds.txt','rb') as passobj:
        
        adminPass = load(passobj)
        adminPass = load(passobj)
          
    askPass = input('Enter Admin Password: ')
    
    if askPass == adminPass:
        
        print('Access Granted!')
        sleep(0.4)
        os.system('cls')
        
        return 1
    
    else:
            print('Wrong Password!')
            sleep(0.4)
            os.system('cls')
            
            return 0


#all the commands that the admin has access to
#can view the client database : opens an excel file of the database


def adminAccess():
    
    with open(r'adminCreds.txt','rb') as nameobj:
        
        adminName = load(nameobj)
        
        print('\t\t\t\t\t\t\t\t\t\t Welcome {}!'.format(adminName))
        print('\n\n\n\n')    
        
    while True:
         
        try:
            admOpt = int(input('(1)View Database\n(2)Exit Database\n'))
            if admOpt == 2:
                
                print('Logging Out of Administrative Account', end = '')
                
                for i in range(5):
                    print('.', end = '', flush = True)
                    sleep(0.4)
                    
                print('\n\n\n\n')
                os.system('cls')
                break
        
            elif admOpt == 1:
                print('Accessing Administrative Database', end = '')
                
                for i in range(5):
                    print('.',end = '', flush=True)
                    sleep(0.4)
                    
                os.startfile(r'bankDb.csv')
                os.system('cls')
    
            else:
                print('Invalid Input!')
                sleep(0.5)
                os.system('cls')
    
        except ValueError:
            print('Invalid Input!')
            sleep(0.5)
            os.system('cls')
    
      
#a prompt to create a new account : asks for name, age and a password
#age cannot be less than 18, password has to be between 4 and 30
#uses the newIdConfirm() function to give the client a new unique ID
#creates a new entry of the client's credentials in the sql database           
    
def newAcc():
    
    while True:
        
        newName = input('Enter Name: ')
        if len(newName) != 0:
            break 
        
        else:
            print('This Field Cannot Be Empty!')
    
    while True:
        
        try:
            newAge = int(input('Enter Age: '))
            
            if newAge < 18:
                print('Only Ages of 18 and Above Can Register!')
                
            else:
                break 
    
        except ValueError:
            print('Invalid Age!')


    while True:
        newPass = input('Create Password: ')
        
        if len(newPass) < 4 :
            print('Password Cannot be Less Than Four Characters')
            
        elif len(newPass) >= 30:
            print('Password Cannot be More Than Thirty Characters')
            
        else:
            break
        
    newId = newIdConfirm()
       
    print('Registering Account',end = '')
    for i in range(4):
        print('.',end = '', flush = True)
    
    csr.execute('''insert into tBankDb (ID,cName,Age,Password)
values('{}','{}',{},'{}');'''.format(newId,newName,newAge,newPass))
    csr.execute('commit;')
                  
    print('\n\n\n Account Registered!')
    
    checkinp = input('Login as Client Through Main Menu, Press Enter\n')
    os.system('cls')
    
    
#login prompt for client: asks for client ID and password
#gives client access if ID exists and corresponding password matches    

def clientLogin():
    
    idCondition = 0
    
    loginId = input('Enter ID: ').upper()
    loginPass = input('Enter Password: ')
    
    csr.execute('select ID from tBankDb;')
    idList = csr.fetchall()
    
    for i in idList:
        if loginId != i[0]:
            continue
            
        else:
            idCondition = 1
            break
        
    else:
        print('ID not Found!')
              
    if idCondition == 0:
        sleep(0.4)
        os.system('cls')
        
        return [0]
    
    elif idCondition == 1:
        csr.execute(f'select Password from tBankDb where ID = \'{loginId}\';')
        passList = csr.fetchall()
        
        if passList[0][0] == loginPass:
            print('Access Granted!')
            sleep(0.4)
            os.system('cls')
            return 1, loginId
        
        else:
            print('Wrong Password!')
            sleep(0.4)
            os.system('cls')
            return [0]


#all the commands that the client has access to
#can view account balance, deposit and withdraw money, change name    
def clienAccess():
    
    
    clientId = clCredtp[1]   #this is the tuple of the returned values from clientLogin()
    
    csr.execute(f'select cName from tBankDb where ID = \'{clientId}\';')
    nameList = csr.fetchall()
    clientName = nameList[0]
      
    print(f'\t\t\t\t\t\t\t\t\t\t Welcome {clientName[0]} !')
    print('\n\n\n\n')
      
    while True:
        
        try:
            
            clOpt = int(input('''(1)View Balance
(2)Deposit Money
(3)Withdraw Money
(4)Change Name
(5)Log Out of Account
'''))
            
            
            if clOpt == 5:
                print('Logging Out of Account', end = '')
                
                for i in range(5):
                    print('.', end = '', flush = True)
                    sleep(0.4)
                    
                print('\n\n\n\n')
                os.system('cls')
                break
                  
            elif clOpt == 1:
                csr.execute(f'select Balance from tBankDb where ID = \'{clientId}\';')
                balanceList = csr.fetchall()
                clientBalance = balanceList[0][0]
                
                print(f'Your Current Balance is: {clientBalance}')
                checkInput = input('\n\n\n\nPress Enter to Continue\n')
                os.system('cls')
                           
            elif clOpt == 2:
                try:
                    depSum = abs(int(input('Enter Amount to be Deposited: ')))
                    
                    csr.execute('''update tBankDb set Balance = Balance + {}
where ID = \'{}\''''.format(depSum, clientId))
                    
                    csr.execute('commit')
                    
                    print(f'{depSum} Successfully Deposited Into Your Account')
                
                    checkInput = input('\n\n\n\nPress Enter to Continue\n')
                    os.system('cls')
                    
                except ValueError:
                    print('Invalid Input!')
                    sleep(0.5)
                    os.system('cls')     
                        
            elif clOpt == 3:
                
                try:
                    witSum = abs(int(input('Enter Amount to be Withdrawn: ')))
                    
                    csr.execute(f'select Balance from tBankDb where ID = \'{clientId}\';')
                    balList = csr.fetchall()
                    clientbal = balList[0][0]
                                        
                    if witSum > clientbal:
                        print('Not Enough Money In Your Account!')
                        sleep(0.5)
                        os.system('cls')
                    else:
                            
                        csr.execute('''update tBankDb set Balance = Balance - {}
where ID = \'{}\''''.format(witSum, clientId))
                            
                        csr.execute('commit')
                        
                        print(f'{witSum} Successfully Withdrawn From Your Account')
                        
                        checkInput = input('\n\n\n\nPress Enter to Continue\n')
                        os.system('cls')
                                         
                except ValueError:
                    print('Invalid Input!')
                    sleep(0.5)
                    os.system('cls')                
                
            elif clOpt == 4:
                    while True:
                        clNewName = input('Enter Name: ')
                        if len(clNewName) != 0:
                            
                            csr.execute('''update tBankDb set cName = \'{}\'
where id = \'{}\''''.format(clNewName, clientId))
                            
                            csr.execute('commit')
                            
                            print('Name Changed Successfully!')
                            sleep(0.5)
                            os.system('cls')
                            
                            break 
                        else:
                            print('This Field Cannot Be Empty!')
                
            else:
                print('Invalid Input!')
                sleep(0.5)
                os.system('cls')
  
        except ValueError:
            print('Invalid Input!')
            sleep(0.5)
            os.system('cls')        


#a function to update the admin table 
def excelUpdate():
    csr.execute('select ID, cName, Age, Balance from tBankDb;')
    excelDb = csr.fetchall()
            
    with open('bankDb.csv','w', newline = '') as cobj:
                
        wobj = csv.writer(cobj)
        wobj.writerow(['ID', 'Name', 'Age', 'Balance'])
        wobj.writerows(excelDb)
        cobj.flush()


# __main__

keyboard.press('f11')
print('\t\t\t\t\t\t\t\t\t\t _-PABLO FINANCES-_')
print('\n\n\n\n')
    

exitCon = 0
while exitCon == 0:
    excelUpdate()
    try:
        
        bankOpt = int(input('''(1)Create New Account
(2)Log Into Account
(3)Log In As Administrator
(4)Exit
'''))
        
        if bankOpt == 1:
            os.system('cls')
            newAcc()
        
        elif bankOpt == 2:
            os.system('cls')
            clCredtp = clientLogin()
            if clCredtp[0] == 1:
                clienAccess()

        elif bankOpt == 3:
            os.system('cls')
            adminCred = adminLogin()
            if adminCred == 1:
                adminAccess()
                         
        elif bankOpt == 4:
                
            print('Exiting Application')
            sleep(0.5)
            os.system('cls')
            keyboard.press('f11')
            
            exitCon = 1
            break
            
    except ValueError:
        print('Invalid Input!')
        sleep(0.5)
        os.system('cls')
        
                    