## in this script *only* the admin can call "withdrawEverything" on the smart contract
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

    # family members
    family_member_2 = config["wallets"]["from_key"]["family_member_2"]
    family_member_2_address = config["addresses"]["family_member_2_address"]

    ##
    print("\n------------------------------------------------------------------\n")
    print("------------------------------------------------------------------\n")
    print("\nSTARTING THE SCRIPT WITHDRAW_EVERYTHING.PY...\n")
    print("------------------------------------------------------------------\n")
    print("------------------------------------------------------------------\n")

    ####################################################################################
    ### PART 1
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
    nonce = w3.eth.getTransactionCount(admin_address)
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

    ####################################################################################
    ####################################################################################
    ####################################################################################

    ## PART 3
    # ADDING TO SAVINGS

    ####################################################################################
    ####################################################################################
    ####################################################################################

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
    nonce = w3.eth.getTransactionCount(family_member_2_address)
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
    ####################################################################################
    ####################################################################################

    ## PART 3
    ## ADMIN WILL NOW WITHDRAW ALL THE SAVINGS

    ####################################################################################
    ####################################################################################
    ####################################################################################

    ## Withdrawing everything

    # checking the individual's balance before execution of the withdrawal
    print(f"Checking the current balance of {admin_address}...\n")

    admin_balance = w3.eth.get_balance(admin_address)
    admin_balance_converted = w3.fromWei(admin_balance, "ether")

    print(
        f"The current balance of the admin ({admin_balance}) is {admin_balance_converted} ETH.\n"
    )

    # checking the current family savings
    print("Checking the current family savings...\n")

    current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": admin_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(current_holdings, "ether")

    print(
        f"The current amount of ETH in the faminly defi savings is: {holdings_converted}.\n"
    )

    #########################

    # executing the withdrawal

    #########################

    print(
        f"The admin ({admin_address}) is now executing the withdrawal of all the savings...\n"
    )

    nonce = w3.eth.getTransactionCount(admin_address)
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

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print(
        f"The admin ({admin_address}) has now successfully withdrawn from the reserves.\n"
    )

    # checking the updated balance from the withdrawal
    print(f"Checking the current balance of the admin ({admin_address})...\n")

    admin_balance = w3.eth.get_balance(admin_address)
    admin_balance_converted = w3.fromWei(admin_balance, "ether")

    print(
        f"The updated balance of the admin ({admin_address}) is now {admin_balance_converted} ETH.\n"
    )

    # checking the updated family holdings
    print("Checking the new amount in the family savings...\n")

    current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": admin_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(current_holdings, "ether")

    print(
        f"The current amount of ETH in the family savings is: {holdings_converted}.\n"
    )

    print("-----------------------------------------------------------------")
    print("-----------------------------------------------------------------")
    print("-----------------------------------------------------------------")
    print("\nWITHDRAW_EVERYTHING.PY SCRIPT IS NOW COMPLETE.\n")
    print("-----------------------------------------------------------------")
    print("-----------------------------------------------------------------")
    print("-----------------------------------------------------------------\n")
