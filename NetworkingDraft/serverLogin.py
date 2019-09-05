# Author:       Jake Klein and Zachary Garner    
#Jake worked on the Login and SignUp Procedures
# Zack worked on editing it to go with the gui a little better and
# added the play funcitonality as well as the ability to quit
#
from socket import *
from _thread import *
serverPort = 12007 #Make sure it matches the port number specified in the client side
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(30)
USER = ""
PASS = ""
ID = ""
print ('The server is ready to receive')

def connectionProcessing(connectionSocket):
     request = connectionSocket.recv(1024)
     toDo = True
     while(toDo):
          print("Received: ")
          print(request)

          method = request.decode("ascii").split("\t")[0].strip()
          
          #If the method name is Login
          if (method == "Login"):
               success = False
               invalidPassword = False
               #obtain the second field (user name) and third field (Password)
               userName = request.decode("ascii").split("\t")[2].strip()
               USER = userName
               password = request.decode("ascii").split("\t")[3].strip()
               PASS = password
               #Check the password file to see whether the user name and password match the record or not
               inputFile = open("password.txt", 'r') #open the file for reading
               for lines in inputFile.readlines():
                    #Each line has the format: userName \t password. Split them to get info
                    readUsername = lines.split("\t")[0].strip()
                    #If the user name in this line matches the login usernmae
                    if (userName == readUsername):
                        readPassword = lines.split("\t")[1].strip()
                        #Check whether the password matches
                        if (password == readPassword):
                            success = True
                        else:
                             invalidPassword = True

               #If it did not find the login  username in any record of the password file, record this error
               if (success == False):
                 response = "LoginResponse"+"\t" + "No profile found" +"\n\r"
               inputFile.close()
               #Prepare the response message correspondingy.
               if (success == True):
                    #For successful login, the response is "Success"
                    response = "LoginResponse"+"\t" + "Success"
               elif (invalidPassword == True):
                   response = "LoginResponse"+"\t" + "Incorrect Password" +"\n\r"
               connectionSocket.send(response.encode())
               #Continue within Login only returning to the outer while when Logout
               #Make Logout the next first part recieving at correct intervalse
               
               if(response.split("\t")[1].strip()=="Success"):
                    insideMsg= connectionSocket.recv(1024)
                    toContin = True
                    while(toContin):
                         if(insideMsg.decode("ascii").split("\t")[0].strip() == "Logout"):
                              logoutResponse = "Logout" +"\n\r"
                              connectionSocket.send(logoutResponse.encode())
                              toContin = False
                              print("Logged Out " + USER)
                              break
                         if(insideMsg.decode("ascii").split("\t")[0].strip() == "Quit"):
                              method = "Quit"
                              toDo = False
                              toContin = False
                              break
                         if(insideMsg.decode("ascii").split("\t")[0].strip() == "PlayGame"):
                              response = "PlayGame" + "\t" +  "Continue" + "\n\r"
                              connectionSocket.send(response.encode())
                              scoreMsg = connectionSocket.recv(1024)
                              if(scoreMsg.decode("ascii").split("\t")[0].strip() == "Quit"):
                                   method = "Quit"
                                   toDo = False
                                   toContin = False
                                   break
                              elif(scoreMsg.decode("ascii").split("\t")[0].strip() == "Logout"):
                                   logoutResponse = "Logout" +"\n\r"
                                   connectionSocket.send(logoutResponse.encode())
                                   toContin = False
                                   break
                              elif(scoreMsg.decode("ascii").split("\t")[0].strip() == "Score"):
                                   invalid = False
                                   myScore = scoreMsg.decode("ascii").split("\t")[1].strip()
                                   #Append a play record into the file "record.txt"
                                   outFile = open("record.txt","a+")
                                   #Get the new record ready, just need the IP address, not port #
                                   newRecord = str(addr[0])+"\t"+str(USER)+"\t"+str(PASS)+"\t"+str(myScore) + "\n"
                                   print(newRecord)
                                   outFile.write(newRecord)
                                   outFile.close()
                                   response = "Score" + "\t" +  "Recieved" + "\n\r"
                                   connectionSocket.send(response.encode())
                         if(insideMsg.decode("ascii").split("\t")[0].strip() == "GetScore"):
                              try:
                                 outFile = open("record.txt", "r")
                              except FileNotFoundError:
                                 errorMsg = ("NoScore" + "\t"+"Error" + "\t"+ "there are no records of this user in our systems." + "\n\r")
                                 connectionSocket.send(errorMsg.encode())
                              else:
                                 hit = 0
                                 allOutput = ""
                                 for line in outFile.readlines():
                                     if(USER == line.split('\t')[1].strip() and PASS == line.split('\t')[2].strip()):
                                         #print out all play records from this special IP address
                                         allOutput = allOutput + line.strip() + "\n"
                                         hit = hit + 1
                                 if(hit != 0):
                                     connectionSocket.send(("Returned Score" + "\n" +allOutput).encode())
                                 else:
                                     noPerson = "No records exist"
                                     connectionSocket.send(("NoScore" + "\t" + noPerson).encode())
                                 outFile.close()
                         if(method != "Quit"):
                              insideMsg= connectionSocket.recv(1024)
                         if(method == "Quit"):
                              print("Logged Out" + USER)
           
          elif (method == "SignUp"):
               invalid = False
               userName = request.decode("ascii").split("\t")[2].strip()
               password = request.decode("ascii").split("\t")[3].strip()
               #Check the password file to see whether or not the user name already exists
               inputFile = open("password.txt", 'r') #open the file for reading
               for lines in inputFile.readlines():
                    #Each line has the format: userName \t password. Split them to get info
                    readUsername = lines.split("\t")[0].strip()
                    #If the user name in this line matches the login usernmae
                    if (userName == readUsername):
                         response = "SignUp" + "\t" + "Username already exists" +"\n\r"
                         invalid = True
                    else:
                         inputFile.close()
               if (invalid == False):
                    inputFile = open("password.txt", 'a')
                    # create the profile in the file
                    inputFile.write("\n" + userName + "\t" + password)
                    response = "SignUp" + "\t" + "Success" +"\n\r"
                    inputFile.close()

               connectionSocket.send(response.encode())
          if (method == "Quit"):
               toDo = False
               break
          request = connectionSocket.recv(1024)
     print("Connection Closed")
     connectionSocket.close()



while 1:
     connectionSocket, addr = serverSocket.accept()
     print("From:", addr)
     #Change the following sentence to make the server support multiple thread
     start_new_thread(connectionProcessing,(connectionSocket,))
     #connectionProcessing(connectionSocket)

     

