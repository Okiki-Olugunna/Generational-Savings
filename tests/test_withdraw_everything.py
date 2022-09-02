from brownie import accounts, config
from web3 import Web3
from decimal import Decimal
import pytest


w3 = Web3(Web3.WebsocketProvider(config["provider"]["websockets"]))

with open("./contract_data/goerli-eth/address.txt") as file_a:
    contract_address = file_a.read()

with open("./contract_data/goerli-eth/abi.json") as file_b:
    contract_abi = file_b.read()

# initialising the contract instance
contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)


def test_withdraw_everything():
    # instantiating the accounts
    admin = config["wallets"]["from_key"]["admin"]
    admin_address = config["addresses"]["admin_address"]

    # family members
    family_member_2 = config["wallets"]["from_key"]["family_member_2"]
    family_member_2_address = config["addresses"]["family_member_2_address"]

    # checking the current family holdings
    initial_current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": admin_address}
    )

    ####################################################################################
    ## ADMIN ADDING SAVINGS

    # initialising the amount of ETH to send
    amount_to_send = w3.toWei(Decimal("0.01"), "ether")  # 0.01 ETH
    # converting to ether
    amount_converted = w3.fromWei(amount_to_send, "ether")

    # depositing eth into the savings - this tx will go to Aave V3
    nonce = w3.eth.get_transaction_count(admin_address)
    tx = contract_instance.functions.easySaveETH().buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": 5,
            "from": admin_address,
            "value": amount_to_send,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, admin)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Waiting for the transaction to go through...
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    ####################################################################################
    # FAMILY MEMBER 2 ADDING TO SAVINGS

    # initialising the amount of ETH to send
    amount_to_send = w3.toWei(Decimal("0.01"), "ether")  # 0.01 ETH
    # converting to ether
    amount_converted = w3.fromWei(amount_to_send, "ether")

    # depositing eth into the savings - this tx will go to Aave V3
    nonce = w3.eth.get_transaction_count(family_member_2_address)
    tx = contract_instance.functions.easySaveETH().buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": 5,
            "from": family_member_2_address,
            "value": amount_to_send,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, family_member_2)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Waiting for the transaction to go through...
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    # checking the current family holdings
    new_savings_amount = contract_instance.functions.viewFamilyHoldings().call(
        {"from": family_member_2_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(new_savings_amount, "ether")

    ####################################################################################

    ## ADMIN WILL NOW WITHDRAW ALL THE SAVINGS

    ## Withdrawing everything

    # checking the admin's balance before execution of the withdrawal
    admin_balance = w3.eth.get_balance(admin_address)
    admin_balance_converted = w3.fromWei(admin_balance, "ether")

    #########################
    # executing the withdrawal
    #########################

    nonce = w3.eth.get_transaction_count(admin_address)
    tx = contract_instance.functions.withdrawEverything().buildTransaction(
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

    # Waiting for the transaction to go through...
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    # checking the updated balance of the admin from the withdrawal

    new_admin_balance = w3.eth.get_balance(admin_address)
    # admin_balance_converted = w3.fromWei(new_admin_balance, "ether")

    # checking the updated family savings
    family_savings_after_withdrawal = (
        contract_instance.functions.viewFamilyHoldings().call({"from": admin_address})
    )

    ## ASSERTIONS
    assert family_savings_after_withdrawal == 0
    assert new_admin_balance > admin_balance
