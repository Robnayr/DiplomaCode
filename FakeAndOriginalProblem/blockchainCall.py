import cv2
from pyzbar import pyzbar
from web3 import Web3
import re
import pandas as pd
import tkinter as tk
from tkinter import ttk
import webbrowser
import pyperclip
from tkinter import messagebox

qr_data = ""
# Create a capture object to get frames from the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while len(qr_data) == 0:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use the pyzbar library to find QR codes in the frame
    qr_codes = pyzbar.decode(gray)

    # Iterate over the QR codes found in the frame
    for qr_code in qr_codes:
        # Extract the data from the QR code
        qr_data = qr_code.data.decode("utf-8")

        # Print the data to the console
        print(qr_data)

    # Display the current frame in a window
    cv2.imshow("QR Code Reader", frame)

    # Wait for a key press to exit the program
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the capture object and close the window
cap.release()
cv2.destroyAllWindows()

# Create an instance of the Web3 class using the Binance Testnet endpoint
w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545'))

# Set the contract address and ABI
contract_address = '0x6A51720f6BEAE6D08Ff2a0a25459Ed9E157E61ad' # Storage contract binance testnet address
contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"addingTimestamp","type":"uint256"},{"indexed":True,"internalType":"address","name":"newAdmin","type":"address"}],"name":"addedAdmin","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"addingTimestamp","type":"uint256"},{"indexed":True,"internalType":"string","name":"description","type":"string"}],"name":"addedGoods","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"removingTimestamp","type":"uint256"},{"indexed":True,"internalType":"address","name":"removedAdmin","type":"address"}],"name":"removedAdmin","type":"event"},{"inputs":[{"internalType":"address","name":"_newAdmin","type":"address"}],"name":"addAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"_createTime","type":"uint256"},{"internalType":"uint256","name":"_weight","type":"uint256"},{"internalType":"uint256","name":"_height","type":"uint256"},{"internalType":"string","name":"_description","type":"string"},{"internalType":"string","name":"_creatorName","type":"string"}],"name":"addGoods","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"admins","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"getGoods","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"goodsById","outputs":[{"internalType":"uint256","name":"createTime","type":"uint256"},{"internalType":"uint256","name":"weight","type":"uint256"},{"internalType":"uint256","name":"height","type":"uint256"},{"internalType":"string","name":"description","type":"string"},{"internalType":"string","name":"creatorName","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_oldAdmin","type":"address"}],"name":"removeAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"}]

# Create an instance of the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Call the contract function and print the result
result = contract.functions.getGoods(int(qr_data)).call()

date = int(result[0])
weight = int(result[1])
height = int(result[2])
description = result[3]
links = re.findall(r"(https?://\S+)", description)  # Extract links from description
description = description.replace(links[0], "")
creator = result[4].strip("'")

data = [[date, weight,  height,  description, links, creator]]
df = pd.DataFrame.from_dict(data)
# print(df)

# Create a tkinter window
root = tk.Tk()
root.title('My Data')

# Create a frame to hold the data
frame = tk.Frame(root)
frame.pack(fill='both', expand=True)

# Create a treeview to display the data
columns = ['Date', 'Weight', 'Height', 'Description','links', 'Creator']
treeview = ttk.Treeview(frame, columns=columns, show='headings')
treeview.pack(side='left', fill='both', expand=True)

# Set the column headings
for col in columns:
    treeview.heading(col, text=col)

# Add the data to the treeview
for row in data:
    treeview.insert('', 'end', values=row)

# Add a scrollbar
scrollbar = ttk.Scrollbar(frame, orient='vertical', command=treeview.yview)
scrollbar.pack(side='right', fill='y')
treeview.configure(yscrollcommand=scrollbar.set)

# Define a callback function to open the link
def open_link(event):
    item = treeview.identify_row(event.y)
    values = treeview.item(item)['values']
    link = values[3].split('|')[1]
    pyperclip.copy(links[0])
    messagebox.showinfo('Link Copied', 'The link has been copied to your clipboard. Please paste it into your browser\'s address bar to open it.')

# Attach the callback function to the treeview's tags
for row_id in treeview.get_children():
    values = treeview.item(row_id)['values']
    if '|' in values[3]:
        treeview.item(row_id, tags=('clickable',))
treeview.tag_bind('clickable', '<Button-1>', open_link)

# Run the tkinter event loop
root.mainloop()

# # Print the extracted parameters
# print(f"Date: {date}")
# print(f"Weight: {weight}")
# print(f"Height: {height}")
# print(f"Description: {description}")
# print(f"Links: {links}")
# print(f"Creator: {creator}")