import smartpy as sp

class AssuredContractFarmingPlatform(sp.Contract):
    def __init__(self, admin):
        self.init(
            farmers = sp.big_map(tkey=sp.TAddress, tvalue=sp.TRecord(name=sp.TString, balance=sp.TMutez)),
            buyers = sp.big_map(tkey=sp.TAddress, tvalue=sp.TRecord(name=sp.TString, balance=sp.TMutez)),
            products = sp.big_map(tkey=sp.TString, tvalue=sp.TRecord(
                farmer=sp.TAddress,
                quantity=sp.TNat,
                price=sp.TMutez,
                bids=sp.big_map(tkey=sp.TAddress, tvalue=sp.TRecord(bid=sp.TMutez))
            )),
            contracts = sp.big_map(tkey=sp.TNat, tvalue=sp.TRecord(
                farmer=sp.TAddress,
                buyer=sp.TAddress,
                product=sp.TString,
                quantity=sp.TNat,
                price=sp.TMutez,
                status=sp.TString
            )),
            next_contract_id=sp.nat(0),
            daily_price = sp.big_map(tkey=sp.TString, tvalue=sp.TMutez),  # Prices from Oracles
            queries = sp.big_map(tkey=sp.TNat, tvalue=sp.TRecord(
                query_text=sp.TString,
                status=sp.TString,
                raised_by=sp.TAddress,
                resolved_by=sp.TAddress
            )),
            next_query_id=sp.nat(0),
            admin=admin
        )

    @sp.entry_point
    def register_farmer(self, name):
        sp.verify(sp.sender not in self.data.farmers, "Farmer already registered")
        self.data.farmers[sp.sender] = sp.record(name=name, balance=sp.mutez(0))

    @sp.entry_point
    def register_buyer(self, name):
        sp.verify(sp.sender not in self.data.buyers, "Buyer already registered")
        self.data.buyers[sp.sender] = sp.record(name=name, balance=sp.mutez(0))

    @sp.entry_point
    def add_product(self, product_name, quantity, price):
        sp.verify(sp.sender in self.data.farmers, "Only farmers can add products")
        sp.verify(~self.data.products.contains(product_name), "Product already exists")
        self.data.products[product_name] = sp.record(
            farmer=sp.sender,
            quantity=quantity,
            price=price,
            bids=sp.big_map()
        )

    @sp.entry_point
    def update_product(self, product_name, quantity):
        sp.verify(sp.sender in self.data.farmers, "Only farmers can update products")
        sp.verify(self.data.products.contains(product_name), "Product not found")
        product = self.data.products[product_name]
        sp.verify(sp.sender == product.farmer, "Not authorized to update this product")
        self.data.products[product_name].quantity = quantity

    @sp.entry_point
    def place_bid(self, product_name, bid_amount):
        sp.verify(sp.sender in self.data.buyers, "Only buyers can place bids")
        sp.verify(self.data.products.contains(product_name), "Product not found")
        product = self.data.products[product_name]
        sp.verify(product.quantity > 0, "Product quantity is zero")
        product.bids[sp.sender] = sp.record(bid=bid_amount)

    @sp.entry_point
    def finalize_bid(self, product_name):
        sp.verify(sp.sender in self.data.farmers, "Only farmers can finalize bids")
        sp.verify(self.data.products.contains(product_name), "Product not found")
        product = self.data.products[product_name]
        sp.verify(sp.sender == product.farmer, "Not authorized to finalize this product")

        highest_bidder = sp.local("highest_bidder", sp.none)
        highest_bid = sp.local("highest_bid", sp.mutez(0))

        for bidder, bid_info in product.bids.items():
            sp.if bid_info.bid > highest_bid.value:
                highest_bid.value = bid_info.bid
                highest_bidder.value = sp.some(bidder)

        sp.verify(highest_bidder.value.is_some(), "No bids available")
        buyer = highest_bidder.value.open_some()

        self.data.contracts[self.data.next_contract_id] = sp.record(
            farmer=product.farmer,
            buyer=buyer,
            product=product_name,
            quantity=product.quantity,
            price=highest_bid.value,
            status="Pending"
        )
        self.data.next_contract_id += 1

    @sp.entry_point
    def confirm_contract(self, contract_id, percentage_received):
        sp.verify(sp.sender in self.data.buyers, "Only buyers can confirm contract")
        sp.verify(self.data.contracts.contains(contract_id), "Contract not found")
        contract = self.data.contracts[contract_id]
        sp.verify(sp.sender == contract.buyer, "Not authorized to confirm this contract")
        sp.verify(contract.status == "Pending", "Contract already processed")

        total_amount = contract.price
        amount_to_pay = sp.mutez(int(total_amount * percentage_received / 100))
        amount_to_return = total_amount - amount_to_pay
        
        sp.verify(self.data.buyers[sp.sender].balance >= total_amount, "Insufficient funds")
        sp.verify(amount_to_pay > sp.mutez(0), "Invalid payment amount")

        # Perform transfers
        sp.send(sp.sender, amount_to_return)
        sp.send(contract.farmer, amount_to_pay)
        
        self.data.contracts[contract_id].status = "Completed"
        self.data.buyers[sp.sender].balance -= total_amount
        self.data.farmers[contract.farmer].balance += amount_to_pay

    @sp.entry_point
    def update_oracle_price(self, product_name, price):
        sp.verify(sp.sender == self.data.admin, "Only admin can update prices")
        sp.verify(price > sp.mutez(0), "Price must be positive")
        self.data.daily_price[product_name] = price

    @sp.entry_point
    def raise_query(self, query_text):
        sp.verify(sp.sender in self.data.farmers or sp.sender in self.data.buyers, "Only registered users can raise queries")
        query_id = self.data.next_query_id
        self.data.queries[query_id] = sp.record(
            query_text=query_text,
            status="Pending",
            raised_by=sp.sender,
            resolved_by=sp.none
        )
        self.data.next_query_id += 1

    @sp.entry_point
    def resolve_query(self, query_id):
        sp.verify(sp.sender == self.data.admin, "Only admin can resolve queries")
        sp.verify(self.data.queries.contains(query_id), "Query not found")
        query = self.data.queries[query_id]
        sp.verify(query.status == "Pending", "Query already resolved")
        self.data.queries[query_id].status = "Resolved"
        self.data.queries[query_id].resolved_by = sp.some(sp.sender)

    @sp.entry_point
    def update_balance(self):
        sp.verify(sp.sender in self.data.buyers or sp.sender in self.data.farmers, "Only registered users can update balance")

    @sp.entry_point
    def update_address(self, new_address):
        sp.verify(sp.sender in self.data.buyers or sp.sender in self.data.farmers, "Only registered users can update address")
        sp.verify(self.data.valid_addresses.contains(new_address), "New address is not valid")
        if sp.sender in self.data.buyers:
            self.data.buyers[sp.sender].address = new_address
        else:
            self.data.farmers[sp.sender].address = new_address

# To deploy this contract
@sp.add_test(name = "AssuredContractFarmingPlatform")
def test():
    scenario = sp.test_scenario()
    scenario.h1("Assured Contract Farming Platform")
    
    admin = sp.address("tz1-admin")
    contract = AssuredContractFarmingPlatform(admin)
    scenario += contract

    # Admin actions
    scenario += contract.update_oracle_price("wheat", sp.mutez(1000)).run(sender=admin)

    # Farmer registration
    farmer = sp.address("tz1-farmer")
    scenario += contract.register_farmer("Farmer Joe").run(sender=farmer)

    # Buyer registration
    buyer = sp.address("tz1-buyer")
    scenario += contract.register_buyer("Buyer Bob").run(sender=buyer)

    # Add and update products
    scenario += contract.add_product("wheat", 100, sp.mutez(1500)).run(sender=farmer)
    scenario += contract.update_product("wheat", 80).run(sender=farmer)

    # Place and finalize bids
    scenario += contract.place_bid("wheat", sp.mutez(1600)).run(sender=buyer)
    scenario += contract.finalize_bid("wheat").run(sender=farmer)

    # Confirm contract
    scenario += contract.confirm_contract(0, 90).run(sender=buyer)

    # Raise and resolve query
    scenario += contract.raise_query("Query about wheat pricing").run(sender=buyer)
    scenario += contract.resolve_query(0).run(sender=admin)
