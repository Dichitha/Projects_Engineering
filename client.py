import socket, ssl
import tkinter as tk
import pickle
import sys
import ipaddress

root = tk.Tk()
root.geometry('500x300')
root.title('Client')
root.configure(bg='light blue')

# set the default font size
default_font = ('Times New Roman', 14)

# create a label and entry box for the server address
server_label = tk.Label(root, text='Server IP address:', bg='light blue', font=default_font)
server_label.pack()

server_entry = tk.Entry(root, font=default_font)
server_entry.pack()

# create a label and entry box for the client address
client_label = tk.Label(root, text='Target IP address:', bg='light blue', font=default_font)
client_label.pack()

message_entry = tk.Entry(root, font=default_font)
message_entry.pack()

# create a label and entry boxes for the starting and ending ports
from1_label = tk.Label(root, text='Starting port:', bg='light blue', font=default_font)
from1_label.pack()

message_entry1 = tk.Entry(root, font=default_font)
message_entry1.pack()

to1_label = tk.Label(root, text='Ending port:', bg='light blue', font=default_font)
to1_label.pack()

message_entry2 = tk.Entry(root, font=default_font)
message_entry2.pack()

# create a label to display the available ports
result_label = tk.Label(root, text='', bg='light blue', font=default_font)
result_label.pack()

def is_valid_ipv4(ip):
     try:
         ipaddress.IPv4Address(ip)
         return 1
     except ValueError:
         return 0
     
def err(ip):
    print("The IP address "+ip+" is invalid ")

def send_message():
    server_address = server_entry.get()
    client_address = message_entry.get()
    from1 = message_entry1.get()
    to1 = message_entry2.get()
    if int(to1)>=65536:
        print("Limit exceeded")
        sys.exit()
    if int(from1)<0:
        print("Starting port number is invalid!")
        sys.exit()
    if int(to1<from1):
        print("Ending port should be greater than starting port")
        sys.exit()

    if (is_valid_ipv4(server_address)==0):
        err(server_address)
        sys.exit()
    elif(is_valid_ipv4(client_address)==0):
        err(client_address)
        sys.exit()
    else:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_address, 8100))
        data = (client_address, from1, to1)
        tup = pickle.dumps(data)
        client_socket.send(tup)

        # receive data from the server
        data = client_socket.recv(1024)
        print("Received data: ", data.decode())

        # receive the pickled list from the server
        pickled_list = client_socket.recv(1024)

        # unpickle the list
        my_list = pickle.loads(pickled_list)

        if len(my_list) == 0:
            # display "No available ports" if there are no available ports
            result_label.config(text=f"No available ports for {server_address} ({from1}-{to1})")
        else:
            # display the available ports
            result_label.config(text=f'Available ports: {my_list}')
        

        # close the connection
        client_socket.close()
        print("Port scanning is completed!")

    
send_button = tk.Button(root, text='Send', command=send_message, bg='orange', font=default_font)
send_button.pack()

# start the Tkinter event loop
root.mainloop()