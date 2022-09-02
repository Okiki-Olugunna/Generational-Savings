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


def test_withdraw_from_reserves():

    # instantiating the accounts
    admin = config["wallets"]["from_key"]["admin"]
    admin_address = config["addresses"]["admin_address"]

    # family members to add
    family_member_2 = config["wallets"]["from_key"]["family_member_2"]
    family_member_2_address = config["addresses"]["family_member_2_address"]

    family_member_3 = config["wallets"]["from_key"]["family_member_3"]
    family_member_3_address = config["addresses"]["family_member_3_address"]

    family_member_4 = config["wallets"]["from_key"]["family_member_4"]
    family_member_4_address = config["addresses"]["family_member_4_address"]

    ####################################################################################

    ####################################################################################
    ####################################################################################

    ## PART 1 - ASSUMING THAT ALL MEMBERS HAVE ALREADY BEEN ADDED TO THE FAMILY
    ## each member will now add to the reserves with a direct transaction

    ####################################################################################
    ####################################################################################
    ####################################################################################

    ## ADMIN ADDING RESERVES

    # checking the current reserves
    initial_reserves = contract_instance.functions.reserveETH().call(
        {"from": admin_address}
    )
    # reserves converted
    reserves_converted = w3.fromWei(initial_reserves, "ether")

    # initialising the amount of ETH to send
    amount_to_send = w3.toWei(Decimal("0.01"), "ether")  # 0.01 ETH
    # converting to ether
    amount_converted = w3.fromWei(amount_to_send, "ether")

    # depositing eth into the reserve
    nonce = w3.eth.get_transaction_count(admin_address)

    # Signing the transaction...
    signed_tx = w3.eth.account.sign_transaction(
        {
            "gasPrice": w3.eth.gas_price,
            "gas": 80000,
            "chainId": 5,
            "to": contract_address,
            "from": admin_address,
            "value": amount_to_send,
            "nonce": nonce,
        },
        admin,
    )

    # sending the transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Waiting for the transaction to go through...
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    ####################################################################################

    ## FAMILY MEMBER 2 ADDING RESERVES

    # checking the current reserves
    current_reserves_2 = contract_instance.functions.reserveETH().call(
        {"from": family_member_2_address}
    )
    # reserves converted
    reserves_converted = w3.fromWei(current_reserves_2, "ether")

    # initialising the amount of ETH to send
    amount_to_send = w3.toWei(Decimal("0.01"), "ether")  # 0.01 ETH
    # converting to ether
    amount_converted = w3.fromWei(amount_to_send, "ether")

    # depositing  eth into the reserve

    # Getting the nonce of family member 2
    nonce = w3.eth.get_transaction_count(family_member_2_address)

    # Signing the transaction...
    signed_tx = w3.eth.account.sign_transaction(
        {
            "gasPrice": w3.eth.gas_price,
            "gas": 80000,
            "chainId": 5,
            "to": contract_address,
            "from": family_member_2_address,
            "value": amount_to_send,
            "nonce": nonce,
        },
        family_member_2,
    )

    # sending the transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Waiting for the transaction to go through...
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    # checking the current reserves
    current_reserves_3 = contract_instance.functions.reserveETH().call(
        {"from": admin_address}
    )
    # reserves converted
    reserves_converted = w3.fromWei(current_reserves_3, "ether")

    ####################################################################################
    ####################################################################################
    ####################################################################################

    ## PART 3
    ## MEMBER 2 WILL REQUEST A WITHDRAWAL FROM THE RESERVES

    ####################################################################################
    ####################################################################################
    ####################################################################################

    ## FAMILY MEMBER 2 REQUESTING A WITHDRAWAL

    # reason to withdraw
    reason_to_withdraw = "Creating the world's greatest startup."

    # sending the request
    nonce = w3.eth.get_transaction_count(family_member_2_address)
    tx = contract_instance.functions.requestToWithdrawReserves(
        reason_to_withdraw
    ).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": 5,
            "from": family_member_2_address,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, family_member_2)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Waiting for the transaction to go through...
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    # checking the current request ID
    request_id = contract_instance.functions.requestID().call(
        {"from": family_member_2_address}
    )

    ####################################################################################
    ####################################################################################
    ####################################################################################

    ## PART 4
    ## 2 FAMILY MEMBERS WILL APPROVE THE REQUEST OF MEMBER 2 USING THE REQUEST ID
    # - since 2 is the current approval number

    ####################################################################################
    ####################################################################################
    ####################################################################################

    # finding out the current number of approvals
    current_num_of_approvals = contract_instance.functions.requestIDToApprovals(
        request_id
    ).call({"from": family_member_3_address})

    # family member 3 will approve the request

    # approving the request
    nonce = w3.eth.get_transaction_count(family_member_3_address)
    tx = contract_instance.functions.approveRequest(request_id).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": 5,
            "from": family_member_3_address,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, family_member_3)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Waiting for the transaction to go through...
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    # checking the new number of approvals
    current_num_of_approvals = contract_instance.functions.requestIDToApprovals(
        request_id
    ).call({"from": family_member_3_address})

    ####################################################################################

    # family member 4 will approve the request

    # approving the request
    nonce = w3.eth.get_transaction_count(family_member_4_address)
    tx = contract_instance.functions.approveRequest(request_id).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": 5,
            "from": family_member_4_address,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, family_member_4)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Waiting for the transaction to go through...
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    # checking the new number of approvals
    current_num_of_approvals = contract_instance.functions.requestIDToApprovals(
        request_id
    ).call({"from": family_member_3_address})

    # checking the required approvals
    required_approvals = contract_instance.functions.requiredApprovals().call()

    ####################################################################################
    ####################################################################################
    ####################################################################################

    ## PART 5
    ## FAMILY MEMBER 2 WILL NOW EXECUTE THE WITHDRAWAL FROM THE RESERVES NOW THAT IT HAS BEEN APPROVED

    ####################################################################################
    ####################################################################################
    ####################################################################################

    # checking the individual's balance before execution of the withdrawal
    family_member_2_balance_before_withdrawal = w3.eth.get_balance(
        family_member_2_address
    )

    # checking the current family reserves
    current_reserves_before_withdrawal = contract_instance.functions.reserveETH().call(
        {"from": admin_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(current_reserves_before_withdrawal, "ether")

    #########################
    # executing the withdrawal

    nonce = w3.eth.get_transaction_count(family_member_2_address)
    tx = contract_instance.functions.executeReserveWithdrawal(
        request_id
    ).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": 5,
            "from": family_member_2_address,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, family_member_2)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Waiting for the transaction to go through...
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    # checking the updated balance of family member 2 after the withdrawal
    family_member_2_updated_balance = w3.eth.get_balance(family_member_2_address)

    # checking the updated family reserves
    reserves_after_withdrawal = contract_instance.functions.reserveETH().call(
        {"from": admin_address}
    )

    ## assertions
    assert reserves_after_withdrawal == 0
    assert family_member_2_updated_balance > family_member_2_balance_before_withdrawal
