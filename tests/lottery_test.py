from email.policy import default
from math import e
import pytest
from collections.abc import Generator
from lottery import contract
from smart_contracts.lottery.contract import Lottery
from algopy_testing import AlgopyTestContext, algopy_testing_context
from _algopy_testing.context_helpers.txn_context import TransactionContext, DeferredAppCall
from algopy import (
    UInt64,
)

@pytest.fixture()
def context() -> Generator[AlgopyTestContext, None, None]:
    with algopy_testing_context() as ctx:
        yield ctx

def test_create_application(context:AlgopyTestContext)->None:
    contract = Lottery()
    entry_fee = context.any.uint64()
    default_sender = context.default_sender

    contract.create_application(entry_fee)

    assert contract.entry_fee == entry_fee
    assert contract.total_enteries == UInt64(0)
    assert contract.creator_address == default_sender

def test_enter_lottery(context:AlgopyTestContext)->None:
    contract = Lottery()
    entry_fee = UInt64(1_000_000)
    contract.create_application(entry_fee)


    test_app = context.ledger.get_app(contract)
    payment_txn = context.any.txn.payment(receiver=test_app.address,amount=entry_fee)


    contract.enter_lottery(payment_txn)
    assert contract.total_enteries == UInt64(1)
    assert payment_txn.receiver == test_app.address
    assert payment_txn.amount == entry_fee