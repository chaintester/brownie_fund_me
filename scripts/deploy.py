from brownie import FundMe, MockV3Aggregator, network, config
from scripts.heplful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS

def deploy_fund_me():
    account = get_account()
    # ako smo na lokalnoj Ganache mrezi treba nam mocking za priceFeed
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:  # ako nije Ganache ili GUI
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address  # daj posljednji isporuceni Mock

    fund_me = FundMe.deploy(
        price_feed_address, {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify")    #za slucaj da ["verify"] ne postoji u conf
    )

    # verzija sa priceFeed-om u konstruktoru za perzistentnu mrezu kao sto je Rinkeby:
    #fund_me = FundMe.deploy("0x8A753747A1Fa494EC906cE90E9f37563A8AF630e", {"from": account}, publish_source=True)
    # verzija sa hard kodovanim priceFeed-om:
    #fund_me = FundMe.deploy({"from":account}, publish_source=True)  # hocemo da objavimo nas izvorni kod
    print(f"Ugovor je isporucen na {fund_me.address}")
    return fund_me

def main():
    deploy_fund_me()