from algopy import (
    Global,
    Txn,
    UInt64,
    arc4,
    gtxn,
    itxn,
    Account,
    ARC4Contract,
)
#from httpx import delete
class Lottery(ARC4Contract):
    

    entry_fee:UInt64

    total_enteries:UInt64

    creator_address:Account


    @arc4.abimethod(create="require")
    def create_application(self,entry_fee:UInt64)->None:

        self.entry_fee = entry_fee
        self.total_enteries = UInt64(0)
        self.creator_address = Global.creator_address
    
    @arc4.abimethod
    def enter_lottery(self,payment_txn:gtxn.PaymentTransaction)->None:

        assert payment_txn.receiver == Global.current_application_address
        assert payment_txn.amount == self.entry_fee
        self.total_enteries+=UInt64(1)

    @arc4.abimethod
    def pick_winner(self)->None:
        assert Txn.sender == self.creator_address
        assert self.total_enteries > UInt64(0)

        round_number = Global.round
        random_number = round_number % self.total_enteries

        winner_address = gtxn.Transaction(random_number).sender

        itxn.Payment(
            amount = Global.current_application_address.balance - UInt64(1_000_000),
            receiver = winner_address,
            fee = 1000
        ).submit()

    @arc4.abimethod(allow_actions=["DeleteApplication"])
    def delete_application(self)->None:
        assert Txn.sender == self.creator_address
        itxn.Payment(
            receiver=self.creator_address,
            amount=0,
            close_remainder_to=self.creator_address,
            fee=1000
        ).submit()
        

