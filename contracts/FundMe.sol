// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    //using SafeMathChainlink for uint256;

    mapping(address => uint256) public addresstovaluefunded;
    address public owner;
    address[] public funders;
    AggregatorV3Interface public priceFeeds;

    constructor(address _priceFeed) public {
        priceFeeds = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        uint256 minimumUSD = 50 * 10**18;
        require(
            getconversionrate(msg.value) >= minimumUSD,
            "okala shuke, spend this ETH"
        );
        addresstovaluefunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getversion() public view returns (uint256) {
        return priceFeeds.version();
    }

    function getprice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeeds.latestRoundData();
        return uint256(answer * 10000000000);
    }

    // Note that 1000000000 wei = i gwei
    function getconversionrate(uint256 ethamount)
        public
        view
        returns (uint256)
    {
        uint256 ethprice = getprice();
        uint256 ethamountinUSD = (ethprice * ethamount) / 1000000000000000000;
        return ethamountinUSD;
    }

    function getEntranceFee() public view returns (uint256) {
        //minimunUSD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getprice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
        for (
            uint256 fundersIndex = 0;
            fundersIndex < funders.length;
            fundersIndex++
        ) {
            address funder = funders[fundersIndex];
            addresstovaluefunded[funder] = 0;
        }
        funders = new address[](0);
    }
}
