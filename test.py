import jpysocket
import socket

host = '192.168.1.4' #Host Name
port = 5560    #Port Number

s=socket.socket() #Create Socket
s.bind((host,port)) #Bind Port And Host
s.listen(5) #Socket is Listening
print("Socket Is Listening....")
connection,address=s.accept() #Accept the Connection
print("Connected To ",address)
msgsend=jpysocket.jpyencode("Thank You For Connecting.") #Encript The Msg
connection.send(msgsend) #Send Msg
msgrecv=connection.recv(1024) #Recieve msg
msgrecv=jpysocket.jpydecode(msgrecv) #Decript msg
print("From Client: ",msgrecv)
s.close() #Close connection
print("Connection Closed.")