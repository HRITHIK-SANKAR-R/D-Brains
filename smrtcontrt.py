import smartpy as sp

class Assuredcontract(sp.Contract):
    def __init__(self):
        self.init(
            fadrs=sp.address("tz1PguFJTj2ZPT9fCqAxt4BwbJtDP8XNAfJS"),
            cuadrs=sp.address("tz1Wo5j2PHYarqekwd7FimrZgS2Ps7oB2war"),
            goods=sp.map({
                "rice":500,
                "wheat":400,
                "onion":700,
                "brinjal":600,
                "rajma":1000,
                "bengal gram":500
            }),
            price = 0,
            cn=False
        )
    @sp.entry_point
    def buy(self,byls):
        sp.verify(sp.sender == self.data.fadrs,"Only customer can buy!")
        price=0
        for i in byls:
            price+=self.data.goods[i]
        self.data.price = price
        self.deliver(price)
    @sp.entry_point
    def sendm(self,price,byls):
        if(sp.data.cn):
            sp.send(self.data.fardrs,price)
    @sp.entry_point
    def deliver(self,pr):
        if(pr>0):
            self.confrim_payment()
            self.sendm(self.data.price,self.data.fadrs)
            price=0
            self.data.price = 0 
        else:
            sp.error("Not enough money")
    @sp.entry_point
    def confrim_payment(self):
        sp.data.cn=True

@sp.add_test(name="Assured Contract")
def test():
    sen=sp.test_scenario("My 1st Assured Contract")
    con=Assuredcontract()
    senario+=con

    con.buy(["rice","wheat"])

   




    



