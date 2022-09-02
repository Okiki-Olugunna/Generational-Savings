from brownie import accounts, config
from web3 import Web3
import pytest


w3 = Web3(Web3.WebsocketProvider(config["provider"]["websockets"]))

with open("./contract_data/goerli-eth/address.txt") as file_a:
    contract_address = file_a.read()

with open("./contract_data/goerli-eth/abi.json") as file_b:
    contract_abi = file_b.read()

# initialising the contract instance
contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)


def test_change_approvals():

    # initialising the admin
    admin = config["wallets"]["from_key"]["admin"]
    admin_address = config["addresses"]["admin_address"]

    # getting the current approval number
    old_approval_number = contract_instance.functions.requiredApprovals().call()

    # number to change approvals to
    new_approval_number = old_approval_number + 1

    # getting the nonce of the admin that will be sending the transaction
    nonce = w3.eth.get_transaction_count(admin_address)
    # building the transaction
    tx = contract_instance.functions.changeRequiredApprovals(
        new_approval_number
    ).buildTransaction(
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

    # asserting that the number of approvals is different
    assert old_approval_number != new_approval_number
