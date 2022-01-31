// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256; // sluzi za overflow provjeru cijelih brojeva, ne treba za solidity >= 0.8

    mapping(address => uint256) public addressToAmountFunded;   // mapiranje key=>value
    address[] public funders;   // array adresa ljudi koji finansiraju
    address public owner;
    AggregatorV3Interface public priceFeed;

    // konstruktor ce se izvrsiti kad se ugovor napravi prvi put
    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        // hard kodovani priceFeed - nece raditi sa Ganacheom
        //priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e); // Chainlink ETH/USD feed za Rinkeby
        owner = msg.sender; // onaj ko je isporucio ugovor (transakcijom)
    }
    /*
    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }
    */

    // funkcija za uplatu. payable znaci da sender salje eth primaocu pomocu transakcije
    function fund() public payable {
        uint256 minimumUSD = 50 * 10**18;   // 1 eth = 10**18 wei = 10**9 gwei
        require(getConversionRate(msg.value) >= minimumUSD, "You need to spend more ETH!");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    // funkcija za dobijanje verzije chainlink price feeda
    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    // funkcija koja vraca cijenu ETH u USD
    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();  // answer vraca 8-cifreni broj ako je eth bar 1000 USD
        return uint256(answer * 10000000000);   // prebaci u wei
    }

    // 1000000000
    function getConversionRate(uint256 ethAmount) public view returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    // modifajer mijenja ponasanje funkcije za koju je vezan
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;  // ovaj znak znaci ubaci tijelo funkcije ovdje (merge wildcard)
    }

    function withdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);
        // posalji sve sa adrese this instance ugovora na adresu posaljioca transakcije. Ugovor moze imati vise instanci,
        // tj. mozemo ga deploy vise puta, svaki pur ce imati drugu adresu

        // postavi vrijednosti koje su ljudi donirali na 0
        for (uint256 funderIndex = 0; funderIndex < funders.length; funderIndex++) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0); // novi prazni array adresa velicine (0)
    }
}