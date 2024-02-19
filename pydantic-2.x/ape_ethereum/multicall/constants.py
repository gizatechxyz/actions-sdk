from copy import deepcopy
from typing import cast

from ape.types import AddressType, HexBytes

SUPPORTED_CHAINS = [
    1,
    42,
    4,
    5,
    3,
    11155111,
    10,
    69,
    420,
    42161,
    421613,
    421611,
    137,
    80001,
    100,
    43114,
    43113,
    4002,
    250,
    56,
    97,
    1284,
    1285,
    1287,
    1666600000,
    25,
    122,
    14,
    19,
    16,
    114,
    288,
    1313161554,
    592,
    66,
    128,
    1088,
    30,
    31,
    9001,
    9000,
    108,
    18,
    42262,
    42220,
    44787,
    71402,
    71401,
    8217,
    2001,
    321,
    106,
    40,
]
MULTICALL3_ADDRESS = cast(AddressType, "0xcA11bde05977b3631167028862bE2a173976CA11")
MULTICALL3_CODE = HexBytes(
    "0x6080604052600436106100f35760003560e01c80634d2301cc1161008a578063a8b0574e11610059578063a8b0"
    "574e1461025a578063bce38bd714610275578063c3077fa914610288578063ee82ac5e1461029b57600080fd5b80"
    "634d2301cc146101ec57806372425d9d1461022157806382ad56cb1461023457806386d516e81461024757600080"
    "fd5b80633408e470116100c65780633408e47014610191578063399542e9146101a45780633e64a696146101c657"
    "806342cbb15c146101d957600080fd5b80630f28c97d146100f8578063174dea711461011a578063252dba421461"
    "013a57806327e86d6e1461015b575b600080fd5b34801561010457600080fd5b50425b6040519081526020015b60"
    "405180910390f35b61012d610128366004610a85565b6102ba565b6040516101119190610bbe565b61014d610148"
    "366004610a85565b6104ef565b604051610111929190610bd8565b34801561016757600080fd5b50437fffffffff"
    "ffffffffffffffffffffffffffffffffffffffffffffffffffffffff0140610107565b34801561019d57600080fd"
    "5b5046610107565b6101b76101b2366004610c60565b610690565b60405161011193929190610cba565b34801561"
    "01d257600080fd5b5048610107565b3480156101e557600080fd5b5043610107565b3480156101f857600080fd5b"
    "50610107610207366004610ce2565b73ffffffffffffffffffffffffffffffffffffffff163190565b3480156102"
    "2d57600080fd5b5044610107565b61012d610242366004610a85565b6106ab565b34801561025357600080fd5b50"
    "45610107565b34801561026657600080fd5b50604051418152602001610111565b61012d610283366004610c6056"
    "5b61085a565b6101b7610296366004610a85565b610a1a565b3480156102a757600080fd5b506101076102b63660"
    "04610d18565b4090565b60606000828067ffffffffffffffff8111156102d8576102d8610d31565b604051908082"
    "52806020026020018201604052801561031e57816020015b60408051808201909152600081526060602082015281"
    "52602001906001900390816102f65790505b5092503660005b828110156104775760008582815181106103415761"
    "0341610d60565b6020026020010151905087878381811061035d5761035d610d60565b905060200281019061036f"
    "9190610d8f565b6040810135958601959093506103886020850185610ce2565b73ffffffffffffffffffffffffff"
    "ffffffffffffff16816103ac6060870187610dcd565b6040516103ba929190610e32565b60006040518083038185"
    "875af1925050503d80600081146103f7576040519150601f19603f3d011682016040523d82523d6000602084013e"
    "6103fc565b606091505b50602080850191909152901515808452908501351761046d577f08c379a0000000000000"
    "00000000000000000000000000000000000000000000600052602060045260176024527f4d756c746963616c6c33"
    "3a2063616c6c206661696c656400000000000000000060445260846000fd5b5050600101610325565b5082341461"
    "04e6576040517f08c379a00000000000000000000000000000000000000000000000000000000081526020600482"
    "0152601a60248201527f4d756c746963616c6c333a2076616c7565206d69736d6174636800000000000060448201"
    "526064015b60405180910390fd5b50505092915050565b436060828067ffffffffffffffff81111561050c576105"
    "0c610d31565b60405190808252806020026020018201604052801561053f57816020015b60608152602001906001"
    "9003908161052a5790505b5091503660005b8281101561068657600087878381811061056257610562610d60565b"
    "90506020028101906105749190610e42565b92506105836020840184610ce2565b73ffffffffffffffffffffffff"
    "ffffffffffffffff166105a66020850185610dcd565b6040516105b4929190610e32565b60006040518083038160"
    "00865af19150503d80600081146105f1576040519150601f19603f3d011682016040523d82523d6000602084013e"
    "6105f6565b606091505b5086848151811061060957610609610d60565b602090810291909101015290508061067d"
    "576040517f08c379a000000000000000000000000000000000000000000000000000000000815260206004820152"
    "601760248201527f4d756c746963616c6c333a2063616c6c206661696c6564000000000000000000604482015260"
    "64016104dd565b50600101610546565b5050509250929050565b43804060606106a086868661085a565b90509350"
    "9350939050565b6060818067ffffffffffffffff8111156106c7576106c7610d31565b6040519080825280602002"
    "6020018201604052801561070d57816020015b604080518082019091526000815260606020820152815260200190"
    "6001900390816106e55790505b5091503660005b828110156104e657600084828151811061073057610730610d60"
    "565b6020026020010151905086868381811061074c5761074c610d60565b905060200281019061075e9190610e76"
    "565b925061076d6020840184610ce2565b73ffffffffffffffffffffffffffffffffffffffff1661079060408501"
    "85610dcd565b60405161079e929190610e32565b6000604051808303816000865af19150503d80600081146107db"
    "576040519150601f19603f3d011682016040523d82523d6000602084013e6107e0565b606091505b506020808401"
    "919091529015158083529084013517610851577f08c379a000000000000000000000000000000000000000000000"
    "000000000000600052602060045260176024527f4d756c746963616c6c333a2063616c6c206661696c6564000000"
    "00000000000060445260646000fd5b50600101610714565b6060818067ffffffffffffffff811115610876576108"
    "76610d31565b6040519080825280602002602001820160405280156108bc57816020015b60408051808201909152"
    "60008152606060208201528152602001906001900390816108945790505b5091503660005b82811015610a105760"
    "008482815181106108df576108df610d60565b602002602001015190508686838181106108fb576108fb610d6056"
    "5b905060200281019061090d9190610e42565b925061091c6020840184610ce2565b73ffffffffffffffffffffff"
    "ffffffffffffffffff1661093f6020850185610dcd565b60405161094d929190610e32565b600060405180830381"
    "6000865af19150503d806000811461098a576040519150601f19603f3d011682016040523d82523d600060208401"
    "3e61098f565b606091505b506020830152151581528715610a07578051610a07576040517f08c379a00000000000"
    "0000000000000000000000000000000000000000000000815260206004820152601760248201527f4d756c746963"
    "616c6c333a2063616c6c206661696c656400000000000000000060448201526064016104dd565b506001016108c3"
    "565b5050509392505050565b6000806060610a2b60018686610690565b919790965090945092505050565b600080"
    "83601f840112610a4b57600080fd5b50813567ffffffffffffffff811115610a6357600080fd5b60208301915083"
    "60208260051b8501011115610a7e57600080fd5b9250929050565b60008060208385031215610a9857600080fd5b"
    "823567ffffffffffffffff811115610aaf57600080fd5b610abb85828601610a39565b9096909550935050505056"
    "5b6000815180845260005b81811015610aed57602081850181015186830182015201610ad1565b81811115610aff"
    "576000602083870101525b50601f017fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    "ffe0169290920160200192915050565b600082825180855260208086019550808260051b84010181860160005b84"
    "811015610bb1578583037fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0018952"
    "81518051151584528401516040858501819052610b9d81860183610ac7565b9a86019a9450505090830190600101"
    "610b4f565b5090979650505050505050565b602081526000610bd16020830184610b32565b9392505050565b6000"
    "60408201848352602060408185015281855180845260608601915060608160051b870101935082870160005b8281"
    "1015610c52577fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa088870301845261"
    "0c40868351610ac7565b95509284019290840190600101610c06565b509398975050505050505050565b60008060"
    "0060408486031215610c7557600080fd5b83358015158114610c8557600080fd5b9250602084013567ffffffffff"
    "ffffff811115610ca157600080fd5b610cad86828701610a39565b9497909650939450505050565b838152826020"
    "820152606060408201526000610cd96060830184610b32565b95945050505050565b600060208284031215610cf4"
    "57600080fd5b813573ffffffffffffffffffffffffffffffffffffffff81168114610bd157600080fd5b60006020"
    "8284031215610d2a57600080fd5b5035919050565b7f4e487b710000000000000000000000000000000000000000"
    "0000000000000000600052604160045260246000fd5b7f4e487b7100000000000000000000000000000000000000"
    "000000000000000000600052603260045260246000fd5b600082357fffffffffffffffffffffffffffffffffffff"
    "ffffffffffffffffffffffffff81833603018112610dc357600080fd5b9190910192915050565b60008083357fff"
    "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe1843603018112610e0257600080fd5b"
    "83018035915067ffffffffffffffff821115610e1d57600080fd5b602001915036819003821315610a7e57600080"
    "fd5b8183823760009101908152919050565b600082357fffffffffffffffffffffffffffffffffffffffffffffff"
    "ffffffffffffffffc1833603018112610dc357600080fd5b600082357fffffffffffffffffffffffffffffffffff"
    "ffffffffffffffffffffffffffffa1833603018112610dc357600080fdfea2646970667358221220bb2b5c71a328"
    "032f97c676ae39a1ec2148d3e5d6f73d95e9b17910152d61f16264736f6c634300080c0033"
)

AGGREGATE3VALUE_METHOD = {
    "name": "aggregate3value",
    "type": "function",
    "stateMutability": "payable",
    "inputs": [
        {
            "name": "calls",
            "type": "tuple[]",
            "components": [
                {"name": "target", "type": "address"},
                {"name": "allowFailure", "type": "bool"},
                {"name": "value", "type": "uint256"},
                {"name": "callData", "type": "bytes"},
            ],
        }
    ],
    "outputs": [
        {
            "name": "returnData",
            "type": "tuple[]",
            "components": [
                {"name": "success", "type": "bool"},
                {"name": "returnData", "type": "bytes"},
            ],
        },
    ],
}

AGGREGATE3_METHOD = deepcopy(AGGREGATE3VALUE_METHOD)
AGGREGATE3_METHOD["name"] = "aggregate3"
AGGREGATE3_METHOD["inputs"][0]["components"].pop(2)  # type: ignore

AGGREGATE_METHOD = deepcopy(AGGREGATE3_METHOD)
AGGREGATE_METHOD["name"] = "aggregate"
AGGREGATE_METHOD["inputs"][0]["components"].pop(1)  # type: ignore
AGGREGATE_METHOD["outputs"] = [
    {"name": "blockNumber", "type": "uint256"},
    {"name": "returnData", "type": "bytes[]"},
]


MULTICALL3_CONTRACT_TYPE = {
    "contractName": "Multicall3",
    "abi": [AGGREGATE_METHOD, AGGREGATE3_METHOD, AGGREGATE3VALUE_METHOD],
}
