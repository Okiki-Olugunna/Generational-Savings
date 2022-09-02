from brownie import accounts, config, network
from web3 import Web3


w3 = Web3(Web3.WebsocketProvider(config["provider"]["websockets"]))


with open("./contract_data/goerli-eth/address.txt") as file_a:
    contract_address = file_a.read()

with open("./contract_data/goerli-eth/abi.json") as file_b:
    contract_abi = file_b.read()


def main():
    # instantiating the accounts
    admin = accounts.add(config["wallets"]["from_key"]["admin"])
    family_member_2 = accounts.add(config["wallets"]["from_key"]["family_member_2"])
    family_member_3 = accounts.add(config["wallets"]["from_key"]["family_member_3"])
    family_member_4 = accounts.add(config["wallets"]["from_key"]["family_member_4"])

    # initialising the contract instance
    contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)

    # checking the number of family memebers
    num_of_family = contract_instance.functions.numOfFamilyMembers().call()
    print(f"\nNumber of family members: {num_of_family}\n")

    # checking the number of admins
    num_of_admins = contract_instance.functions.numOfAdmins().call()
    print(f"Number of admins: {num_of_admins}\n")

    # checking the required approvals
    required_approvals = contract_instance.functions.requiredApprovals().call()
    print(
        f"The required number of approvals for a withdrawal to go through is: {required_approvals}\n"
    )

    # checking the current family holdings
    current_holdings = contract_instance.functions.viewFamilyHoldings().call(
        {"from": admin.address}
    )
    current_holdings_converted = w3.fromWei(current_holdings, "ether")
    print(f"The current savings in aWETH are: {current_holdings_converted} aWETH\n")

    # checking the reserve ETH
    reserve_eth = contract_instance.functions.reserveETH().call()
    reserve_eth_converted = w3.fromWei(reserve_eth, "ether")
    print(f"The current reserve ETH in the contract is: {reserve_eth_converted} ETH\n")
