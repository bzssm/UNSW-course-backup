pragma solidity ^0.4.18;

//deploy address: 0x2822ead52203bc821bf0157a778630187d0a9d86
/*
additional function:
set how many times a voter can vote: (one voter can vote several times.)
struct voter: uint time
function set_times(address,t): voter[address].time=t
function vote: require(voter[address].time>0)

*/


contract VotingSystem {
    // set Voter attribute: whether the voter is eligible for voting
    struct Voter { 
        bool eligible;
    }
    // set option attributes: option name and how many votes it has
    struct Option {
        string name;
        uint count; 
    }
    //set owner address
    address public owner=msg.sender;
    
    modifier onlyOwner {
        if(msg.sender!=owner) {
            throw;
        }
        _;
    }

    mapping(address => Voter) voters;

    Option[] options;
    // set quorum limit and current quorum
    uint public quorumLimit=0;
    uint public current=0;
    
    function setLimit(uint q) onlyOwner public{
        require(q>current);
        quorumLimit = q;
    }
    // add choice to option pool
    function addchoice(string option)  onlyOwner public {
        options.push(
            Option({
                name: option,
                count: 0
            })
        );
    }
    // add friend to voter pool
    function addVoter(address voter)  onlyOwner public {
        voters[voter].eligible = true;
    }
    // voting function, use option index to vote, not option name
    function vote(uint optionIndex) public {
        Voter storage sender = voters[msg.sender];
        require(sender.eligible); // validation
        require(current < quorumLimit); // validation
        sender.eligible = false;
        options[optionIndex].count += 1;
        current += 1;
    }
    // return a options string, seperated by ","
    function listAllOptions() public view returns(string){
        string memory res="";
        for (uint i = 0; i < options.length; i++) {
            res = strcat(res, options[i].name);
            if (i!=options.length-1){
                res = strcat(res,", ");
            }
        }
        return res;
    } 
    // get Final Result
    function getResult() public view returns (string){
        string memory winner = "";
        uint max = 0;
        for (uint i = 0; i < options.length; i++) {
            if (options[i].count > max) {
                max = options[i].count;
                winner =options[i].name;
            }
        }
        return winner;
    }
    // suicide, return funds to assigned address
    function destroy(address billTo) onlyOwner public{
        selfdestruct(billTo);
    }
    // help functions to connect two strings
    function strcat(string a, string b) internal pure returns (string){
        bytes memory bytea = bytes(a); 
        bytes memory byteb = bytes(b);
        bytes memory res = bytes(new string(bytea.length + byteb.length));
        uint k = 0;
        uint i = 0;
        for (i = 0; i < bytea.length; i++){
            res[k++] = bytea[i];
        }
        for (i = 0; i < byteb.length; i++){
            res[k++] = byteb[i];
        }
        return string(res);
    } 
}