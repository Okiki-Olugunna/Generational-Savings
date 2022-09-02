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


def test_receive_eth():
    # instantiating the accounts
    admin = config["wallets"]["from_key"]["admin"]
    admin_address = config["addresses"]["admin_address"]

    # checking the current reserves
    initial_current_reserves = contract_instance.functions.reserveETH().call(
        {"from": admin_address}
    )
    # reserves converted
    initial_reserves_converted = w3.fromWei(initial_current_reserves, "ether")

    # initialising the amount of ETH to send
    amount_to_send = w3.toWei(Decimal("0.01"), "ether")  # 0.01 ETH

    # sending ETH to the family reserve holdings...
    # Getting the nonce
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

    # checking the current reserves
    new_current_reserves = contract_instance.functions.reserveETH().call(
        {"from": admin_address}
    )
    # reserves converted
    new_reserves_converted = w3.fromWei(new_current_reserves, "ether")

    # asserting that the new amount of reserves are greater than the intial reserves
    assert new_reserves_converted > initial_reserves_converted
