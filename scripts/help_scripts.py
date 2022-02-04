from brownie import FundMe, accounts, config, network, MockV3Aggregator
from web3 import Web3

Decimals = 8
Starting_price = 200000000000
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]
FORKED_BLOCKCHAIN_ENV = ["mainnet-fork", "mainnet-fork-dev"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORKED_BLOCKCHAIN_ENV
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")

    # if the num of Mock contracts is < 0, deploy.
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(Decimals, Starting_price, {"from": get_account()})
    print("Mocks deployed")
