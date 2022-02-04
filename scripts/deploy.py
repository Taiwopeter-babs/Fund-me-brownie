from decimal import Decimal
from brownie import FundMe, MockV3Aggregator, accounts, config, network
from scripts.help_scripts import deploy_mocks, get_account, LOCAL_BLOCKCHAIN_ENV


def deploy_fundme():
    # pass the price feed address to FundMe contract (//check FundMe.deploy())
    # if the network is persistent e.g rinkeby, use associated address,
    # else, deploy mocks(create mock solidity contract(contract-> new test folder->MockAggregatorV3.sol))
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_pricefeed"
        ]
    else:
        # if the num of Mock contracts is < 0, deploy, & use the most recent contract deployed
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    # The verify key works like the publish_source=True/False(see config file)
    fundme = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"Contract deployed to {fundme.address}")
    return fundme


def main():
    deploy_fundme()
