from scripts.heplful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    print(f"Entrance fee je: {entrance_fee}")
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Samo za lokalno testiranje!")
        fund_me = deploy_fund_me()
        bad_actor = accounts.add()  # dodajemo neki novi account
        #fund_me.withdraw({"from": bad_actor})  # iskocice greska 'VirtualMachineError'

        # ako se ovaj izvrsi sa greskom 'VirtualMachineError' test je dobar, odnosno proce
        with pytest.raises(exceptions.VirtualMachineError):
            fund_me.withdraw({"from": bad_actor})