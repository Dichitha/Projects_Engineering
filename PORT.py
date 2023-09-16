import socket
import sys
import threading
import time
from tkinter import *
from PIL import Image, ImageTk



# ==== Scan Vars ====
ip_s = 1
ip_f = 1024
log = []
ports = []
target = 'localhost'

# ==== Scanning Functions ====


def scanPort(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        c = s.connect_ex((target, port))
        if c == 0:
            m = ' Port %d \t[open]' % (port,)
            log.append(m)
            ports.append(port)
            listbox.insert("end", str(m))
            updateResult()
        s.close()
    except OSError:
        print('> Too many open sockets. Port ' + str(port))
    except:
        c.close()
        s.close()
        sys.exit()
    sys.exit()


def updateResult():
    rtext = " [ " + str(len(ports)) + " / " + str(ip_f) + " ] ~ " + str(target)
    L27.configure(text=rtext)


def startScan():
    global ports, log, target, ip_f
    clearScan()
    log = []
    ports = []
    # Get ports ranges from GUI
    ip_s = int(L24.get())
    ip_f = int(L25.get())
    # Start writing the log file
    log.append('> Port Scanner')
    log.append('='*14 + '\n')
    log.append(' Target:\t' + str(target))

    try:
        # target = socket.gethostbyname(str(L22.get()))
        target_ip = socket.gethostbyname(target)
        log.append(' IP Adr.:\t' + str(target))
        log.append(' Ports: \t[ ' + str(ip_s) + ' / ' + str(ip_f) + ' ]')
        log.append('\n')
        # Lets start scanning ports!
        while ip_s <= ip_f:
            try:
                scan = threading.Thread(target=scanPort, args=(target, ip_s),daemon=True)
                scan.setDaemon(True)
                scan.start()
            except:
                time.sleep(0.01)
            ip_s += 1
    except:
        m = '> Target ' + str(L22.get()) + ' not found.'
        log.append(m)
    listbox.insert(0, str(m))


def saveScan():
    global log, target, ports, ip_f
    log[5] = " Result:\t[ " + str(len(ports)) + " / " + str(ip_f) + " ]\n"
    with open('portscan-'+str(target)+'.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(log))


def clearScan():
    listbox.delete(0, 'end')


# ==== GUI ====
gui = Tk()
gui.title('Port Scanner')
screen_width = gui.winfo_screenwidth()
screen_height = gui.winfo_screenheight()
gui.geometry(f"{screen_width}x{screen_height}+0+0")
# Set the colors
# ==== Colors ====
mlc = '#000000'
bgc = '#F9EBEA'
dbg = '#000000'
fgc = '#000000'

# Configure tkinter theme colors
gui.configure(bg=bgc)
gui.option_add("*Font", "Helvetica")
gui.option_add("*Label.Font", "Helvetica 12 bold")
gui.option_add("*Button.Font", "Helvetica 12 bold")
gui.option_add("*Entry.Font", "Helvetica 12")


gui.tk_setPalette(background=bgc, foreground=mlc, activeBackground=fgc,
                  activeForeground=bgc, highlightColor=mlc, highlightBackground=mlc)
# replace "path/to/your/image.jpg" with the actual path of your image file


# Add labels with updated colors
# Add labels with updated colors and centered position
L11 = Label(gui, text="Port Scanner",  font=(
    "Helvetica", 45), background='light blue')
L11.place(relx=0.5, rely=0.05, anchor='center')  # Centered position

L21 = Label(gui, text="Target IP Adress: ", background='light blue')
L21.place(relx=0.1, rely=0.15, anchor='e')  # Adjusted x position

L22 = Entry(gui, text="localhost", width=25,
            background='#FFFFFF')  # Increased width
L22.place(relx=0.25, rely=0.15, anchor='w')  # Adjusted x position

L23 = Label(gui, text="Port Range: ", background='light blue')
L23.place(relx=0.1, rely=0.2, anchor='e')  # Adjusted x position

L24 = Entry(gui, text="1", width=10, background='#FFFFFF')  # Increased width
L24.place(relx=0.25, rely=0.2, anchor='w')  # Adjusted x position

L25 = Entry(gui, text="1024", width=10,
            background='#FFFFFF')  # Increased width
L25.place(relx=0.4, rely=0.2, anchor='w')  # Adjusted x position

L26 = Label(gui, text="Results: ", background='light blue')
L26.place(relx=0.1, rely=0.3, anchor='e')  # Adjusted x position

# Increased width and height, added relief
L27 = Label(gui, text="[ ... ]", width=80, height=10,
            relief='sunken', background='#FFFFFF')
L27.place(relx=0.5, rely=0.4, anchor='center')  # Centered position

# ==== Ports list ====
frame = Frame(gui)
# Centered position, increased width and height
frame.place(relx=0.5, rely=0.7, anchor='center', width=380, height=250)
listbox = Listbox(frame, width=75, height=12)  # Increased width and height
listbox.pack(side='left', fill='both', expand=True)
listbox.bind('<<ListboxSelect>>')
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Buttons / Scans
B11 = Button(gui, text="Start Scan", command=startScan,
             background="light blue")
# Centered position, adjusted x position, and set width
B11.place(relx=0.3, rely=0.9, anchor='center', width=170)

# ==== Start GUI ====
gui.mainloop()
