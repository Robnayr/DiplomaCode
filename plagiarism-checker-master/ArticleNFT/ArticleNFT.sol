// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import "Ownable.sol";
import "ERC721URIStorage.sol";
import "base64.sol";

contract ArticleNFT is ERC721URIStorage, Ownable {
    uint256 public tokenCounter;
    event CreatedSVGNFT(uint256 indexed tokenId, string tokenURI);

    constructor() ERC721("Article NFT", "artNFT")
    {
        tokenCounter = 0;
    }

    function create(string memory _metadata) public {
        _safeMint(msg.sender, tokenCounter);
        _setTokenURI(tokenCounter, _metadata);
        tokenCounter = tokenCounter + 1;
        emit CreatedSVGNFT(tokenCounter, _metadata);
    }
}