## Generational DeFi Savings

### Multi-Signature Savings Account to collectively save funds as a family for generations

Website: https://generational-savings.okikicodes.repl.co/ 

### Demo:

< insert screen-recorded video >

#### Interacting directly with the contract:

- Calling the 'easySaveEth' function will send your ETH to Aave V3 via the WETH Gateway
- Sending ETH directly to the contract will not send it to Aave, and will act as "reserve savings"
- In order to withdraw funds from the savings, the individual will need to put in make a request via the 'requestWithdrawal' function, with a reason of the withdrawal
  - family members can review the request, and give their approval via the 'approveRequest' function
  - if a family member changes their mind about an approval, they can call the 'revokeRequest' function
  - when the number of approvals is at least 'requiredApprovals', the individual who wants to withdraw funds may now call 'withdrawSavedETH'

#### Admin Rights:

- The admin of the contract can add and remove extra family members or admins once the contract is deployed
- Admins can also change the number of required approvals in order for a withdrawal request to go through - however this number must always be above 1
- The admin also has the right to withdraw everything in the savings by calling 'withdrawEverything' - however, this will not withdraw the reserves in the contract

#### Scripts & Tests:

- This contract was rigorously tested - all scripts & tests can be found in the scripts and tests folders respectively
- To see the most real-life simulation of this contract, have a look at the script "make_a_withdrawal.py"
