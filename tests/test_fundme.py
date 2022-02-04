from brownie import FundMe, network, accounts, exceptions
from scripts.help_scripts import get_account, LOCAL_BLOCKCHAIN_ENV
from scripts.deploy import deploy_fundme
import pytest


def test_fund_and_withdraw():
    fundme = deploy_fundme()
    account = get_account()
    entrance_fee = fundme.getEntranceFee() + 100
    tx = fundme.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fundme.addresstovaluefunded(account.address) == entrance_fee
    tx2 = fundme.withdraw({"from": account})
    tx2.wait(1)
    assert fundme.addresstovaluefunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip("only for local testing")
    fundme = deploy_fundme()
    new_acc = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fundme.withdraw({"from": new_acc})
