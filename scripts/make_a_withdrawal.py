from brownie import accounts, config
from web3 import Web3
from decimal import Decimal


w3 = Web3(Web3.WebsocketProvider(config["provider"]["websockets"]))

with open("./contract_data/goerli-eth/address.txt") as file_a:
    contract_address = file_a.read()

with open("./contract_data/goerli-eth/abi.json") as file_b:
    contract_abi = file_b.read()

# initialising the contract instance
contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)


def main():
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

    ## PART 1
    print("\n------------------------------------------------------------------\n")
    print("------------------------------------------------------------------\n")
    print("\nSTARTING THE SCRIPT MAKE_A_WITHDRAWAL.PY...\n")
    print("------------------------------------------------------------------\n")
    print("------------------------------------------------------------------\n")

    # admin will add these accounts to the family contract addresses

    # getting the current count of family members
    num_of_family = contract_instance.functions.numOfFamilyMembers().call()
    print(f"\nThere are currently {num_of_family} family members in this contract.\n")

    print("------------------------------------------------------------------\n")

    ####################################################################################
    # adding family member 2
    print(f"Adding family member 2 '{family_member_2_address}'...\n")

    # getting the nonce of the admin that will be sending the transaction
    nonce = w3.eth.get_transaction_count(admin_address)
    # building the transaction
    tx = contract_instance.functions.addFamilyMember(
        family_member_2_address
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

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print(f"Family member 2 '{family_member_2_address}' has been added.\n")

    # checking the new number of family members
    num_of_family = contract_instance.functions.numOfFamilyMembers().call()
    print(f"There are now {num_of_family} family members in this contract.\n")

    print("------------------------------------------------------------------\n")

    ####################################################################################

    # adding family member 3
    print(f"Adding family member 3 '{family_member_3_address}'...\n")

    # getting the nonce of the admin that will be sending the transaction
    nonce = w3.eth.get_transaction_count(admin_address)
    # building the transaction
    tx = contract_instance.functions.addFamilyMember(
        family_member_3_address
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

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print(f"Family member 3 '{family_member_3_address}' has been added.\n")

    # checking the new number of family members
    num_of_family = contract_instance.functions.numOfFamilyMembers().call()
    print(f"There are now {num_of_family} family members in this contract.\n")

    print("------------------------------------------------------------------\n")

    ####################################################################################

    # adding family member 4
    print(f"Adding family member 4 '{family_member_4_address}'...\n")

    # getting the nonce of the admin that will be sending the transaction
    nonce = w3.eth.get_transaction_count(admin_address)
    # building the transaction
    tx = contract_instance.functions.addFamilyMember(
        family_member_4_address
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

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print(f"Family member 4 '{family_member_4_address}' has been added.\n")

    # checking the new number of family members
    num_of_family = contract_instance.functions.numOfFamilyMembers().call()
    print(f"There are now {num_of_family} family members in this contract.\n")

    print("------------------------------------------------------------------\n")

    ####################################################################################

    ####################################################################################
    ####################################################################################

    ## PART 2
    ## each member will now add call easySaveETH

    ####################################################################################
    ####################################################################################

    ####################################################################################

    ## ADMIN ADDING SAVINGS

    # checking the current family holdings
    print("\nChecking the current family savings...\n")

    current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": admin_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(current_holdings, "ether")

    print(f"The current savings in aWETH are: {holdings_converted} aWETH\n")

    # initialising the amount of ETH to send
    amount_to_send = w3.toWei(Decimal("0.003"), "ether")  # 0.003 ETH
    # converting to ether
    amount_converted = w3.fromWei(amount_to_send, "ether")

    print(
        f"The admin / 'family member 1 ({admin_address})' is sending {amount_converted} ETH to the family savings account...\n"
    )

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

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print(
        f"The admin / 'family member 1 ({admin_address})' has successfully added {amount_converted} ETH to the defi family savings account.\n"
    )

    # checking the current family holdings
    current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": admin_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(current_holdings, "ether")

    print(f"The current savings in aWETH are: {holdings_converted} aWETH :) \n")

    print("------------------------------------------------------------------\n")

    ####################################################################################

    ## FAMILY MEMBER 2 ADDING SAVINGS

    # checking the current family holdings
    print("\nChecking the current family savings...\n")

    current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": family_member_2_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(current_holdings, "ether")

    print(f"The current savings in aWETH are: {holdings_converted} aWETH\n")

    # initialising the amount of ETH to send
    amount_to_send = w3.toWei(Decimal("0.003"), "ether")  # 0.003 ETH
    # converting to ether
    amount_converted = w3.fromWei(amount_to_send, "ether")

    print(
        f"Family member 2 ({family_member_2_address}) is sending {amount_converted} ETH to the family savings account...\n"
    )

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

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print(
        f"Family member 2 ({family_member_2_address}) has successfully added {amount_converted} ETH to the defi family savings account.\n"
    )

    # checking the current family holdings
    current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": family_member_2_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(current_holdings, "ether")

    print(f"The current savings in aWETH are: {holdings_converted} aWETH :) \n")

    print("------------------------------------------------------------------\n")

    ####################################################################################

    ## FAMILY MEMBER 3 ADDING SAVINGS

    # checking the current family holdings
    print("\nChecking the current family savings...\n")

    current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": family_member_3_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(current_holdings, "ether")

    print(f"The current family savings in aWETH are: {holdings_converted} aWETH\n")

    # initialising the amount of ETH to send
    amount_to_send = w3.toWei(Decimal("0.003"), "ether")  # 0.003 ETH
    # converting to ether
    amount_converted = w3.fromWei(amount_to_send, "ether")

    print(
        f"Family member 3 ({family_member_3_address}) is sending {amount_converted} ETH to the family savings account...\n"
    )

    # depositing some eth into the savings - this tx will go to Aave V3
    nonce = w3.eth.get_transaction_count(family_member_3_address)
    tx = contract_instance.functions.easySaveETH().buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": 5,
            "from": family_member_3_address,
            "value": amount_to_send,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, family_member_3)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print(
        f"Family member 3 {family_member_3_address} has successfully added {amount_converted} ETH to the defi family savings account.\n"
    )

    # checking the current family holdings
    current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": family_member_3_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(current_holdings, "ether")

    print(f"The current savings in aWETH are: {holdings_converted} aWETH :) \n")

    print("------------------------------------------------------------------\n")

    ####################################################################################

    ####################################################################################
    ####################################################################################

    ## PART 3
    ## MEMBER 2 WILL REQUEST A WITHDRAWAL

    ####################################################################################
    ####################################################################################

    ####################################################################################

    ## FAMILY MEMBER 2 REQUESTING A WITHDRAWAL

    # checking the current family holdings
    print("\nChecking the current family holdings...\n")

    current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": family_member_2_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(current_holdings, "ether")

    print(f"The current savings in aWETH are: {holdings_converted} aWETH\n")

    # initialising the amount of ETH to withdraw
    amount_to_request = w3.toWei(Decimal("0.003"), "ether")  # 0.003 ETH
    # converting to ether
    amount_converted = w3.fromWei(amount_to_request, "ether")
    # reason to withdraw
    reason_to_withdraw = "Buying a new house."

    print(
        f"Family member 2 ({family_member_2_address}) is requesting a withdrawal of {amount_converted} ETH from the family savings account, with the reason '{reason_to_withdraw}'...\n"
    )

    # sending the request - this will use request ID = 1
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

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    # checking the current request ID
    request_id = contract_instance.functions.requestID().call(
        {"from": family_member_2_address}
    )

    print(f"Your request ID is: {request_id} :) \n")

    print(
        f"Successfully made a request for {amount_converted} ETH from the defi family savings account, with the requestID of {request_id}. Please wait for the others to approve your request...\n"
    )

    print("------------------------------------------------------------------\n")

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

    print(
        f"The current number of approvals for requestID {request_id} is {current_num_of_approvals}\n"
    )

    # getting the reason to the request
    reason_for_request = contract_instance.functions.requestIDToReason(request_id).call(
        {"from": family_member_3_address}
    )

    print(f"The reason for requestID {request_id} is: '{reason_for_request}' \n")

    # family member 3 will approve the request
    print(
        f"Family member 3 ({family_member_3_address}) is approving requestID: {request_id}...\n"
    )

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

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print(
        f"Family member 3 ({family_member_3_address}) has successfully approved requestID: {request_id}.\n"
    )

    # checking the new number of approvals
    current_num_of_approvals = contract_instance.functions.requestIDToApprovals(
        request_id
    ).call({"from": family_member_3_address})

    print(
        f"The current number of approvals for requestID {request_id} is {current_num_of_approvals}\n"
    )

    ####################################################################################

    # family member 4 will approve the request
    print(
        f"Family member 4 ({family_member_4_address}) is approving request ID: {request_id}...\n"
    )

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

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print(
        f"Family member 4 ({family_member_4_address}) has successfully approved requestID: {request_id}.\n"
    )

    # checking the new number of approvals
    current_num_of_approvals = contract_instance.functions.requestIDToApprovals(
        request_id
    ).call({"from": family_member_3_address})

    print(
        f"The current number of approvals for requestID {request_id} is {current_num_of_approvals}\n"
    )

    # checking the required approvals
    required_approvals = contract_instance.functions.requiredApprovals().call()
    print(
        f"The required number of approvals for a withdrawal to go through is: {required_approvals} approvals\n"
    )

    ####################################################################################
    ####################################################################################
    ####################################################################################

    ## PART 5
    ## FAMILY MEMBER 2 WILL NOW EXECUTE THEIR WITHDRAWAL NOW THAT IT HAS BEEN APPROVED

    ####################################################################################
    ####################################################################################
    ####################################################################################

    # checking the individual's balance before execution of the withdrawal
    print(f"Checking the current balance of {family_member_2_address}...\n")

    family_member_2_balance = w3.eth.get_balance(family_member_2_address)
    family_member_2_balance_converted = w3.fromWei(family_member_2_balance, "ether")

    print(
        f"The current balance of family member 2 ({family_member_2_address}) is {family_member_2_balance_converted} ETH.\n"
    )

    # checking the current family holdings
    print("Checking the current family savings...\n")

    current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": admin_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(current_holdings, "ether")

    print(f"The current family savings in aWETH are: {holdings_converted} aWETH\n")

    #########################
    # executing the withdrawal
    print(
        f"Family member 2 ({family_member_2_address}) is now executing their withdrawal...\n"
    )

    nonce = w3.eth.get_transaction_count(family_member_2_address)
    tx = contract_instance.functions.withdrawSavedETH(request_id).buildTransaction(
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

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print(
        f"Family member 2 ({family_member_2}) has now successfully withdrawn from the family defi savings.\n"
    )

    # checking the updated balance before after the withdrawal
    print(
        f"Checking the current balance of family member 2 ({family_member_2_address})...\n"
    )

    family_member_2_balance = w3.eth.get_balance(family_member_2_address)
    family_member_2_balance_converted = w3.fromWei(family_member_2_balance, "ether")

    print(
        f"The current balance of family member 2 ({family_member_2_address}) is now {family_member_2_balance_converted} ETH.\n"
    )

    # checking the updated family holdings
    print("Checking the new amount in family savings...\n")

    current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": admin_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(current_holdings, "ether")

    print(f"The current updated savings in aWETH are: {holdings_converted} aWETH\n")

    print("-----------------------------------------------------------------")
    print("-----------------------------------------------------------------")
    print("-----------------------------------------------------------------")
    print("\nMAKE_A_WITHDRAWAL.PY SCRIPT IS NOW COMPLETE.\n")
    print("-----------------------------------------------------------------")
    print("-----------------------------------------------------------------")
    print("-----------------------------------------------------------------")
