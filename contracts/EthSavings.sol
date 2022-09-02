// SPDX-License-Identifier: LGPL-3.0

pragma solidity ^0.8.10;

import "../interfaces/IERC20.sol";
import "../interfaces/IPool.sol";
import "../interfaces/IWETHGateway.sol";

/**
 * @title Generational Multi-Sig Savings Account
 * @author Okiki Olugunna
 * @notice This contract is intended to be used as a multisig savings account with your family
 * This same contract can be use for generations and generations, effectively maintaing your family's wealth
 * as long as the individuals are added to the family addresses.
 * @notice This contract can also be extended to other use cases where
 * you want to save funds as a group & want to implement multi-sig functionality
 * for withdrawals.
 * @dev This contract is intended for the Goerli Testnet.
 */
contract EthSavings {
    /**
     * @notice This is the admin of the contract
     * @dev The admin is the deployer of the contract
     */
    address payable public admin;

    /**
     * @notice This is the contract address of the Aave V3 Pool on Goerli
     */
    IPool public constant AAVE_V3_POOL =
        IPool(0x368EedF3f56ad10b9bC57eed4Dac65B26Bb667f6);

    /**
     * @notice This is the contract address of the WETH Gateway on Goerli
     * @dev This is where the ETH sent to the easySaveETH() function goes through to get to the Pool
     */
    IWETHGateway public constant WETH_GATEWAY =
        IWETHGateway(0xd5B55D3Ed89FDa19124ceB5baB620328287b915d);

    /**
     * @notice This is the contract address of the WETH 'a' token on Aave V3 (Goerli)
     * @dev The ETH sent to Aave V3 via the WETH Gateway accrues interest in the form of 'aWETH'
     */
    IERC20 public constant WETH_ATOKEN =
        IERC20(0x27B4692C93959048833f40702b22FE3578E77759);

    /// @notice This mapping stores whether someone is an admin
    mapping(address => bool) isAdmin;

    /// @notice This mapping stores whether someone is a family member
    mapping(address => bool) isFamilyMember;

    /// @notice This mapping stores how much each person has deposited over time
    mapping(address => uint256) public depositedAmount;

    /// @notice This mapping stores how much each person has withdrawn over time
    mapping(address => uint256) public totalWithdrawn;

    /// @notice Ths mapping stores the withdrawal requestID & links it to the amount the individual wants to withdraw
    mapping(uint256 => uint256) public requestIDToAmount;

    /// @notice Ths mapping stores the withdrawal requestID & the reason the individual want to make the withdrawal
    mapping(uint256 => string) public requestIDToReason;

    /// @notice This mapping counts the approvals that have been made for a requestID
    mapping(uint256 => uint256) public requestIDToApprovals;

    /// @notice This mapping links the requestID to the address who made the request
    mapping(uint256 => address) public requestIDToRequester;

    /// @notice This mapping stores whether an address has voted on a requestID
    mapping(address => mapping(uint256 => bool)) public hasVotedOnRequestID;

    /// @notice This mapping stores whether a requestID has been withdrawn
    mapping(uint256 => bool) public hasWithdrawn;

    /**
     * @notice This is the current request ID
     * @dev This value gets incremented each time someone makes a request
     */
    uint256 public requestID;

    /// @notice This is the required number of approvals for a request to go through
    uint256 public requiredApprovals;

    /// @notice This variable keeps track of the number of admins
    uint256 public numOfAdmins;

    /// @notice This variable keeps track of the number of family members
    uint256 public numOfFamilyMembers;

    /**
     * @notice This variable keeps track of the 'reserve ETH' in the contract
     * @dev 'reserveETH' is merely the ETH held directly in the contract & not developing interest in Aave
     */
    uint256 public reserveETH;

    // array of admins
    // address[] public allAdmins;

    /// @notice This array keeps track of non-family members who added to the savings
    address[] public nicePeople;

    // store the accrued fees
    // uint256 accruedFees;

    /**
     * @notice This event gets triggered when a family member contributes to the savings using easySaveETH()
     * @param _familyMember The address that added to the savings
     */
    event SavingsAdded(address _familyMember);

    /**
     * @notice This event gets triggered when non-family members add to the savings using easySaveETH()
     * @param _person The outsider address that added to the savings
     */
    event OutsiderAddedFunds(address indexed _person);

    /**
     * @notice This event gets triggered when someone requests a withdrawal from the savings using requestWithdrawal()
     * @param _requestID The requestID of the withdrawal request
     * @param _amount The amount requested to be withdrawn from the savings on Aave
     * @param _person The address making the request
     * @param _reason The reason for the withdrawal
     */
    event WithdrawalRequested(
        uint256 _requestID,
        uint256 _amount,
        address _person,
        string _reason
    );

    /**
     * @notice This event gets triggered when someone requests a withdrawal from the reserves using requestToWithdrawReserves()
     * @param _requestID The requestID of the reserves withdrawal request
     * @param _amount The amount requested to be withdrawn from the reserves
     * @param _person The address making the request
     * @param _reason The reason for the withdrawal
     */
    event ReservesWithdrawalRequested(
        uint256 _requestID,
        uint256 _amount,
        address _person,
        string _reason
    );

    /**
     * @notice This event gets triggered when every family member has approvaled a requestID
     * @dev If the requiredApprovals is much lower than the number of family members, then this will not be triggered often
     * @param _requestID The requestID that has been approved
     * @param _amount The amount that the requester wishes to withdraw from the savings
     */
    event AllApproved(uint256 _requestID, uint256 _amount);

    /**
     * @notice This event gets triggered when the number of required approvals is changed using changeRequiredApprovals()
     * @param _newApprovalNumber The new number of required approvals for a request to go through
     */
    event RequiredApprovalsChanged(uint256 _newApprovalNumber);

    /**
     * @notice This event gets triggered when a withdrawal is executed from the savings after the number of required approvals has been reached using withdrawSavedETH()
     * @param _person The address that executed the withdrawal from the Aave savings
     * @param _amount The amount that the address withdrew from savings
     */
    event WithdrawalMade(address _person, uint256 _amount);

    /**
     * @notice This event gets triggered when a reserve withdrawal is made after the number of required approvals has been reached using executeReserveWithdrawal()
     * @param _person The address that executed the withdrawal from the reserves
     * @param _amount The amount that the address withdrew from the reserves
     */
    event ReservesWithdrawalMade(address _person, uint256 _amount);

    /**
     * @notice This event gets triggered when a family member is added using addFamilyMember()
     * @param _person The address that has been added to the family
     */
    event FamilyMemberAdded(address _person);

    /**
     * @notice This event gets triggered when a family member is removed using removeFamilyMember()
     * @param _person The address that has been removed from the family
     */
    event FamilyMemberRemoved(address _person);

    /**
     * @notice This event gets triggered when an admin is added using addAdmin()
     * @param _newAdmin The address that has been added as an admin
     */
    event NewAdminAdded(address _newAdmin);

    /**
     * @notice This event gets triggered when an admin is removed
     * @param _oldAdmin The address that been removed as an admin
     */
    event AdminRemoved(address _oldAdmin);

    /// @dev Only family members can call functions marked by this modifier
    modifier onlyFamily() {
        require(
            isFamilyMember[msg.sender],
            "You are not a member of the family."
        );
        _;
    }

    /// @dev Only admins can call functions marked by this modifier
    modifier onlyAdmin() {
        require(isFamilyMember[msg.sender], "You are not an admin.");
        _;
    }

    /**
     * @dev constructor
     * @param _requiredApprovals The number to initialise as the required approvals for a withdrawal request to go through
     */
    constructor(uint256 _requiredApprovals) {
        // initialising the admin
        admin = payable(msg.sender);
        isAdmin[msg.sender] = true;
        numOfAdmins = 1;

        // initialising the admin as a family member
        isFamilyMember[msg.sender] = true;
        numOfFamilyMembers = 1;

        // initialising the number of approvals required for a withdrawal to be accepted
        requiredApprovals = _requiredApprovals;
    }

    /**
     * @notice This function allows family members & outsider to deposit ETH into this savings
     */
    function easySaveETH() external payable {
        // supplying ETH to Aave
        WETH_GATEWAY.depositETH{value: msg.value}(
            address(AAVE_V3_POOL),
            address(this),
            0
        );

        // updating the depositedAmount mapping
        depositedAmount[msg.sender] += msg.value;

        // if it was a family member that contributed
        if (isFamilyMember[msg.sender]) {
            emit SavingsAdded(msg.sender);
        }

        // if the address is not a family member
        if (!isFamilyMember[msg.sender]) {
            // adding the address to 'nicePeople' array
            nicePeople.push(msg.sender);
            // emitting event
            emit OutsiderAddedFunds(msg.sender);
        }
    }

    /**
     * @notice This function is for family members to view the current savings amount in Aave
     * @return uint256 The value returned is the 'aWETH' holdings
     */
    function viewFamilyHoldings() external view onlyFamily returns (uint256) {
        return WETH_ATOKEN.balanceOf(address(this));
    }

    /**
     * @notice This function is for a family member to request a withdrawal
     * @param _amount The amount to withdraw from Aave
     * @param _reason The reason for the withdrawal
     * @return requestID The requestID for this withdrawal request
     */
    function requestWithdrawal(uint256 _amount, string calldata _reason)
        external
        onlyFamily
        returns (uint256)
    {
        // initialising the savings balance
        uint256 aWETHBalance = WETH_ATOKEN.balanceOf(address(this));
        // requested amount to withdraw must be less than the savings
        require(_amount < aWETHBalance, "Reduce your withdrawal request.");

        // initialising an id for the request
        requestID += 1;
        // adding request and amount to withdrawal requests
        requestIDToAmount[requestID] = _amount;
        // initialising the requestID in the mapping of approvals
        requestIDToApprovals[requestID] = 0;
        // linking the requestser to the request ID
        requestIDToRequester[requestID] = msg.sender;
        // adding the reason to the requestID
        requestIDToReason[requestID] = _reason;
        // marking that the requestID has not been withdrawn
        hasWithdrawn[requestID] = false;

        // emitting withdrawal request event
        emit WithdrawalRequested(requestID, _amount, msg.sender, _reason);

        // returning the requestID to the msg.sender
        return requestID;
    }

    /**
     * @notice This function is for family members to view the reason for someone's request ID
     * @return string The value returned is the reason
     */
    function viewReasonForRequest(uint256 _requestID)
        external
        view
        onlyFamily
        returns (string memory)
    {
        return requestIDToReason[_requestID];
    }

    /**
     * @notice This function is for family members to approve a withdrawal submission
     * @notice If you try to approve your own request, this function will revert
     * @param _requestID The requestID to approve
     */
    function approveRequest(uint256 _requestID) external onlyFamily {
        // you cannot approve your own request
        require(
            requestIDToRequester[_requestID] != msg.sender,
            "You cannot approve your own request."
        );

        // incrementing the number of approvals for the request ID
        requestIDToApprovals[_requestID] += 1;

        // updating the mapping to show the msgsender has voted on the request
        hasVotedOnRequestID[msg.sender][_requestID] = true;

        // if approvals are equal to (num of family members -1), then emit AllApproved event
        if (requestIDToApprovals[_requestID] == (numOfFamilyMembers - 1)) {
            // emit event
            emit AllApproved(_requestID, requestIDToAmount[_requestID]);
        }
    }

    /**
     * @notice This function allows family members to revoke a withdrawal request they have already approved
     * @param _requestID The requestID to revoke your approval of
     * @notice You cannot call this function if you have not yet approved the request
     */
    function revokeRequest(uint256 _requestID) external onlyFamily {
        // the person revoking a request must have already approved before calling this
        require(
            hasVotedOnRequestID[msg.sender][_requestID],
            "Cannot revoke what you have not yet approved."
        );

        // decrementing the number of approvals for the request
        requestIDToApprovals[_requestID] -= 1;
    }

    /**
     * @notice This function allows family members to execute their requestID withdrawal of savings from Aave after the required number approvals has been reached
     * @param _requestID The requestID for the withdrawal request
     * @notice Another family member can call this function for you, but the funds will still go to the initial requester's account
     */
    function withdrawSavedETH(uint256 _requestID) external payable onlyFamily {
        // requiring that the family members have approved the sender to withdraw x amount from the savings
        require(
            requestIDToApprovals[_requestID] >= requiredApprovals,
            "More approvals are required before you can withdraw."
        );
        // making sure the person has not already executed their withdrawal
        require(
            !hasWithdrawn[_requestID],
            "You have already executed your withdrawal."
        );

        // marking that the requestID that been withdrawn
        hasWithdrawn[_requestID] = true;

        // initialising how much to withdraw from the savings
        uint256 withdrawalAmount = requestIDToAmount[_requestID];

        // updating the mapping of how much this member has withdrawn
        totalWithdrawn[msg.sender] += withdrawalAmount;

        // approving the gateway to spend the aWETH
        WETH_ATOKEN.approve(address(WETH_GATEWAY), withdrawalAmount);

        // withdrawing the interest and ETH + sending it to the owner
        WETH_GATEWAY.withdrawETH(
            address(AAVE_V3_POOL),
            withdrawalAmount,
            requestIDToRequester[_requestID]
        );

        // emitting event
        emit WithdrawalMade(msg.sender, withdrawalAmount);
    }

    /**
     * @notice This function allows the admin to withdraw all savings from Aave
     * @notice This function will not withdraw the ETH in the reserves
     * @dev Only the admin(s) can call this
     */
    function withdrawEverything() external payable onlyAdmin {
        // calculating the amount of aWETH earned
        uint256 aWETHBalance = WETH_ATOKEN.balanceOf(address(this));

        // approving the gateway to spend the aWETH
        WETH_ATOKEN.approve(address(WETH_GATEWAY), aWETHBalance);

        // withdrawing the interest and ETH + sending it to the owner
        WETH_GATEWAY.withdrawETH(
            address(AAVE_V3_POOL),
            type(uint256).max,
            msg.sender
        );

        // emitting event
        emit WithdrawalMade(msg.sender, aWETHBalance);
    }

    // function for admin to withdraw the accruedFees
    // function withdrawFees() external onlyAdmin {}

    /**
     * @notice This function allows the admin to add a family member this contract
     * @param _person The address to add to the family
     */
    function addFamilyMember(address _person) external onlyAdmin {
        // must not already be a family member
        require(!isFamilyMember[_person], "Already a family member.");

        // updating the mapping to hold add this person to the family
        isFamilyMember[_person] = true;

        // incrementing number of family members
        numOfFamilyMembers++;

        // emitting event for new person added
        emit FamilyMemberAdded(_person);
    }

    /**
     * @notice This function allows the admin to remove a family member from the contract
     * @param _person The address to remove from the family
     */
    function removeFamilyMember(address _person) external onlyAdmin {
        // must be a family member first to remove
        require(isFamilyMember[_person], "Address is not a family member.");

        // updating the mapping to hold add this person to the family
        isFamilyMember[_person] = false;

        // decrementing number of family members
        numOfFamilyMembers--;

        // emitting event for new person added
        emit FamilyMemberRemoved(_person);
    }

    /**
     * @notice This function allows the admin to change the required number of approvals for a withdrawal request to go through
     * @param _newApprovalNum The new number of required approvals for a request to go through
     */
    function changeRequiredApprovals(uint256 _newApprovalNum)
        external
        onlyAdmin
    {
        require(
            _newApprovalNum > 1,
            "Required number of approvals must be greater than 1."
        );
        // changing the required approvals
        requiredApprovals = _newApprovalNum;

        // emitting event for change in required approvals
        emit RequiredApprovalsChanged(_newApprovalNum);
    }

    /**
     * @notice This function allows the admin to add another admin
     * @param _newAdmin The address of the new admin to be added
     * @notice This new admin will *not* automatically be family
     * @dev To add this admin to family, also call the addFamilyMember function
     */
    function addAdmin(address _newAdmin) external onlyAdmin {
        // must not already be an admin
        require(!isAdmin[_newAdmin], "Already an admin.");

        // updating the mapping to hold add this person to the admins
        isAdmin[_newAdmin] = true;

        // incrementing the number of admins
        numOfAdmins++;

        // emitting event for new person added
        emit NewAdminAdded(_newAdmin);
    }

    /**
     * @notice This function allows an admin to remove an admin
     * @param _admin The address of the admin to remove
     * @notice If the admin being removed is also a family member, this function will not change their familial status
     */
    function removeAdmin(address _admin) external onlyAdmin {
        // the address must be an admin to remove it
        require(isAdmin[_admin], "Address to remove must be an admin first");

        // there must be at least 2 admins, if you want to remove an admin
        require(numOfAdmins >= 2, "There must always be at least 1 admin.");

        // updating the mapping to hold add this person to the admins
        isAdmin[_admin] = false;

        // decrementing the number of admins
        numOfAdmins--;

        // emitting event for new person added
        emit AdminRemoved(_admin);
    }

    /**
     * @notice This function allows anyone to send ETH to the 'reserves'
     * @notice Sending direct ETH to the contract like this will not send it to Aave to develop interest
     */
    receive() external payable {
        // the ETH received here can act as a reserve for the family savings
        reserveETH += msg.value;
    }

    /**
     * @notice This function allows family members to request a withdrawal from the reserves
     * @param _reason The reason for the withdrawal from the reserves
     * @return requestID The requestID for the withdrawal request
     * @dev 'reserves' is the ETH sitting directly in the contract
     */
    function requestToWithdrawReserves(string calldata _reason)
        external
        onlyFamily
        returns (uint256)
    {
        // getting the amount in reserves
        uint256 reservesAmount = address(this).balance;
        // reserves must be above 0 to request
        require(reservesAmount > 0, "No reserves.");

        // initialising an id for the request
        requestID += 1;

        // adding request and amount to withdrawal requests
        requestIDToAmount[requestID] = reservesAmount;

        // initialising the requestID in the mapping of approvals
        requestIDToApprovals[requestID] = 0;

        // linking the requestser to the request ID
        requestIDToRequester[requestID] = msg.sender;

        // adding the reason to the request ID
        requestIDToReason[requestID] = _reason;

        // marking that the requestID has not been withdrawn
        hasWithdrawn[requestID] = false;

        // emitting withdrawal request event
        emit ReservesWithdrawalRequested(
            requestID,
            reservesAmount,
            msg.sender,
            _reason
        );

        // returning the requestID to the msg.sender
        return requestID;
    }

    /**
     * @notice This function allows family members to execute the withdrawal from the reserves once the request has reached the required number of approvals
     * @param _requestID The requestID of the withdrawal request
     */
    function executeReserveWithdrawal(uint256 _requestID)
        external
        payable
        onlyFamily
    {
        // requiring that the family members have approved the sender to withdraw from the reserves
        require(
            requestIDToApprovals[_requestID] >= requiredApprovals,
            "More approvals are required before you can withdraw."
        );

        // only the person who made the request can call this
        require(
            requestIDToRequester[_requestID] == msg.sender,
            "Access denied."
        );

        // making sure the person has not already executed their withdrawal
        require(
            !hasWithdrawn[_requestID],
            "You have already executed your withdrawal."
        );

        // marking that the requestID that been withdrawn
        hasWithdrawn[_requestID] = true;

        // initialising how much to withdraw from the reserves
        uint256 withdrawalAmount = requestIDToAmount[_requestID];

        // updating the state variable of the reserves
        reserveETH -= withdrawalAmount;

        // withdrawing the reserves and sending it to the caller
        payable(msg.sender).transfer(withdrawalAmount);

        // emitting event
        emit ReservesWithdrawalMade(msg.sender, withdrawalAmount);
    }
}
