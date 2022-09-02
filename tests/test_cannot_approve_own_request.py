from brownie import accounts, config, exceptions
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


def test_withdraw_from_savings():
    # instantiating the accounts
    admin = config["wallets"]["from_key"]["admin"]
    admin_address = config["addresses"]["admin_address"]

    # family members
    family_member_2 = config["wallets"]["from_key"]["family_member_2"]
    family_member_2_address = config["addresses"]["family_member_2_address"]

    family_member_3 = config["wallets"]["from_key"]["family_member_3"]
    family_member_3_address = config["addresses"]["family_member_3_address"]

    family_member_4 = config["wallets"]["from_key"]["family_member_4"]
    family_member_4_address = config["addresses"]["family_member_4_address"]

    ## PART 1

    # family members were already added in previous scripts / tests

    ####################################################################################
    ####################################################################################
    ####################################################################################

    ## PART 2
    ## some members will now call easySaveETH

    ####################################################################################
    ####################################################################################

    ####################################################################################

    ## ADMIN ADDING SAVINGS

    # checking the current family holdings
    initial_current_savings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": admin_address}
    )

    # initialising the amount of ETH to send
    amount_to_send = w3.toWei(Decimal("0.01"), "ether")  # 0.01 ETH
    # converting to ether
    amount_converted = w3.fromWei(amount_to_send, "ether")

    # depositing some eth into the savings - this tx will go to Aave V3
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

    # checking the current family holdings
    current_savings_2 = contract_instance.functions.viewFamilyHoldings().call(
        {"from": admin_address}
    )

    ####################################################################################

    ## FAMILY MEMBER 2 ADDING SAVINGS

    # initialising the amount of ETH to send
    amount_to_send = w3.toWei(Decimal("0.01"), "ether")  # 0.01 ETH
    # converting to ether
    amount_converted = w3.fromWei(amount_to_send, "ether")

    # depositing some eth into the savings - this tx will go to Aave V3
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
    current_savings_3 = contract_instance.functions.viewFamilyHoldings().call(
        {"from": family_member_2_address}
    )

    ####################################################################################
    ####################################################################################
    ####################################################################################

    ## PART 3
    ## MEMBER 2 WILL REQUEST A WITHDRAWAL

    ####################################################################################
    ####################################################################################
    ####################################################################################

    ## FAMILY MEMBER 2 REQUESTING A WITHDRAWAL

    # initialising the amount of ETH to withdraw
    amount_to_request = w3.toWei(Decimal("0.01"), "ether")  # 0.01 ETH
    # converting to ether
    amount_converted = w3.fromWei(amount_to_request, "ether")
    # reason to withdraw
    reason_to_withdraw = "Buying a new house."

    # sending the request
    nonce = w3.eth.get_transaction_count(family_member_2_address)
    tx = contract_instance.functions.requestWithdrawal(
        amount_to_request, reason_to_withdraw
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
    # family member 2 will approve the request
    # MEMBER 2 is the same member who made the request - this should NOT go through

    nonce = w3.eth.get_transaction_count(family_member_2_address)

    # test will pass if error is thrown
    with pytest.raises(exceptions.VirtualMachineError):
        # with pytest.raises(exceptions.ContractLogicError):
        # approving the request
        tx = contract_instance.functions.approveRequest(request_id).buildTransaction(
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

        # # Waiting for the transaction to go through...
        tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
