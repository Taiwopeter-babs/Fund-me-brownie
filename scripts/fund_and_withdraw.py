from webbrowser import get
from brownie import FundMe
from scripts.help_scripts import get_account


def fund():
    fundme = FundMe[-1]
    account = get_account()
    entrance_fee = fundme.getEntranceFee()
    print(f"The current entry fee is: {entrance_fee}\n Funding...")
    fundme.fund({"from": account, "value": entrance_fee})
    print("The account has been Funded")


def withdraw():
    fundme = FundMe[-1]
    account = get_account()
    print(f"withdrawing from {account}")
    fundme.withdraw({"from": account})
    print("Withdraw successful")


def main():
    fund()
    withdraw()
