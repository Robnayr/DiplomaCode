import tkinter as tk
from tkinter import messagebox
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import paraphrase_mining
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os
import re
from web3 import Web3
from web3.middleware import geth_poa_middleware

working_dir = os.getcwd()
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Set account that will send the transaction
account = '...' # here has to be your address

# Set private key of the account
private_key = '...' # here has to be private key of your address

# Initialize address nonce
nonce = w3.eth.get_transaction_count(account)

# Set the contract address and ABI
contract_address = '0x131A0e2B2470187620C15926D745713b4E67662d' # NFT smart contract binance testnet address
contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"approved","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"operator","type":"address"},{"indexed":False,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":False,"internalType":"string","name":"tokenURI","type":"string"}],"name":"CreatedSVGNFT","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_metadata","type":"string"}],"name":"create","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"tokenCounter","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]

model = SentenceTransformer('paraphrase-albert-small-v2')

def remove_punct(text):
    punct_open = open(f"{working_dir}\\punctuation.txt", "r", encoding="utf8")
    punct = punct_open.read()
    for char in punct:
        text = text.replace(char, "")
    return text

def preprocess(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text).lower()
    text = remove_punct(text)
    tokens = word_tokenize(text)
    lemmatized_text = [lemmatizer.lemmatize(word) for word in tokens]
    stop_word_free_text = [word for word in lemmatized_text if word not in stop_words]
    stop_word_free_text_str = ' '.join(stop_word_free_text)
    return stop_word_free_text_str

def check_plagiarism():
    text = input_text.get("1.0", tk.END)
    originals_train = []
    for filename in os.listdir(f"{working_dir}\\train_docs\\og"):
        with open(os.path.join(f"{working_dir}\\train_docs\\og", filename), "r", encoding="utf-8") as f:
            originals_train.append(f.read().replace('\n', ' '))

    originals_test = []
    for filename in os.listdir(f"{working_dir}\\test_docs\\og"):
        with open(os.path.join(f"{working_dir}\\test_docs\\og", filename), "r", encoding="utf-8") as f:
            originals_test.append(f.read().replace('\n', ' '))

    docs = originals_train + originals_test

    preprocessed_docs = []
    for doc in docs:
        preprocessed_docs.append(preprocess(doc))

    preprocessed_input_text = preprocess(text)

    threshold = 0.5

    predictions = []
    for doc in preprocessed_docs:
        pair = [preprocessed_input_text, doc]
        predictions.append(paraphrase_mining(model, pair)[0][0])

    if max(predictions) > threshold:
        print(f'Max similarity score is {max(predictions)}. Your input text is plagiarized')
        messagebox.showinfo("Plagiarism Detected", f"The text is {max(predictions):.2%} plagiarized.")
    else:
        print(f'Max similarity score is {max(predictions)}. Your input text is not plagiarized')
        messagebox.showinfo("Anti-Plagiarism Check", f"The text is {1 - max(predictions):.2%} unique.")
        mint_NFT(text)


def mint_NFT(nft_metadata):
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id
    # Call your function
    call_function = contract.functions.create(nft_metadata).build_transaction({"chainId": Chain_id, "from": account, "gas": 30000000, "gasPrice": w3.to_wei('10', 'gwei'), "nonce": nonce})
    # Sign transaction
    signed_tx = w3.eth.account.sign_transaction(call_function, private_key=private_key)
    # Send transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
    print(tx_receipt) 

root = tk.Tk()
root.title("Text Plagiarism Checker")

input_text = tk.Text(root, height=10, width=50)
input_text.grid(row=0, column=0, padx=10, pady=10)

check_button = tk.Button(root, text="Check Plagiarism", command=check_plagiarism)
check_button.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()
