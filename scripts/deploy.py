from brownie import EthSavings, accounts, config
import json


def main():
    admin = accounts.add(config["wallets"]["from_key"]["admin"])
    required_approvals = 2

    print("\nDeploying the contract...\n")
    contract = EthSavings.deploy(required_approvals, {"from": admin})
    print(
        "Contract has been successfully deployed.\n \nThe number of required approvals has been set to 2 in the constructor.\n"
    )
    print(f"The contract address is {contract.address}\n")

    print("Updating the abi file in the frontend...")

    abi = contract.abi
    json_object = json.dumps(abi)

    with open("./contract_data/goerli-eth/abi.json", "w") as file:
        file.write(json_object)
    with open("./frontend/my-app/utils/abi.json", "w") as file:
        file.write(json_object)

    print("Successfully updated the ABI.\n")

    print("Updating the contract address file in the frontend...")

    address = contract.address

    with open("./contract_data/goerli-eth/address.txt", "w") as file:
        file.write(address)
    with open("./frontend/my-app/utils/address.txt", "w") as file:
        file.write(address)

    print("Successfully updated the contract address.\n")

    print("The deployed contract is ready to be interacted with. :) \n")

    # gas usage: 1,920,716
