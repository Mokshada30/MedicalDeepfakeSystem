// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MedicalAudit {
    address public admin;

    struct ScanReport {
        string ipfsHash;
        string verdict;    
        uint256 confidence; 
        uint256 timestamp;
    }

    mapping(string => ScanReport) public reports;
    string[] public allHashes;
    mapping(address => bool) public authorizedHospitals;
    
    event ReportAdded(string ipfsHash, string verdict, uint256 timestamp);
    
    constructor() {
        admin = msg.sender; 
        authorizedHospitals[msg.sender] = true; 
    }
    
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only Admin can authorize new hospitals");
        _;
    }

    modifier onlyAuthorized() {
        require(authorizedHospitals[msg.sender] == true, "Unauthorized: Not a verified clinical node");
        _;
    }

    function authorizeHospital(address _hospitalAddress) public onlyAdmin {
        authorizedHospitals[_hospitalAddress] = true;
    }

    function addReport(string memory _hash, string memory _verdict, uint256 _conf) public onlyAuthorized {
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