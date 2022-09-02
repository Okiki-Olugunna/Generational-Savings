from brownie import config
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

    # checking the current reserves
    print("\nChecking the current holdings in the reserve...\n")

    current_reserves = contract_instance.functions.reserveETH().call(
        {"from": admin_address}
    )
    # reserves converted
    reserves_converted = w3.fromWei(current_reserves, "ether")

    print(f"The current reserve holdings are: {reserves_converted} ETH\n")

    # initialising the amount of ETH to send
    amount_to_send = w3.toWei(Decimal("0.01"), "ether")  # 0.01 ETH
    # converting to ether
    amount_converted = w3.fromWei(amount_to_send, "ether")

    print(
        f"{admin_address} is sending {amount_converted} ETH to the family reserve holdings...\n"
    )

    # depositing some eth into the reserve

    print(f"Getting the nonce of {admin_address}...\n")
    nonce = w3.eth.get_transaction_count(admin_address)

    print("Signing the transaction...\n")
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
    print("Sending the transaction...\n")
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print(
        f"{admin_address} has successfully added {amount_converted} ETH to the family reserve holdings.\n"
    )

    tx_hash = w3.toHex(w3.keccak(signed_tx.rawTransaction))
    print(f"Transaction hash: {tx_hash}\n")

    # checking the current reserves
    current_reserves = contract_instance.functions.reserveETH().call(
        {"from": admin_address}
    )
    # reserves converted
    reserves_converted = w3.fromWei(current_reserves, "ether")

    print(f"The current reserve holdings are now: {reserves_converted} ETH :) \n")
