from brownie import accounts, config
from web3 import Web3
from eth_utils import from_wei
from decimal import Decimal


def get_depolyed_contract():
    print("\nConnecting to the node provider...\n")
    w3 = Web3(Web3.WebsocketProvider(config["provider"]["websockets"]))
    print("Connected.\n")

    print("Getting the contract instance...\n")

    with open("./contract_data/goerli-eth/address.txt") as file_a:
        contract_address = file_a.read()

    with open("./contract_data/goerli-eth/abi.json") as file_b:
        contract_abi = file_b.read()

    # initialising the contract instance
    contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)

    print(f"Obtained the contract instance at address {contract_address}\n")


def main():
    get_depolyed_contract()
