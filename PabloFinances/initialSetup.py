import mysql.connector as msq
from pickle import *
import keyboard
import os

tableQuery = '''
create table tBankDb(
ID char(7) primary key,
cName varchar(50),
Age int,
Balance int default 0,
Password varchar(30)
);

'''

adminCondition = 0
keyboard.press('f11')
while True:
    
    print('This is a Prompt to Set up Your Bank Database')
    
    cond = input('Enter (1) to Start Setup \n(2) to exit\n')
    try:
        if cond =='2':
            keyboard.press('f11')
            os.system('cls')
            break 
            
        elif cond =='1':
            setHost = input('Enter Hostname: ')
            setUser = input('Enter Username: ')
            setPass = input('Enter Password: ')
            setDb = input('Enter Template Database(Make sure it exists): ')
            
            
            with open(r'mysqCreds.txt','wb') as hostobj:
                
                dump(setHost, hostobj)
                dump(setUser, hostobj)
                dump(setPass, hostobj)
                dump(setDb, hostobj)
            
            testcon= msq.connect(host=setHost,username = setUser,\
                                 passwd = setPass, database = setDb )

            csr  = testcon.cursor(buffered = True)
            
            
            csr.execute(tableQuery)
            
            
            adminCondition = 1
            os.system('cls')
            break
        
    except msq.errors.DatabaseError :
    
        print('''Cannot execute action
Either credentials are wrong or Database is Non-Exsistent/ Non-Empty''')
        print('\n\n\n\n')
        checkInp = input('Press Enter to Continue')
        os.system('cls')
        continue
        
        
if adminCondition ==1:
    print('\n\n')
    adminName = input('Enter Admin Name : ')
    adminPass = input('Create Admin Password : ')
    
    with open(r'adminCreds.txt','wb') as adminobj:
        
        dump(adminName, adminobj)
        dump(adminPass, adminobj)
        
        csr.execute('commit;')
        testcon.close()
        
        print('\n\nBank Database Ready to be Deployed')
        testkey = input('Press Enter')
        keyboard.press('f11')
        
    
    
 
