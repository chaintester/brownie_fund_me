from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

# ovo su nam lokalna razvojna okruzenja, "ganache-local" je Ganache GUI koji smo dodali:
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 200000000000 # 2000 USD, format iz getPrice() funkcije

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:  # ako je ganache mreza
        return accounts[0]
    else:   # uzmi iz yaml config fajla
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    print(f"Aktivna mreza je: {network.show_active()}")
    print("Isporucujemo Mock ugovor...")
    if len(MockV3Aggregator) <= 0:  # ako vec nismo isporucili Mock
        MockV3Aggregator.deploy(DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()})

    # verzija bez ove petlje iznad:
    # mock_aggregator = MockV3Aggregator.deploy(18, Web3.toWei(2000, "ether"), {"from": account}) # vidi konstruktor
    # mock_aggregator = MockV3Aggregator.deploy(18, 2000000000000000000, {"from": account}) # ovo iznad ali duze
    # price_feed_address = mock_aggregator.address
    print("Mock-ovi su isporuceni!")



