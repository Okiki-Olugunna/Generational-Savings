from web3 import Web3
from brownie import config


w3 = Web3(Web3.WebsocketProvider(config["provider"]["websockets"]))


def main():
    print(w3.isConnected())
