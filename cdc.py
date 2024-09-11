import smartpy as sp

class AssuredContractedFarming(sp.Contract):
    def __init__(self):
        self.init(
            farmers = sp.map(tkey=sp.TAddress, tvalue=sp.TRecord(name=sp.TString, balance=sp.TMutez)),
            buyers = sp.map(tkey=sp.TAddress, tvalue=sp.TRecord(name=sp.TString, balance=sp.TMutez)),
            contracts = sp.big_map(tkey=sp.TNat, tvalue=sp.TRecord(
                farmer=sp.TAddress,
                buyer=sp.TAddress,
                goods=sp.TString,
                price=sp.TMutez,
                delivered=sp.TBool,
                paid=sp.TBool,
                disputed=sp.TBool
            )),
            contract_counter = 0
        )

    @sp.entry_point
    def register_farmer(self, params):
        sp.verify(~self.data.farmers.contains(params.address), "Farmer already registered")
        sp.verify(sp.pack(params.name).is_string(), "Name should be a string")
        sp.verify(sp.len(params.name) > 0, "Name should not be empty")
        self.data.farmers[params.address] = sp.record(name=params.name, balance=sp.mutez(0))

    @sp.entry_point
    
    def register_buyer(self, params):
        # Verify that the address is not already registered as a buyer.
        sp.verify(~self.data.buyers.contains(params.address), "Buyer already registered")

        # Verify that the name is a string.
        sp.verify(sp.pack(params.name).is_string(), "Name should be a string")

        # Verify that the name is not empty.
        sp.verify(sp.len(params.name) > 0, "Name should not be empty")

        # Register the buyer.
        self.data.buyers[params.address] = sp.record(name=params.name, balance=sp.mutez(0))
    @sp.entry_point
    def create_contract(self, params):
        sp.verify(self.data.farmers.contains(params.farmer), "Farmer not registered")
        sp.verify(self.data.buyers.contains(params.buyer), "Buyer not registered")
        self.data.contracts[self.data.contract_counter] = sp.record(
            farmer=params.farmer,
            buyer=params.buyer,
            goods=params.goods,
            price=params.price,
            delivered=False,
            paid=False,
            disputed=False
        )
        self.data.contract_counter += 1

    @sp.entry_point
    def deliver_goods(self, params):
        sp.verify(self.data.contracts.contains(params.contract_id), "Contract does not exist")
        contract = self.data.contracts[params.contract_id]
        sp.verify(sp.sender == contract.farmer, "Only farmer can mark as delivered")
        sp.verify(~contract.delivered, "Goods already delivered")
        contract.delivered = True
        self.data.contracts[params.contract_id] = contract

    @sp.entry_point
    def make_payment(self, params):
        sp.verify(self.data.contracts.contains(params.contract_id), "Contract does not exist")
        contract = self.data.contracts[params.contract_id]
        sp.verify(sp.sender == contract.buyer, "Only buyer can make payment")
        sp.verify(contract.delivered, "Goods not delivered yet")
        sp.verify(~contract.paid, "Payment already made")
        sp.verify(sp.amount == contract.price, "Incorrect payment amount")
        contract.paid = True
        self.data.farmers[contract.farmer].balance += sp.amount
        self.data.contracts[params.contract_id] = contract

    @sp.entry_point
    def raise_dispute(self, params):
        sp.verify(self.data.contracts.contains(params.contract_id), "Contract does not exist")
        contract = self.data.contracts[params.contract_id]
        sp.verify(sp.sender == contract.buyer, "Only buyer can raise dispute")
        sp.verify(contract.delivered, "Goods not delivered yet")
        sp.verify(~contract.disputed, "Dispute already raised")
        contract.disputed = True
        self.data.contracts[params.contract_id] = contract

    @sp.entry_point
    def resolve_dispute(self, params):
        sp.verify(self.data.contracts.contains(params.contract_id), "Contract does not exist")
        contract = self.data.contracts[params.contract_id]
        sp.verify(contract.disputed, "No dispute to resolve")
        sp.verify(sp.sender == contract.farmer or sp.sender == contract.buyer, "Only involved parties can resolve dispute")
        contract.disputed = False
        self.data.contracts[params.contract_id] = contract

@sp.add_test(name = "Assured Contracted Farming")
def test():
    scenario = sp.test_scenario()
    contract = AssuredContractedFarming()
    scenario += contract

    farmer = sp.test_account("Farmer")
    buyer = sp.test_account("Buyer")

    scenario += contract.register_farmer(address=farmer.address, name="Farmer John").run(sender=farmer)
    scenario += contract.register_buyer(address=buyer.address, name="Buyer Bob").run(sender=buyer)

    scenario += contract.create_contract(farmer=farmer.address, buyer=buyer.address, goods="Tomatoes", price=sp.mutez(1000)).run(sender=farmer)
    scenario += contract.deliver_goods(contract_id=0).run(sender=farmer)
    scenario += contract.make_payment(contract_id=0).run(sender=buyer, amount=sp.mutez(1000))
    scenario += contract.raise_dispute(contract_id=0).run(sender=buyer)
    scenario += contract.resolve_dispute(contract_id=0).run(sender=farmer)