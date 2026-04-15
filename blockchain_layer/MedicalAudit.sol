// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MedicalAudit {
    address public admin;

    struct Report {
        string cid;
        string verdict;
        uint256 confidence;
        uint256 timestamp;
        address nodeAddress; 
    }
    Report[] public allReports;
    
    mapping(address => bool) public authorizedNodes;

    event ReportAdded(string cid, string verdict, uint256 confidence, uint256 timestamp, address indexed nodeAddress);
    event NodeAuthorized(address indexed nodeAddress);
    event NodeRevoked(address indexed nodeAddress);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    modifier onlyAuthorizedNode() {
        require(authorizedNodes[msg.sender], "Unauthorized Node");
        _;
    }

    constructor() {
        admin = msg.sender;
        authorizedNodes[msg.sender] = true; 
    }

    function authorizeNode(address _node) public onlyAdmin {
        authorizedNodes[_node] = true;
        emit NodeAuthorized(_node);
    }

    function revokeNode(address _node) public onlyAdmin {
        authorizedNodes[_node] = false;
        emit NodeRevoked(_node);
    }

    function addReport(string memory _cid, string memory _verdict, uint256 _confidence) public onlyAuthorizedNode {
        allReports.push(Report({
            cid: _cid,
            verdict: _verdict,
            confidence: _confidence,
            timestamp: block.timestamp,
            nodeAddress: msg.sender
        }));
        
        emit ReportAdded(_cid, _verdict, _confidence, block.timestamp, msg.sender);
    }

    function getAllReports() public view returns (Report[] memory) {
        return allReports;
    }
}