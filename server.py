import socket
from datetime import datetime
import sys
import threading
from queue import Queue
import pickle

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host=socket.gethostname()
port=8100

try:
    serversocket.bind(('0.0.0.0', 8100))
except socket.error as e:
    print(str(e))
print("Waiting for the connection")

serversocket.listen(10)

print("Listening on " + str(host) + ":" + str(port))

def scan_port(host, port, result_queue):
    """
    This function scans a single port on the specified host and adds the result to a queue.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) # set timeout to 1 second
        sock.connect((host, port))
        result_queue.put(port)
        sock.close()
    except (socket.timeout, ConnectionRefusedError):
        pass

def scan_ports(host, start_port, end_port, num_threads):
    """
    This function scans a range of ports on the specified host using multiple threads.
    """
    # create a queue to store the results of each scan
    result_queue = Queue()
    
    # create a list of threads to perform the scans
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=scan_worker, args=(host, start_port, end_port, num_threads, i, result_queue))
        t.start()
        threads.append(t)
    
    # wait for all threads to finish
    for t in threads:
        t.join()
    
    # get the results from the queue and return them as a sorted list
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    results.sort()
    return results

def scan_worker(host, start_port, end_port, num_threads, thread_num, result_queue):
    """
    This function is called by each worker thread to scan a portion of the port range.
    """
    for port in range(start_port + thread_num, end_port + 1, num_threads):
        scan_port(host, port, result_queue)


def handle_client(client_socket):
    client_socket.send("Connection Established".encode())

    # receive data from the client
    
    data_received = False

    while not data_received:
        try:
            # receive the pickled tuple from the client
            pickled_data = client_socket.recv(1024)
            if pickled_data:
                # unpickle the tuple
                data = pickle.loads(pickled_data)
                host1 = data[0]
                from2 = data[1]
                to2 = data[2]
                target = socket.gethostbyname(host1)
                print("Scanning Target: " + target)
                print("Scanning started at:" + str(datetime.now()))
                l = []
                try:
                    from1 = int(from2)
                    to1 = int(to2)
                    threads=2
                    open_ports=scan_ports(host,from1,to1,threads)
                    l=[i for i in open_ports]
                    # pickle the list
                    pickled_list = pickle.dumps(l)

                    # send the pickled list to the client
                    client_socket.send(pickled_list)
                    client_socket.send("Port scanning successfully done".encode())

                except KeyboardInterrupt:
                    print("\n Exiting Program !!!!")
                    sys.exit()
                except socket.gaierror:
                    print("\n Hostname Could Not Be Resolved !!!!")
                    sys.exit()
                except socket.error:
                    print("\ Server not responding !!!!")
                    sys.exit()

                # set data_received to True to exit the loop
                data_received = True

        except:
            # wait for some time before trying again
            pass
    # close the connection
    client_socket.close()


def accept_clients():
    while True:
        # accept a client connection
        client_socket, client_address = serversocket.accept()
        print('Connected to:', client_address)

        # start a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# start accepting client connections in a separate thread
accept_thread = threading.Thread(target=accept_clients)
accept_thread.start()