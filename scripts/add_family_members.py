from brownie import accounts, config
from web3 import Web3


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

    # family member to add
    family_member_2 = accounts.add(config["wallets"]["from_key"]["family_member_2"])

    """ extra family memebers:
    family_member_3 = accounts.add(config["wallets"]["from_key"]["family_member_3"])
    family_member_4 = accounts.add(config["wallets"]["from_key"]["family_member_4"])
    """

    # getting the current count of family members
    num_of_family = contract_instance.functions.numOfFamilyMembers().call()
    print(f"\nThere are currently {num_of_family} family members in this contract.\n")

    # adding the new family member
    print(f"Adding family member {family_member_2.address}...\n")

    # getting the nonce of the admin that will be sending the transaction
    nonce = w3.eth.getTransactionCount(admin_address)
    # building the transaction
    tx = contract_instance.functions.addFamilyMember(
        family_member_2.address
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

    print(f"Family member {family_member_2.address} has been added.\n")

    # checking the new number of family members
    num_of_family = contract_instance.functions.numOfFamilyMembers().call()
    print(f"There are now {num_of_family} family members in this contract.\n")
