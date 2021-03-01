import os , base64
import cryptography
from cryptography.fernet import Fernet as f
import pyfiglet as fb
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import threading
import time
from math import ceil
from termcolor import colored as c

def password(passwd):
    
    password = passwd.encode() # Convert to type bytes
    salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
            )
    k = base64.urlsafe_b64encode(kdf.derive(password))
    return k



def enc_fun(key,file):
    try:
    
        with open(file,"rb") as fname:
            data = fname.read()
        fl,ext = os.path.splitext(file)
        fkey = f(key)
        enc = fkey.encrypt(data)
        with open(str(fl[0:])+ext+'.en','wb') as encfile:
            encfile.write(enc)
        os.remove(file)
        print("                      ")
        print(f"->file encrypted sucessfully ")
        print("                               ") 
        print(f"-> {file} ==> {str(fl[0:])+ext+'.en'}")
        
    except Exception as e:
        print("                      ")
        print("-> some thing went wrong",e)

def dec_fun(key,file):
    try:
        
        with open(file, "rb") as fname:
            data = fname.read()
        fkey = f(key)
        fl,ext = os.path.splitext(file)
        dec = fkey.decrypt(data)
        with open(str(fl[0:]), 'wb') as decfile:
            decfile.write(dec)
        os.remove(file)
        print("                      ")
        print(f"-> file decrypted sucessfully")
        print("                             ")
        print(f"->{file} ==> {fl[0:]}")
    
    except:
        print("                      ")
        print("-> some thing went wrong ")


def banner():
     b = fb.figlet_format("CryTool",font='graffiti')
     a = fb.figlet_format("Ashwin kanojia",font='digital')
     return print(c(b,'green'),c(a,'blue'))



def main():
    banner()
    while True:
        
        print('')
        choice = input("->Enter your choice encrypt or decrypt (e/d/q) :").lower()
        listOfFiles = list()
       
        if choice=='e':
            print("                      ")
            file_input = input("->Enter full path of Targeted file or Dir :")
            print(" ")
            if os.path.exists(file_input):
                if file_input !="":
                    passwd = input("->Enter your password to encrypt the data :")
                    start = time.time()
                    if os.path.isfile(file_input)==False:
                        for (dirpath, dirnames, filenames) in os.walk(file_input):
                            listOfFiles += [os.path.join(dirpath, file) for file in filenames]
                        for l in listOfFiles:    
                            x= threading.Thread(target=enc_fun,args=(password(passwd),l))
                            x.start()
                            x.join()
                    else :
                        enc_fun(password(passwd),file_input)
                    print('')
                    print("->Time taken to encrypt :",ceil(time.time()-start),'sec')
                else:
                    print("->Enter full path")
            else:
                print("->Path Doesn't exists")

        elif choice=='d':
            print("                      ")
            file_input = input("->Enter full path of Targeted file or Dir :")
            if os.path.exists(file_input):
                print(" ")
                if file_input !="":
                    passwd = input("->Enter your password to decrypt the data :")
                    start = time.time()
                    if os.path.isfile(file_input)==False:
                        for (dirpath, dirnames, filenames) in os.walk(file_input):
                            listOfFiles += [os.path.join(dirpath, file) for file in filenames]
                        for l in listOfFiles:    
                            x = threading.Thread(target=dec_fun,args=(password(passwd),l))
                            x.start()
                            x.join()
                    else:
                        dec_fun(password(passwd),file_input)
                    print('')
                    print("->Time taken to decrypt :",ceil(time.time()-start),'sec')
                else:
                    print("->Enter full path")
            else:
                print("->Path Doesn't exists")


        elif choice=="q" or choice=='quit':
            break
        else:
            print(" ")
            print("->please enter a valid Choice !!")


if __name__=="__main__":
    main()
