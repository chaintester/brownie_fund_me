from brownie import FundMe
from scripts.heplful_scripts import get_account

def fund():
    fund_me = FundMe[-1]    # uzima adresu posljednjeg ugovora iz '/build/deployments', iz tekuce networkID
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(entrance_fee)
    print(f"Trenutni entrance fee je: {entrance_fee} wei-ja (50 USD).")
    print("Finansiranje...")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()