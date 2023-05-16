/**
 *Submitted for verification at BscScan.com on 2023-05-01
*/

// SPDX-License-Identifier: MIT

pragma solidity ^0.8.15;

contract Storage {

    modifier onlyAdmin() {
        require(isAdmin(msg.sender), "Storage:: Only the contract admins can call this function");
        _;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Storage:: Only owner of the contract can call this function");
        _;
    }

    event addedAdmin (uint256 indexed addingTimestamp, address indexed newAdmin);
    event removedAdmin (uint256 indexed removingTimestamp, address indexed removedAdmin);
    event addedGoods (uint256 indexed addingTimestamp, string indexed description);

    constructor() {
        owner = msg.sender;
    }

    struct Goods {
        uint256 createTime;
        uint256 weight;
        uint256 height;
        string description;
        string creatorName;
    }

    address public owner;
    address[] public admins;

    mapping(uint256 => Goods) public goodsById;

    function getGoods(uint256 _id) public view returns (uint256, uint256, uint256, string memory, string memory) {
        Goods memory goods = goodsById[_id];
        return (goods.createTime, goods.weight, goods.height, goods.description, goods.creatorName);
    }

    function addAdmin(address _newAdmin) external onlyOwner {
        admins.push(_newAdmin);
        emit addedAdmin(block.timestamp, _newAdmin);
    }

    function removeAdmin(address _oldAdmin) external onlyOwner {
        for(uint256 i; i < admins.length; ++i) {
            if(admins[i] == _oldAdmin) {
                admins[i] = admins[(admins.length) -1];
                admins.pop;
            }
        }
        emit removedAdmin(block.timestamp, _oldAdmin);
    }

    function addGoods(uint256 _id, uint256 _createTime, uint256 _weight, uint256 _height, string memory _description, string memory _creatorName) external onlyAdmin{
        goodsById[_id] = Goods(_createTime, _weight, _height, _description, _creatorName);
        emit addedGoods(block.timestamp, _description);
    }

    function isAdmin(address _admin) internal view returns(bool) {
        for(uint256 i; i < admins.length; ++i) {
            if(admins[i] == _admin)
                return true;
        }
        return false;
    }
}

// address = 0x6A51720f6BEAE6D08Ff2a0a25459Ed9E157E61ad