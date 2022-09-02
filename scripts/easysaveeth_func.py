from brownie import accounts, config
from web3 import Web3
from eth_utils import from_wei
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

    # checking the current family holdings
    print("\nChecking the current family holdings...\n")

    current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": admin_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(current_holdings, "ether")

    print(f"The current savings in aWETH are: {holdings_converted} aWETH\n")

    # initialising the amount of ETH to send
    amount_to_send = w3.toWei(Decimal("0.01"), "ether")  # 0.01 ETH
    # converting to ether
    amount_converted = w3.fromWei(amount_to_send, "ether")

    print(
        f"{admin_address} is sending {amount_converted} ETH to the family savings account...\n"
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
        f"Successfully added {amount_converted} ETH to the defi family savings account.\n"
    )

    # checking the current family holdings
    current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": admin_address}
    )
    # holdings converted
    holdings_converted = w3.fromWei(current_holdings, "ether")

    print(f"The current savings in aWETH are: {holdings_converted} aWETH :) \n")
