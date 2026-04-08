// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MedicalAudit {
    address public owner;

    struct ScanReport {
        string ipfsHash;
        string verdict;    
        uint256 confidence; 
        uint256 timestamp;
    }

    mapping(string => ScanReport) public reports;
    string[] public allHashes;  
    event ReportAdded(string ipfsHash, string verdict, uint256 timestamp);
    constructor() {
        owner = msg.sender; 
    }
    modifier onlyOwner() {
        require(msg.sender == owner, "Unauthorized: Only the hospital server can add reports");
        _;
    }

    function addReport(string memory _hash, string memory _verdict, uint256 _conf) public onlyOwner {
        require(reports[_hash].timestamp == 0, "Report already exists for this scan");

        reports[_hash] = ScanReport(_hash, _verdict, _conf, block.timestamp);
        allHashes.push(_hash); 

        emit ReportAdded(_hash, _verdict, block.timestamp);
    }

    function getAllReports() public view returns (ScanReport[] memory) {
        ScanReport[] memory allData = new ScanReport[](allHashes.length);
        for (uint i = 0; i < allHashes.length; i++) {
            allData[i] = reports[allHashes[i]];
        }
        return allData;
    }
}