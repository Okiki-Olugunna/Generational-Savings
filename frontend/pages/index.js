// import abi from "../utils/EthSavings.json";
import abi from "../utils/abi.json";
// import address from "../utils/address.txt";
import ThankYouPopup from "./components/ThankYouPopup";
import WithdrawPopup from "./components/WithdrawPopup";
import Loading from "./components/Loading";
import { BigNumber, ethers } from "ethers";
import React, { useEffect, useState } from "react";
// import { useDisconnect } from "@thirdweb-dev/react";
import Head from "next/head";
import Image from "next/image";
import styles from "../styles/Home.module.css";
import AddFamilyMember from "./components/AddFamilyMember";
import AddAdmin from "./components/AddAdmin";

export default function Home() {
  // loading the contract data
  const contractABI = abi.abi;
  // console.log(contractABI);

  const contractAddress = "0x20f7310c60b305C655d47Ae1569a61E542AF4536";
  // console.log("Contract address:", contractAddress);

  // savings amount to show on screen later
  let convertedFromWei;
  // reason of request ID to show on screen later
  // let reasonOfRequestID;

  // Component states
  // sets what account is currently connected
  const [currentAccount, setCurrentAccount] = useState(false);
  // used to show buttons with admin privileges
  const [adminAccount, setAdminAccount] = useState(false);

  // used when admin is adding a member
  const [familyAddress, setFamilyAddress] = useState("");
  const [newAdminAddress, setNewAdminAddress] = useState("");

  // sets the ETH amount to deposit or withdraw
  const [ethAmount, setETHAmount] = useState("");

  // the trigger to show the individial's request ID after making a withdrawal request
  const [hasRequested, setHasRequested] = useState(false);
  // sets the request ID for a withdrawal request
  const [requestID, setRequestID] = useState("");
  // sets the request ID to approve a request
  const [approveRequestID, setApproveRequestID] = useState("");
  // sets the request ID to view the reason for a request
  const [findReasonOfRequestID, setFindReasonOfRequestID] = useState("");
  // sets the reason to show
  const [reasonForRequestID, setReasonForRequestID] = useState("");
  // shows whether the request has executed - for the view reason function
  const [requestExecuted, setRequestAlreadyExecuted] = useState("");

  // sets the request ID to execute a request
  const [executeRequestID, setExecuteRequestID] = useState("");

  // sets the savings amount when viewing the current savings
  const [currentSavingsAmount, setCurrentSavingsAmount] = useState("");

  const [name, setName] = useState("");
  // sets the reason for a withdrawal request
  const [message, setMessage] = useState("");

  // different loading states
  const [loading, setLoadingState] = useState(false);
  const [loadingRequest, setLoadingRequestState] = useState(false);
  const [loadingApproval, setLoadingApprovalState] = useState(false);
  const [loadingWithdrawal, setLoadingWithdrawalState] = useState(false);

  const [loadingAddFamily, setLoadingAddFamilyState] = useState(false);
  const [loadingRemoveFamily, setLoadingRemoveFamilyState] = useState(false);
  const [loadingAddAdmin, setLoadingAddAdminState] = useState(false);
  const [loadingRemoveAdmin, setLoadingRemoveAdminState] = useState(false);

  // popups
  const [thankYouPopUp, setThankYouPopUp] = useState(false);
  const [requestPopUp, setRequestPopUp] = useState(false);
  const [approvePopUp, setApprovePopUp] = useState(false);
  const [withdrawPopUp, setWithdrawPopUp] = useState(false);

  // events for the input fields
  const onETHAmountChange = (event) => {
    setETHAmount(event.target.value);
  };

  // request
  const onRequestIDChange = (event) => {
    setRequestID(event.target.value);
  };

  // approve
  const onRequestIDChange2 = (event) => {
    setApproveRequestID(event.target.value);
  };

  // execute
  const onRequestIDChange3 = (event) => {
    setExecuteRequestID(event.target.value);
  };

  // view reason
  const onRequestIDChange4 = (event) => {
    setFindReasonOfRequestID(event.target.value);
  };

  const onNameChange = (event) => {
    setName(event.target.value);
  };

  const onMessageChange = (event) => {
    setMessage(event.target.value);
  };

  const onFamilyAddressChange = (event) => {
    setFamilyAddress(event.target.value);
  };

  const onAddAdminAddressChange = (event) => {
    setNewAdminAddress(event.target.value);
  };

  // function to connect to metamask
  const connectWallet = async () => {
    console.log("Requesting account...");

    // setAdminAccount(false);

    // getting the chainid of the current network the user is connected to
    const chainId = await window.ethereum.request({ method: "eth_chainId" });

    if (typeof window.ethereum) {
      console.log("Ethereum wallet detected...");

      if (chainId !== "0x5") {
        // switching the user's network to Goerli
        await window.ethereum.request({
          method: "wallet_switchEthereumChain",
          params: [{ chainId: "0x5" }],
        });
      }

      try {
        const accounts = await window.ethereum.request({
          method: "eth_requestAccounts",
        });
        console.log(accounts[0]);
        setCurrentAccount(accounts[0]);
      } catch (error) {
        console.log("Error connecting..");
      }
    } else {
      console.log("Please install metamask");
    }

    // check to the see if the wallet address is the admin
    if (ethereum) {
      const provider = new ethers.providers.Web3Provider(ethereum, "any");
      const signer = provider.getSigner();
      const signerAddress = await signer.getAddress();
      console.log(`The signers address is: ${signerAddress}`);

      // loading the contract
      const ethSavingsContract = new ethers.Contract(
        contractAddress,
        contractABI,
        signer
      );

      // loading the admin from the contract
      console.log("checking the wallet address..");
      const admin = await ethSavingsContract.admin();
      console.log(`The admin of the contract is: ${admin}`);

      // if the wallet address is equal to the address
      if (signerAddress == admin) {
        // show admin buttons
        setAdminAccount(true);
        console.log("Admin is connected");
      } else {
        console.log("Current account is not the admin");
      }
    }
  };

  const isWalletConnected = async () => {
    if (typeof window.ethereum) {
      try {
        const accounts = await ethereum.request({ method: "eth_accounts" });
        console.log("accounts: ", accounts);

        if (accounts.length > 0) {
          const account = accounts[0];
          console.log("Wallet is connected! " + account);
        } else {
          console.log("Make sure MetaMask is connected");
        }
      } catch (error) {
        console.log("error: ", error);
      }
    }
  };

  // function to add to the savings
  const addToSavings = async () => {
    console.log("Contract ABI:", contractABI);
    console.log("Contract address:", contractAddress);

    console.log("Connecting to account...");
    try {
      const { ethereum } = window;

      if (ethereum) {
        console.log("Getting the provider...");
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        console.log("Provider:", provider);

        console.log("Getting the signer...");
        const signer = provider.getSigner();
        console.log("Signer:", signer);

        console.log("Initialising the contract...");
        const ethSavingsContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );
        console.log("Contract:", ethSavingsContract);

        console.log("Setting the amount of ETH to send...");
        // const sendAmount = ;
        console.log("Adding ETH to savings...");
        const sendEthTxn = await ethSavingsContract.easySaveETH({
          value: ethers.utils.parseEther(ethAmount),
        });

        console.log("Waiting for the transaction to go through...");
        // show loading popup while transaction is being mined
        setLoadingState(true);
        await sendEthTxn.wait();

        console.log("Transaction mined ", sendEthTxn.hash);
        console.log("Added to savings!");

        // Clear the form fields.
        setName("");
        setMessage("");

        // remove loading popup
        setLoadingState(false);
        // show thank you popup
        setThankYouPopUp(true);
      }
    } catch (error) {
      console.log(error);
    }
  };

  // function to view the savings amount
  const viewSavingsAmount = async () => {
    console.log("Contract ABI:", contractABI);
    console.log("Contract address:", contractAddress);

    console.log("Connecting to account...");
    try {
      const { ethereum } = window;

      if (ethereum) {
        console.log("Getting the provider...");
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        console.log("Provider:", provider);

        console.log("Getting the signer...");
        const signer = provider.getSigner();
        console.log("Signer:", signer);

        console.log("Initialising the contract...");
        const ethSavingsContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );
        console.log("Contract:", ethSavingsContract);

        console.log("Calling the contract...");
        console.log("Finding out the amount in savings...");
        const viewSavingsTxn = await ethSavingsContract.viewFamilyHoldings();

        console.log("Waiting for the transaction to go through...");
        // show loading popup while transaction is being mined
        setLoadingState(true);
        // await viewSavingsTxn.wait(); - view function
        console.log("Transaction mined ", viewSavingsTxn.hash);

        console.log("Current savings amount in hex:", viewSavingsTxn);
        const convertedFromHex = BigNumber.from(viewSavingsTxn);

        convertedFromWei = ethers.utils.formatEther(convertedFromHex);
        console.log(`Current savings amount is ${convertedFromWei} aWETH`);
        // // remove loading popup
        setLoadingState(false);

        setCurrentSavingsAmount(`${convertedFromWei} aWETH`);
      }
    } catch (error) {
      console.log("You are not permitted to view this function.");
      console.log(
        "Connect your MetaMask, or ask the admin to join the family to view the savings amount."
      );
    }
  };

  // function to request A Withdrawal
  const requestAWithdrawal = async () => {
    console.log("Contract ABI:", contractABI);
    console.log("Contract address:", contractAddress);
    //
    setHasRequested(false);

    console.log("Connecting to account...");
    try {
      const { ethereum } = window;

      if (ethereum) {
        console.log("Getting the provider...");
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        console.log("Provider:", provider);

        console.log("Getting the signer...");
        const signer = provider.getSigner();
        console.log("Signer:", signer);

        console.log("Initialising the contract...");
        const ethSavingsContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );
        console.log("Contract:", ethSavingsContract);

        console.log("Setting the amount of ETH to request...");
        // const requestAmount = ;
        console.log(
          `You are requesting ${ethers.utils.parseUnits(
            ethAmount,
            "ether"
          )} wei`
        );
        console.log("Making request...");
        const requestTxn = await ethSavingsContract.requestWithdrawal(
          ethers.utils.parseUnits(ethAmount, "ether"),
          // ethAmount,
          message
        );

        console.log("Waiting for the transaction to go through...");
        // show loading popup while transaction is being mined
        setLoadingRequestState(true);
        await requestTxn.wait();

        console.log("Transaction mined ", requestTxn.hash);
        console.log("Request made!");
        console.log("Your request tx:", requestTxn);
        // console.log(requestTxn);

        //
        console.log("Getting the request ID...");
        const newRequestID = await ethSavingsContract.requestID();
        const convertedFromHex = newRequestID.toNumber();
        console.log("Your request ID is:", convertedFromHex);

        // show the request ID
        setHasRequested(true);
        // remove loading popup
        setLoadingRequestState(false);

        // Clear the form fields.
        setName("");
        setMessage("");

        // displaying the request ID
        setRequestID(`Your request ID is: ${convertedFromHex}`);
      }
    } catch (error) {
      console.log(error);
    }
  };

  // function to approve A Request
  const approveARequest = async () => {
    console.log("Contract ABI:", contractABI);
    console.log("Contract address:", contractAddress);

    console.log("Connecting to account...");
    try {
      const { ethereum } = window;

      if (ethereum) {
        console.log("Getting the provider...");
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        console.log("Provider:", provider);

        console.log("Getting the signer...");
        const signer = provider.getSigner();
        console.log("Signer:", signer);

        console.log("Initialising the contract...");
        const ethSavingsContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );
        console.log("Contract:", ethSavingsContract);

        console.log("Storing the request ID...");
        console.log("Approving the request...");
        const approveTxn = await ethSavingsContract.approveRequest(
          approveRequestID
        );

        console.log("Waiting for the transaction to go through...");
        // show loading popup while transaction is being mined
        setLoadingApprovalState(true);
        await approveTxn.wait();

        console.log("Transaction mined ", approveTxn.hash);
        console.log("Request has been approved!");

        // Clear the form fields.
        setName("");
        setMessage("");

        // remove loading popup
        setLoadingApprovalState(false);
      }
    } catch (error) {
      console.log(error);
    }
  };

  // function to view the reason for a requestID
  const viewReasonForRequest = async () => {
    console.log("Contract ABI:", contractABI);
    console.log("Contract address:", contractAddress);

    console.log("Connecting to account...");
    try {
      const { ethereum } = window;

      if (ethereum) {
        console.log("Getting the provider...");
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        console.log("Provider:", provider);

        console.log("Getting the signer...");
        const signer = provider.getSigner();
        console.log("Signer:", signer);

        console.log("Initialising the contract...");
        const ethSavingsContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );
        console.log("Contract:", ethSavingsContract);

        console.log("Calling the contract...");
        console.log("Getting the reason for the request ID...");
        const viewReasonTxn = await ethSavingsContract.viewReasonForRequest(
          findReasonOfRequestID
        );
        const viewAmountTxn = await ethSavingsContract.requestIDToAmount(
          findReasonOfRequestID
        );

        console.log("Waiting for the transaction to go through...");
        // show loading popup while transaction is being mined
        // setLoadingState(true);
        // await viewSavingsTxn.wait(); - view function
        console.log(
          "Transaction mined ",
          viewReasonTxn.hash,
          viewAmountTxn.hash
        );

        // converting from wei
        // const convertedFromHex = BigNumber.from(viewSavingsTxn);

        const converted = ethers.utils.formatEther(viewAmountTxn);

        console.log(
          `The reason for the request is ${viewReasonTxn} & the amount requested is ${converted} ETH`
        );

        setReasonForRequestID(
          `The reason for the request is "${viewReasonTxn}" - and the amount requested is ${converted} ETH`
        );

        const thisHasExecuted = await ethSavingsContract.hasWithdrawn(
          findReasonOfRequestID
        ); // returns true or false

        // console.log(thisHasExecuted);
        if (thisHasExecuted) {
          console.log("This request has been already been withdrawn");
          setRequestAlreadyExecuted(
            `This request has been already been withdrawn`
          );
        } else {
          setRequestAlreadyExecuted("");
        }
      }
    } catch (error) {
      console.log("You are not permitted to view this function.");
      console.log(
        "Connect your MetaMask, or ask the admin to join the family to view the savings amount."
      );
    }
  };

  // function to execute A Withdrawal
  const executeAWithdrawal = async () => {
    console.log("Contract ABI:", contractABI);
    console.log("Contract address:", contractAddress);

    console.log("Connecting to account...");
    try {
      const { ethereum } = window;

      if (ethereum) {
        console.log("Getting the provider...");
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        console.log("Provider:", provider);

        console.log("Getting the signer...");
        const signer = provider.getSigner();
        console.log("Signer:", signer);

        console.log("Initialising the contract...");
        const ethSavingsContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );
        console.log("Contract:", ethSavingsContract);

        console.log("Storing the request ID...");
        console.log("Executing the withdrawal...");
        const withdrawalTxn = await ethSavingsContract.withdrawSavedETH(
          executeRequestID
        );

        console.log("Waiting for the transaction to go through...");
        // show loading popup while transaction is being mined
        setLoadingWithdrawalState(true);
        await withdrawalTxn.wait();

        console.log("Transaction mined ", withdrawalTxn.hash);
        console.log("Request made!");

        // Clear the form fields.
        setName("");
        setMessage("");

        // remove loading popup
        setLoadingWithdrawalState(false);
        // show thank you popup
        setWithdrawPopUp(true);
      }
    } catch (error) {
      console.log(error);
    }
  };

  // add a family member - for the admin of contract
  const addFamilyMember = async () => {
    console.log("Contract ABI:", contractABI);
    console.log("Contract address:", contractAddress);

    console.log("Connecting to account...");
    try {
      const { ethereum } = window;

      if (ethereum) {
        console.log("Getting the provider...");
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        console.log("Provider:", provider);

        console.log("Getting the signer...");
        const signer = provider.getSigner();
        console.log("Signer:", signer);

        console.log("Initialising the contract...");
        const ethSavingsContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );
        console.log("Contract:", ethSavingsContract);

        console.log("Storing the family member's address...");
        console.log("Executing the transaction...");
        const addFamilyTxn = await ethSavingsContract.addFamilyMember(
          familyAddress
        );

        console.log("Waiting for the transaction to go through...");
        // show loading popup while transaction is being mined
        setLoadingAddFamilyState(true);
        await addFamilyTxn.wait();

        console.log("Transaction mined ", addFamilyTxn.hash);
        console.log("Family member added!");

        // Clear the form fields.
        setName("");
        setMessage("");

        // remove loading popup
        setLoadingAddFamilyState(false);
      }
    } catch (error) {
      console.log(error);
    }
  };

  // remove a family member - for the admin of contract
  const removeFamilyMember = async () => {
    console.log("Contract ABI:", contractABI);
    console.log("Contract address:", contractAddress);

    console.log("Connecting to account...");
    try {
      const { ethereum } = window;

      if (ethereum) {
        console.log("Getting the provider...");
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        console.log("Provider:", provider);

        console.log("Getting the signer...");
        const signer = provider.getSigner();
        console.log("Signer:", signer);

        console.log("Initialising the contract...");
        const ethSavingsContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );
        console.log("Contract:", ethSavingsContract);

        console.log("Storing the family member's address...");
        console.log("Executing the transaction...");
        const addFamilyTxn = await ethSavingsContract.removeFamilyMember(
          familyAddress
        );

        console.log("Waiting for the transaction to go through...");
        // show loading popup while transaction is being mined
        setLoadingRemoveFamilyState(true);
        await addFamilyTxn.wait();

        console.log("Transaction mined ", addFamilyTxn.hash);
        console.log("Family member removed!");

        // Clear the form fields.
        setName("");
        setMessage("");

        // remove loading popup
        setLoadingRemoveFamilyState(false);

        // show thank you popup
        // setWithdrawPopUp(true);
      }
    } catch (error) {
      console.log(error);
    }
  };

  // add an admin - for the admin of contract
  const addAnAdmin = async () => {
    console.log("Contract ABI:", contractABI);
    console.log("Contract address:", contractAddress);

    console.log("Connecting to account...");
    try {
      const { ethereum } = window;

      if (ethereum) {
        console.log("Getting the provider...");
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        console.log("Provider:", provider);

        console.log("Getting the signer...");
        const signer = provider.getSigner();
        console.log("Signer:", signer);

        console.log("Initialising the contract...");
        const ethSavingsContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );
        console.log("Contract:", ethSavingsContract);

        console.log("Storing the admin's address...");
        console.log("Executing the transaction...");
        const addAdminTxn = await ethSavingsContract.addAdmin(newAdminAddress);

        console.log("Waiting for the transaction to go through...");
        // show loading popup while transaction is being mined
        setLoadingAddAdminState(true);
        await addFamilyTxn.wait();

        console.log("Transaction mined ", addAdminTxn.hash);
        console.log("Admin added!");

        // Clear the form fields.
        setName("");
        setMessage("");

        // remove loading popup
        setLoadingAddAdminState(false);
      }
    } catch (error) {
      console.log(error);
    }
  };

  // remove an admin - for the admin of contract
  const removeAnAdmin = async () => {
    console.log("Contract ABI:", contractABI);
    console.log("Contract address:", contractAddress);

    console.log("Connecting to account...");
    try {
      const { ethereum } = window;

      if (ethereum) {
        console.log("Getting the provider...");
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        console.log("Provider:", provider);

        console.log("Getting the signer...");
        const signer = provider.getSigner();
        console.log("Signer:", signer);

        console.log("Initialising the contract...");
        const ethSavingsContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );
        console.log("Contract:", ethSavingsContract);

        console.log("Storing the admin's address...");
        console.log("Executing the transaction...");
        const removeAdminTxn = await ethSavingsContract.removeAdmin(
          newAdminAddress
        );

        console.log("Waiting for the transaction to go through...");
        // show loading popup while transaction is being mined
        setLoadingRemoveAdminState(true);
        await addFamilyTxn.wait();

        console.log("Transaction mined ", removeAdminTxn.hash);
        console.log("Admin removed!");

        // Clear the form fields.
        setName("");
        setMessage("");

        // remove loading popup
        setLoadingRemoveAdminState(false);
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className={styles.container}>
      <Head>
        <title>Generational Multi-Sig Savings</title>
        <meta name="description" content="Save money as a group." />
        {/* <link rel="icon" href="/multiple-keys-removebg.png" /> */}
        <link rel="icon" href="/padlock-bw-removebg.png" />
      </Head>

      <nav>
        {/* <button
          id="adminButton"
          className="connect"
          type="button"
          onClick={connectWallet}
        >
          Admin{" "}
        </button> */}

        <button
          id="connectButton"
          className="connect"
          type="button"
          onClick={connectWallet}
        >
          {!currentAccount ? "Connect Wallet" : "Connected"}
        </button>
      </nav>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Generational <a>Multi-Sig</a> <br></br> Savings
        </h1>

        <Image
          src={"/multiple-keys-removebg.png"}
          width={202}
          height={168}
          alt="Multiple Keys"
        />

        <div className={styles.grid}>
          {/* Admin Only Button */}
          <AddFamilyMember
            trigger={adminAccount}
            setTrigger={setAdminAccount}
            className={styles.admincard}
          >
            <a>
              <h2>Add a Family Member</h2>
              <div>
                {loadingAddFamily ? (
                  <center>
                    <Loading trigger={loadingAddFamily}>
                      <div></div>
                    </Loading>
                  </center>
                ) : (
                  <div>
                    <p>Input an address:</p>
                    <p>
                      <input
                        id=""
                        name=""
                        type={"text"}
                        placeholder="0xFC6hP81..."
                        onChange={onFamilyAddressChange}
                      ></input>
                    </p>
                    <button type="submit" onClick={addFamilyMember}>
                      Confirm
                    </button>
                  </div>
                )}
              </div>
            </a>
          </AddFamilyMember>

          {/* Admin Only Button */}
          <AddFamilyMember
            trigger={adminAccount}
            setTrigger={setAdminAccount}
            className={styles.admincard}
          >
            <a>
              <h2>Remove a Family Member</h2>
              <div>
                {loadingRemoveFamily ? (
                  <center>
                    <Loading trigger={loadingRemoveFamily}>
                      <div></div>
                    </Loading>
                  </center>
                ) : (
                  <div>
                    <p>Input an address:</p>
                    <p>
                      <input
                        id=""
                        name=""
                        type={"text"}
                        placeholder="0xFC6hP81..."
                        onChange={onFamilyAddressChange}
                      ></input>
                    </p>
                    <button type="submit" onClick={removeFamilyMember}>
                      Confirm
                    </button>
                  </div>
                )}
              </div>
            </a>
          </AddFamilyMember>
        </div>

        <div className={styles.grid}>
          {/* Admin Only Button */}
          <AddAdmin
            trigger={adminAccount}
            setTrigger={setAdminAccount}
            className={styles.admincard}
          >
            <a>
              <h2>Add an Admin</h2>
              <div>
                {loadingAddAdmin ? (
                  <center>
                    <Loading trigger={loadingAddAdmin}>
                      <div></div>
                    </Loading>
                  </center>
                ) : (
                  <div>
                    <p>Input an address:</p>
                    <p>
                      <input
                        id=""
                        name=""
                        type={"text"}
                        placeholder="0xFC6hP81..."
                        onChange={onAddAdminAddressChange}
                      ></input>
                    </p>
                    <button type="submit" onClick={addAnAdmin}>
                      Confirm
                    </button>
                  </div>
                )}
              </div>
            </a>
          </AddAdmin>

          {/* Admin Only Button */}
          <AddAdmin
            trigger={adminAccount}
            setTrigger={setAdminAccount}
            className={styles.admincard}
          >
            <a>
              <h2>Remove an Admin</h2>
              <div>
                {loadingRemoveAdmin ? (
                  <center>
                    <Loading trigger={loadingRemoveAdmin}>
                      <div></div>
                    </Loading>
                  </center>
                ) : (
                  <div>
                    <p>Input an address:</p>
                    <p>
                      <input
                        id=""
                        name=""
                        type={"text"}
                        placeholder="0xFC6hP81..."
                        onChange={onAddAdminAddressChange}
                      ></input>
                    </p>
                    <button type="submit" onClick={removeAnAdmin}>
                      Confirm
                    </button>
                  </div>
                )}
              </div>
            </a>
          </AddAdmin>
        </div>

        {/* 'loading' pop-up */}
        {/* <center>
          <Loading trigger={loading}>
            <div></div>
          </Loading>
        </center> */}

        {/* 'thank you' pop-up */}
        <ThankYouPopup trigger={thankYouPopUp} setTrigger={setThankYouPopUp}>
          <h3>Thank you! Savings have been added :) </h3>
        </ThankYouPopup>

        <a className={styles.customcard}>
          <h2>Add To Savings</h2>
          <p>Type an amount to deposit:</p>
          <p>
            <input
              // id="coffeeAmount"
              // name="coffeeAmount"
              type={"text"}
              placeholder="0.5"
              onChange={onETHAmountChange}
            ></input>
          </p>
          <p>
            <button type="submit" onClick={addToSavings}>
              Deposit ETH
            </button>
          </p>
        </a>

        <a className={styles.customcard}>
          <h2>View Current Savings Amount</h2>
          <p>Only Family Members Can View</p>
          <p>Current savings: {currentSavingsAmount}</p>
          <p>
            <button type="submit" onClick={viewSavingsAmount}>
              View Savings
            </button>
          </p>
        </a>

        <div className={styles.grid}>
          <a className={styles.requestcard}>
            <h2>Request a Withdrawal</h2>
            <div>
              {loadingRequest ? (
                <center>
                  <Loading trigger={loadingRequest}>
                    <div></div>
                  </Loading>
                </center>
              ) : (
                <div>
                  <p>Type an amount of ETH to withdraw:</p>
                  <p>
                    <input
                      id="coffeeAmount"
                      name="coffeeAmount"
                      type={"text"}
                      placeholder="0.5"
                      onChange={onETHAmountChange}
                    ></input>
                  </p>
                  <p>Reason for withdrawal:</p>
                  <p>
                    <input
                      id="coffeeAmount"
                      name="coffeeAmount"
                      type={"text"}
                      placeholder="Buying a house..."
                      onChange={onMessageChange}
                    ></input>
                  </p>
                  <button type="submit" onClick={requestAWithdrawal}>
                    Make Request
                  </button>
                </div>
              )}
            </div>
            <p trigger={hasRequested}>{requestID}</p>
          </a>

          <a className={styles.approvecard}>
            <h2>Approve a Request</h2>
            <div>
              {loadingApproval ? (
                <center>
                  <Loading trigger={loadingApproval}>
                    <div></div>
                  </Loading>
                </center>
              ) : (
                <div>
                  <p>Input the request ID:</p>
                  <p>
                    <input
                      id="coffeeAmount"
                      name="coffeeAmount"
                      type="number"
                      placeholder="1"
                      onChange={onRequestIDChange2}
                    ></input>
                  </p>
                  <p>
                    <button type="submit" onClick={approveARequest}>
                      Approve
                    </button>
                  </p>
                </div>
              )}
            </div>
          </a>

          <a className={styles.customcard}>
            <h2>View The Reason for a Request</h2>
            <p>Input the request ID:</p>
            <p>
              <input
                id=""
                name=""
                type="number"
                placeholder="1"
                onChange={onRequestIDChange4}
              ></input>
            </p>
            <br></br>
            <p>
              {/* Reason:  */}
              {reasonForRequestID}
            </p>
            <br></br>
            <p>{requestExecuted}</p>
            {/* <br></br> */}
            <p>
              <button type="submit" onClick={viewReasonForRequest}>
                View Reason
              </button>
            </p>
          </a>

          {/* 'Withdrawals have been made' pop-up */}
          <WithdrawPopup trigger={withdrawPopUp} setTrigger={setWithdrawPopUp}>
            <h3>The withdrawal has been successfully executed!</h3>
          </WithdrawPopup>

          <a className={styles.executecard}>
            <h2>Execute a Withdrawal</h2>
            <div>
              {loadingWithdrawal ? (
                <center>
                  <Loading trigger={loadingWithdrawal}>
                    <div></div>
                  </Loading>
                </center>
              ) : (
                <div>
                  <p>Input the request ID:</p>
                  <p>
                    <input
                      id="coffeeAmount"
                      name="coffeeAmount"
                      type={"number"}
                      placeholder="1"
                      onChange={onRequestIDChange3}
                    ></input>
                  </p>
                  <p>
                    <button type="submit" onClick={executeAWithdrawal}>
                      Execute Withdrawal
                    </button>
                  </p>
                </div>
              )}
            </div>
          </a>
        </div>
      </main>

      <footer>
        Feeling curious? Have a look through my{" "}
        <a
          className="github"
          target="_blank"
          href="https://github.com/Okiki-Olugunna"
        >
          GitHub
        </a>
      </footer>
    </div>
  );
}
