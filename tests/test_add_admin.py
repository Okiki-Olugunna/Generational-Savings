from brownie import accounts, exceptions, config, network
from eth_utils import from_wei
from web3 import Web3
import pytest

w3 = Web3(Web3.WebsocketProvider(config["provider"]["websockets"]))


with open("./contract_data/goerli-eth/address.txt") as file_a:
    contract_address = file_a.read()

with open("./contract_data/goerli-eth/abi.json") as file_b:
    contract_abi = file_b.read()

# initialising the contract instance
contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)


def test_add_admin():
    # instantiating the accounts
    admin = config["wallets"]["from_key"]["admin"]
    admin_address = config["addresses"]["admin_address"]

    # admin to add
    family_member_4 = accounts.add(config["wallets"]["from_key"]["family_member_4"])

    # getting the inital number of admins
    initial_admin_number = contract_instance.functions.numOfAdmins().call()

    # admin will now add another admin

    # getting the nonce of the admin that will be sending the transaction
    nonce = w3.eth.get_transaction_count(admin_address)
    # building the transaction
    tx = contract_instance.functions.addAdmin(family_member_4.address).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": 5,
            "from": admin_address,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, admin)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # waiting for the transaction to go through...
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    # checking the new number of admins
    updated_admin_number = contract_instance.functions.numOfAdmins().call()

    # asserting that there are more admins
    assert initial_admin_number < updated_admin_number
