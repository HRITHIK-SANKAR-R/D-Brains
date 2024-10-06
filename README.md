# Assured Contracted Farming

**Assured Contracted Farming** is a decentralized platform leveraging blockchain technology to enable direct trade between farmers and retailers/wholesalers without intermediaries. The platform uses smart contracts to automate payments, escrow, and delivery confirmation, providing transparency and fairness in the agricultural supply chain.

## Features

- **Direct Farmer-to-Retailer Trade**: Facilitates transactions without middlemen, benefiting both farmers and retailers.
- **Smart Contracts**: Automates payments and escrow using Tezos smart contracts written in SmartPy.
- **Escrow System**: Payments are securely held until the buyer confirms the delivery of goods.
- **Blockchain Transparency**: All transactions are recorded on the Tezos blockchain for transparency and accountability.
- **User-Friendly Interface**: Built using Next.js, providing an easy-to-use interface for managing transactions.

## Tech Stack

- **Smart Contracts**: SmartPy (Tezos blockchain)
- **Frontend**: Next.js
- **Blockchain Integration**: Taquito (JavaScript library for Tezos)
- **Wallet Integration**: Temple Wallet, Beacon Wallet

## Installation

### Prerequisites

- Node.js (v14+)
- Temple Wallet or Beacon Wallet (for interaction with the Tezos blockchain)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/HRITHIK-SANKAR-R/assured-contracted-farming.git
   cd assured-contracted-farming
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables (create a `.env` file in the root folder):
   ```bash
   NEXT_PUBLIC_TEZOS_RPC_URL=<Tezos RPC URL>
   NEXT_PUBLIC_CONTRACT_ADDRESS=<Smart Contract Address>
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open your browser and go to `http://localhost:3000` to view the app.

## Smart Contract Deployment

Smart contracts were developed using **SmartPy** and deployed on the Tezos blockchain.

### Smart Contract Deployment Steps

1. Write your contract in SmartPy and deploy using **SmartPy.io**.
2. Use the following template for contract interaction in Taquito:
   ```javascript
   const contract = await Tezos.wallet.at(contractAddress);
   const op = await contract.methods.someMethod(parameters).send();
   await op.confirmation();
   ```

3. Store the deployed contract address in your `.env` file for frontend interaction.

## How to Use

1. **Farmers** can register, list their products, and set prices.
2. **Retailers** can browse available products, place orders, and make payments.
3. Payments are held in escrow by the smart contract until delivery is confirmed by the buyer.
4. Upon confirmation, funds are released to the farmer, ensuring secure and transparent transactions.

## Challenges

- **Integrating Taquito with the Frontend**: Handling asynchronous transactions and ensuring compatibility with smart contracts.
- **Wallet Integration**: Ensuring smooth wallet connections and secure transaction signing.
- **Smart Contract Deployment**: Managing gas fees and optimizing the contract for smooth execution on Tezos.

## Accomplishments

- Successfully deployed smart contracts automating payments and escrow.
- Integrated Taquito for secure blockchain interactions with a user-friendly frontend.
- Achieved seamless wallet authentication using Temple Wallet.

## Future Improvements

- Add support for dispute resolution mechanisms.
- Implement more detailed product tracking and delivery mechanisms.
- Extend the platform for cross-border agricultural trade.

## Contributing

Feel free to submit issues, suggestions, or pull requests. Any contributions that improve the platform or enhance its scalability are welcome!

## License

This project is licensed under the **MIT License**.
