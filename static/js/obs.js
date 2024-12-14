let streamerAddress;
let newStreamerAddress;
let name;
let currBlockBase;
let currBlockEthereum;
let currBlockPolygon;
let currBlockAleph;
let currBlockOptimism;
let currBlockMantle;
let tippingBase;
let tippingEthereum;
let tippingPolygon;
let tippingAleph;
let tippingOptimism;
let tippingMantle;
let txnHashes = new Array();
let resTip = new Array();

async function resolveENS(identifier, web3) {
    console.log("resolving ens", identifier);
    try {
        if (web3.utils.isAddress(identifier)) {
            const response = await fetch(
                `https://api.idriss.xyz/v1/ENS-Addresses?identifer=${identifier}`
            );
            const ensData = await response.json();
            return {address: identifier, ens: ensData.name};
        } else {
            const resolvedAddress = await web3.eth.ens.getAddress(identifier);
            console.log(resolvedAddress);
            return {address: resolvedAddress, ens: identifier};
        }
    } catch (error) {
        return {};
    }
}

document.addEventListener("DOMContentLoaded", async function () {
    const urlParams = new URLSearchParams(window.location.search);
    streamerAddress = urlParams.get("streamerAddress");
    newStreamerAddress = urlParams.get("address");
    if (newStreamerAddress) streamerAddress = newStreamerAddress;
    if (!web3Ethereum.utils.isAddress(streamerAddress))
        streamerAddress = (await resolveENS(streamerAddress, web3Ethereum))
            .address;

    setupWebSocket();
});

let abiTippingOG = [
    {
        inputs: [
            {
                internalType: "address",
                name: "_maticUsdAggregator",
                type: "address",
            },
        ],
        stateMutability: "nonpayable",
        type: "constructor",
    },
    {
        inputs: [{internalType: "bytes", name: "innerError", type: "bytes"}],
        name: "BatchError",
        type: "error",
    },
    {
        inputs: [],
        name: "tipping__withdraw__OnlyAdminCanWithdraw",
        type: "error",
    },
    {
        anonymous: false,
        inputs: [
            {
                indexed: true,
                internalType: "address",
                name: "previousOwner",
                type: "address",
            },
            {
                indexed: true,
                internalType: "address",
                name: "newOwner",
                type: "address",
            },
        ],
        name: "OwnershipTransferred",
        type: "event",
    },
    {
        anonymous: false,
        inputs: [
            {
                indexed: true,
                internalType: "address",
                name: "recipientAddress",
                type: "address",
            },
            {
                indexed: false,
                internalType: "string",
                name: "message",
                type: "string",
            },
            {
                indexed: true,
                internalType: "address",
                name: "sender",
                type: "address",
            },
            {
                indexed: true,
                internalType: "address",
                name: "tokenAddress",
                type: "address",
            },
        ],
        name: "TipMessage",
        type: "event",
    },
    {
        inputs: [],
        name: "MINIMAL_PAYMENT_FEE",
        outputs: [{internalType: "uint256", name: "", type: "uint256"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [],
        name: "MINIMAL_PAYMENT_FEE_DENOMINATOR",
        outputs: [{internalType: "uint256", name: "", type: "uint256"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [],
        name: "PAYMENT_FEE_PERCENTAGE",
        outputs: [{internalType: "uint256", name: "", type: "uint256"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [],
        name: "PAYMENT_FEE_PERCENTAGE_DENOMINATOR",
        outputs: [{internalType: "uint256", name: "", type: "uint256"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [],
        name: "PAYMENT_FEE_SLIPPAGE_PERCENT",
        outputs: [{internalType: "uint256", name: "", type: "uint256"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {internalType: "address", name: "_adminAddress", type: "address"},
        ],
        name: "addAdmin",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [{internalType: "address", name: "", type: "address"}],
        name: "admins",
        outputs: [{internalType: "bool", name: "", type: "bool"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [{internalType: "address", name: "", type: "address"}],
        name: "balanceOf",
        outputs: [{internalType: "uint256", name: "", type: "uint256"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [{internalType: "bytes[]", name: "_calls", type: "bytes[]"}],
        name: "batch",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint256",
                name: "_minimalPaymentFee",
                type: "uint256",
            },
            {
                internalType: "uint256",
                name: "_paymentFeeDenominator",
                type: "uint256",
            },
        ],
        name: "changeMinimalPaymentFee",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint256",
                name: "_paymentFeePercentage",
                type: "uint256",
            },
            {
                internalType: "uint256",
                name: "_paymentFeeDenominator",
                type: "uint256",
            },
        ],
        name: "changePaymentFeePercentage",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [],
        name: "contractOwner",
        outputs: [{internalType: "address", name: "", type: "address"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {internalType: "address", name: "_adminAddress", type: "address"},
        ],
        name: "deleteAdmin",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [
            {internalType: "uint256", name: "_value", type: "uint256"},
            {internalType: "enum AssetType", name: "_assetType", type: "uint8"},
        ],
        name: "getPaymentFee",
        outputs: [{internalType: "uint256", name: "", type: "uint256"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [],
        name: "owner",
        outputs: [{internalType: "address", name: "", type: "address"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [],
        name: "renounceOwnership",
        outputs: [],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {internalType: "address", name: "_recipient", type: "address"},
            {internalType: "uint256", name: "_assetId", type: "uint256"},
            {internalType: "uint256", name: "_amount", type: "uint256"},
            {
                internalType: "address",
                name: "_assetContractAddress",
                type: "address",
            },
            {internalType: "string", name: "_message", type: "string"},
        ],
        name: "sendERC1155To",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {internalType: "address", name: "_recipient", type: "address"},
            {internalType: "uint256", name: "_tokenId", type: "uint256"},
            {
                internalType: "address",
                name: "_nftContractAddress",
                type: "address",
            },
            {internalType: "string", name: "_message", type: "string"},
        ],
        name: "sendERC721To",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {internalType: "address", name: "_recipient", type: "address"},
            {internalType: "uint256", name: "", type: "uint256"},
            {internalType: "string", name: "_message", type: "string"},
        ],
        name: "sendTo",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {internalType: "address", name: "_recipient", type: "address"},
            {internalType: "uint256", name: "_amount", type: "uint256"},
            {
                internalType: "address",
                name: "_tokenContractAddr",
                type: "address",
            },
            {internalType: "string", name: "_message", type: "string"},
        ],
        name: "sendTokenTo",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [{internalType: "bytes4", name: "interfaceId", type: "bytes4"}],
        name: "supportsInterface",
        outputs: [{internalType: "bool", name: "", type: "bool"}],
        stateMutability: "pure",
        type: "function",
    },
    {
        inputs: [{internalType: "address", name: "newOwner", type: "address"}],
        name: "transferOwnership",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [],
        name: "withdraw",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [
            {internalType: "address", name: "_tokenContract", type: "address"},
        ],
        name: "withdrawToken",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
];
let abiTippingBase = [
    {
        inputs: [
            {
                internalType: "address",
                name: "_nativeUsdAggregator",
                type: "address",
            },
            {internalType: "address", name: "_eas", type: "address"},
        ],
        stateMutability: "nonpayable",
        type: "constructor",
    },
    {
        inputs: [{internalType: "bytes", name: "innerError", type: "bytes"}],
        name: "BatchError",
        type: "error",
    },
    {inputs: [], name: "InvalidEAS", type: "error"},
    {
        inputs: [],
        name: "tipping__withdraw__OnlyAdminCanWithdraw",
        type: "error",
    },
    {inputs: [], name: "unknown_function_selector", type: "error"},
    {
        anonymous: false,
        inputs: [
            {
                indexed: true,
                internalType: "address",
                name: "previousOwner",
                type: "address",
            },
            {
                indexed: true,
                internalType: "address",
                name: "newOwner",
                type: "address",
            },
        ],
        name: "OwnershipTransferred",
        type: "event",
    },
    {
        anonymous: false,
        inputs: [
            {
                indexed: true,
                internalType: "address",
                name: "recipientAddress",
                type: "address",
            },
            {
                indexed: false,
                internalType: "string",
                name: "message",
                type: "string",
            },
            {
                indexed: true,
                internalType: "address",
                name: "sender",
                type: "address",
            },
            {
                indexed: true,
                internalType: "address",
                name: "tokenAddress",
                type: "address",
            },
            {
                indexed: false,
                internalType: "uint256",
                name: "amount",
                type: "uint256",
            },
            {
                indexed: false,
                internalType: "uint256",
                name: "fee",
                type: "uint256",
            },
        ],
        name: "TipMessage",
        type: "event",
    },
    {
        inputs: [],
        name: "MINIMAL_PAYMENT_FEE",
        outputs: [{internalType: "uint256", name: "", type: "uint256"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [],
        name: "MINIMAL_PAYMENT_FEE_DENOMINATOR",
        outputs: [{internalType: "uint256", name: "", type: "uint256"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [],
        name: "PAYMENT_FEE_PERCENTAGE",
        outputs: [{internalType: "uint256", name: "", type: "uint256"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [],
        name: "PAYMENT_FEE_PERCENTAGE_DENOMINATOR",
        outputs: [{internalType: "uint256", name: "", type: "uint256"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [],
        name: "PAYMENT_FEE_SLIPPAGE_PERCENT",
        outputs: [{internalType: "uint256", name: "", type: "uint256"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {internalType: "address", name: "_adminAddress", type: "address"},
        ],
        name: "addAdmin",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "address",
                name: "publicGoodAddress",
                type: "address",
            },
        ],
        name: "addPublicGood",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [{internalType: "address", name: "", type: "address"}],
        name: "admins",
        outputs: [{internalType: "bool", name: "", type: "bool"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [{internalType: "bytes[]", name: "_calls", type: "bytes[]"}],
        name: "batch",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint256",
                name: "_minimalPaymentFee",
                type: "uint256",
            },
            {
                internalType: "uint256",
                name: "_paymentFeeDenominator",
                type: "uint256",
            },
        ],
        name: "changeMinimalPaymentFee",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint256",
                name: "_paymentFeePercentage",
                type: "uint256",
            },
            {
                internalType: "uint256",
                name: "_paymentFeeDenominator",
                type: "uint256",
            },
        ],
        name: "changePaymentFeePercentage",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [
            {internalType: "address", name: "_adminAddress", type: "address"},
        ],
        name: "deleteAdmin",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "address",
                name: "publicGoodAddress",
                type: "address",
            },
        ],
        name: "deletePublicGood",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [
            {internalType: "uint256", name: "_value", type: "uint256"},
            {internalType: "enum AssetType", name: "_assetType", type: "uint8"},
        ],
        name: "getPaymentFee",
        outputs: [{internalType: "uint256", name: "", type: "uint256"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [],
        name: "owner",
        outputs: [{internalType: "address", name: "", type: "address"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [{internalType: "address", name: "", type: "address"}],
        name: "publicGoods",
        outputs: [{internalType: "bool", name: "", type: "bool"}],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [],
        name: "renounceOwnership",
        outputs: [],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {internalType: "address", name: "_recipient", type: "address"},
            {internalType: "uint256", name: "_assetId", type: "uint256"},
            {internalType: "uint256", name: "_amount", type: "uint256"},
            {
                internalType: "address",
                name: "_assetContractAddress",
                type: "address",
            },
            {internalType: "string", name: "_message", type: "string"},
        ],
        name: "sendERC1155To",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {internalType: "address", name: "_recipient", type: "address"},
            {internalType: "uint256", name: "_tokenId", type: "uint256"},
            {
                internalType: "address",
                name: "_nftContractAddress",
                type: "address",
            },
            {internalType: "string", name: "_message", type: "string"},
        ],
        name: "sendERC721To",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {internalType: "address", name: "_recipient", type: "address"},
            {internalType: "uint256", name: "", type: "uint256"},
            {internalType: "string", name: "_message", type: "string"},
        ],
        name: "sendTo",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {internalType: "address", name: "_recipient", type: "address"},
            {internalType: "uint256", name: "_amount", type: "uint256"},
            {
                internalType: "address",
                name: "_tokenContractAddr",
                type: "address",
            },
            {internalType: "string", name: "_message", type: "string"},
        ],
        name: "sendTokenTo",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [{internalType: "bytes4", name: "interfaceId", type: "bytes4"}],
        name: "supportsInterface",
        outputs: [{internalType: "bool", name: "", type: "bool"}],
        stateMutability: "pure",
        type: "function",
    },
    {
        inputs: [{internalType: "address", name: "newOwner", type: "address"}],
        name: "transferOwnership",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [],
        name: "withdraw",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [
            {internalType: "address", name: "_tokenContract", type: "address"},
        ],
        name: "withdrawToken",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
    },
];
let tippingAddressBase = "0x324Ad1738B9308D5AF5E81eDd6389BFa082a8968";
let tippingAddressEthereum = "0xe18036D7E3377801a19d5Db3f9b236617979674E";
let tippingAddressPolygon = "0xe35B356ac2c880cCcc769bA9393F0748d94ABBCa";
let tippingAddressAleph = "0xcA6742d2d6B9dBFFD841DF25C15cFf45FBbB98f4";
let tippingAddressOptimism = "0x43F532D678b6a1587BE989a50526F89428f68315";
let tippingAddressMantle = "0x324Ad1738B9308D5AF5E81eDd6389BFa082a8968";
const NATIVE_ADDRESS = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee";
const NULL_ADDRESS = "0x0000000000000000000000000000000000000000";

const web3Base = new Web3(
    new Web3.providers.HttpProvider("https://mainnet.base.org")
);
const web3Ethereum = new Web3(
    new Web3.providers.HttpProvider("https://eth.llamarpc.com")
);
const web3Polygon = new Web3(
    new Web3.providers.HttpProvider("https://polygon-rpc.com/")
);
const web3Aleph = new Web3(
    new Web3.providers.HttpProvider("https://rpc.alephzero.raas.gelato.cloud")
);
const web3Optimism = new Web3(
    new Web3.providers.HttpProvider("https://mainnet.optimism.io")
);
const web3Mantle = new Web3(
    new Web3.providers.HttpProvider("https://mantle.publicnode.com")
);

const DECIMALS_BY_NETWORK_AND_TOKEN = {
    base: {
        "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee": 18,
        "0xfa980ced6895ac314e7de34ef1bfae90a5add21b": 18, // PRIME
        "0x4ed4e862860bed51a9570b96d89af5e1b0efefed": 18, // DEGEN
        "0xeff2a458e464b07088bdb441c21a42ab4b61e07e": 18, // PDT
        "0x25f8087ead173b73d6e8b84329989a8eea16cf73": 18, // PDT
        "0x50c5725949a6f0c72e6c4a641f24049a917db0cb": 18, // DAI
        "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913": 6, // USDC
    },
    ethereum: {
        "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee": 18,
        "0x6b175474e89094c44da98b954eedeac495271d0f": 18, // DAI
        "0xb23d80f5fefcddaa212212f028021b41ded428cf": 18, // PRIME
        "0x3f382dbd960e3a9bbceae22651e88158d2791550": 18, // GHST
        "0x25f8087ead173b73d6e8b84329989a8eea16cf73": 18, // YGG
        "0x375abb85c329753b1ba849a601438ae77eec9893": 18, // PDT
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": 6, // USDC
    },
    polygon: {
        "0x82617aa52dddf5ed9bb7b370ed777b3182a30fd1": 18, // YGG
        "0x385eeac5cb85a38a9a07a70c73e0a3271cfb54a7": 18, // GHST
        "0x8f3cf7ad23cd3cadbd9735aff958023239c6a063": 18, // DAI
        "0x2791bca1f2de4661ed88a30c99a7a9449aa84174": 6, // USDC
    },
    aleph: {
        "0x4ca4b85ead5ea49892d3a81dbfae2f5c2f75d53d": 6, // USDC
    },
    optimism: {
        "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee": 18,
        "0x0b2c639c533813f4aa9d7837caf62653d097Ff85": 6, // USDC
        "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1": 18, // DAI
    },
    mantle: {
        "0x09bc4e0d864854c6afb6eb9a9cdf58ac190d0df9": 6, //USDC
    },
};

const NETWORK_IDS = {
    base: 8453,
    ethereum: 1,
    polygon: 137,
    aleph: 41455,
    mantle: 5000,
    optimism: 10,
};

const SELL_TOKEN_BY_NETWORK = {
    base: "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
    ethereum: "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    polygon: "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
    aleph: "0x4ca4b85ead5ea49892d3a81dbfae2f5c2f75d53d",
    mantle: "0x09bc4e0d864854c6afb6eb9a9cdf58ac190d0df9",
    optimism: "0x0b2c639c533813f4aa9d7837caf62653d097Ff85",
};

async function loadTipping(web3, contractAddr, contractABI) {
    return await new web3.eth.Contract(contractABI, contractAddr);
}

async function loadTippingContracts() {
    tippingBase = await loadTipping(
        web3Base,
        tippingAddressBase,
        abiTippingBase
    );
    tippingEthereum = await loadTipping(
        web3Ethereum,
        tippingAddressEthereum,
        abiTippingOG
    );
    tippingPolygon = await loadTipping(
        web3Polygon,
        tippingAddressPolygon,
        abiTippingOG
    );
    tippingAleph = await loadTipping(
        web3Aleph,
        tippingAddressAleph,
        abiTippingBase
    );
    tippingOptimism = await loadTipping(
        web3Optimism,
        tippingAddressOptimism,
        abiTippingBase
    );
    tippingMantle = await loadTipping(
        web3Mantle,
        tippingAddressMantle,
        abiTippingBase
    );
}

async function setCurrBlock() {
    currBlockBase = await web3Base.eth.getBlockNumber();
    currBlockEthereum = await web3Ethereum.eth.getBlockNumber();
    currBlockPolygon = await web3Polygon.eth.getBlockNumber();
    currBlockAleph = await web3Aleph.eth.getBlockNumber();
    currBlockOptimism = await web3Optimism.eth.getBlockNumber();
    currBlockMantle = await web3Mantle.eth.getBlockNumber();
}

async function getInputs(_method, _remove) {
    // OG/OP/Base/Aleph sendTo()
    if (_method == "16e49145") {
        return await web3Base.eth.abi.decodeParameters(
            [
                {
                    type: "address",
                    name: "_recipient",
                },
                {
                    type: "uint256",
                    name: "_amount",
                },
                {
                    type: "string",
                    name: "_message",
                },
            ],
            _remove
        );
        // OG/OP sendTokenTo()
    } else if (_method == "41dfeca5") {
        return await web3Base.eth.abi.decodeParameters(
            [
                {
                    type: "address",
                    name: "_recipient",
                },
                {
                    type: "uint256",
                    name: "_amount",
                },
                {
                    type: "address",
                    name: "_tokenContractAddr",
                },
                {
                    type: "string",
                    name: "_message",
                },
            ],
            _remove
        );
    }
}

function roundUp(num, precision) {
    precision = Math.pow(10, precision);
    return Math.ceil(num * precision) / precision;
}

async function fetchDonations() {
    console.log("Searching on base from block: ", currBlockBase);

    let tempNewDonations = new Array();

    eventsBase = await tippingBase.getPastEvents("TipMessage", {
        fromBlock: currBlockBase - 5,
        filter: {
            recipientAddress: streamerAddress,
        },
    });
    for (let i = 0; i < eventsBase.length; i++) {
        if (!txnHashes.includes(eventsBase[i].transactionHash)) {
            txn = await web3Base.eth.getTransaction(
                eventsBase[i].transactionHash
            );
            from_ = txn.from;
            let method = txn.input.slice(2, 10);
            let remove = txn.input.replace(method, "");
            let inputs = await getInputs(method, remove);
            let tempRet = {
                amount: inputs._amount,
                tokenAddress: eventsBase[i].returnValues.tokenAddress,
                tokenId: inputs._assetId,
                message: eventsBase[i].returnValues.message,
                fromAddress: from_,
                network: "base",
            };

            tempNewDonations.push(tempRet);
            txnHashes.push(eventsBase[i].transactionHash);
        }
    }

    console.log("Searching on eth from block: ", currBlockEthereum);

    eventsEthereum = await tippingEthereum.getPastEvents("TipMessage", {
        fromBlock: currBlockEthereum - 5,
        filter: {
            recipientAddress: streamerAddress,
        },
    });
    for (let i = 0; i < eventsEthereum.length; i++) {
        if (!txnHashes.includes(eventsEthereum[i].transactionHash)) {
            txn = await web3Ethereum.eth.getTransaction(
                eventsEthereum[i].transactionHash
            );
            from_ = txn.from;
            let method = txn.input.slice(2, 10);
            let remove = txn.input.replace(method, "");
            let inputs = await getInputs(method, remove);
            let tempRet = {
                amount: inputs._amount,
                tokenAddress: eventsEthereum[i].returnValues.tokenAddress,
                tokenId: inputs._assetId,
                message: eventsEthereum[i].returnValues.message,
                fromAddress: from_,
                network: "ethereum",
            };

            tempNewDonations.push(tempRet);
            txnHashes.push(eventsEthereum[i].transactionHash);
        }
    }

    console.log("Searching on poly from block: ", currBlockPolygon);
    eventsPolygon = await tippingPolygon.getPastEvents("TipMessage", {
        fromBlock: currBlockPolygon - 5,
        filter: {
            recipientAddress: streamerAddress,
        },
    });
    for (let i = 0; i < eventsPolygon.length; i++) {
        if (!txnHashes.includes(eventsPolygon[i].transactionHash)) {
            txn = await web3Polygon.eth.getTransaction(
                eventsPolygon[i].transactionHash
            );
            from_ = txn.from;
            let method = txn.input.slice(2, 10);
            let remove = txn.input.replace(method, "");
            let inputs = await getInputs(method, remove);
            let tempRet = {
                amount: inputs._amount,
                tokenAddress: eventsPolygon[i].returnValues.tokenAddress,
                tokenId: inputs._assetId,
                message: eventsPolygon[i].returnValues.message,
                fromAddress: from_,
                network: "polygon",
            };

            tempNewDonations.push(tempRet);
            txnHashes.push(eventsPolygon[i].transactionHash);
        }
    }

    console.log("Searching on aleph from block: ", currBlockAleph);
    eventsAleph = await tippingAleph.getPastEvents("TipMessage", {
        fromBlock: currBlockAleph - 5,
        filter: {
            recipientAddress: streamerAddress,
        },
    });
    for (let i = 0; i < eventsAleph.length; i++) {
        if (!txnHashes.includes(eventsAleph[i].transactionHash)) {
            txn = await web3Aleph.eth.getTransaction(
                eventsAleph[i].transactionHash
            );
            from_ = txn.from;
            let method = txn.input.slice(2, 10);
            let remove = txn.input.replace(method, "");
            let inputs = await getInputs(method, remove);
            let tempRet = {
                amount: inputs._amount,
                tokenAddress: eventsAleph[i].returnValues.tokenAddress,
                tokenId: inputs._assetId,
                message: eventsAleph[i].returnValues.message,
                fromAddress: from_,
                network: "aleph",
            };

            tempNewDonations.push(tempRet);
            txnHashes.push(eventsAleph[i].transactionHash);
        }
    }

    console.log("Searching on optimism from block: ", currBlockOptimism);
    eventsOptimism = await tippingOptimism.getPastEvents("TipMessage", {
        fromBlock: currBlockOptimism - 5,
        filter: {
            recipientAddress: streamerAddress,
        },
    });
    for (let i = 0; i < eventsOptimism.length; i++) {
        if (!txnHashes.includes(eventsOptimism[i].transactionHash)) {
            txn = await web3Optimism.eth.getTransaction(
                eventsOptimism[i].transactionHash
            );
            from_ = txn.from;
            let method = txn.input.slice(2, 10);
            let remove = txn.input.replace(method, "");
            let inputs = await getInputs(method, remove);
            let tempRet = {
                amount: inputs._amount,
                tokenAddress: eventsOptimism[i].returnValues.tokenAddress,
                tokenId: inputs._assetId,
                message: eventsOptimism[i].returnValues.message,
                fromAddress: from_,
                network: "optimism",
            };

            tempNewDonations.push(tempRet);
            txnHashes.push(eventsOptimism[i].transactionHash);
        }
    }

    console.log("Searching on mantle from block: ", currBlockMantle);
    eventsMantle = await tippingMantle.getPastEvents("TipMessage", {
        fromBlock: currBlockMantle - 5,
        filter: {
            recipientAddress: streamerAddress,
        },
    });
    for (let i = 0; i < eventsMantle.length; i++) {
        if (!txnHashes.includes(eventsMantle[i].transactionHash)) {
            txn = await web3Mantle.eth.getTransaction(
                eventsMantle[i].transactionHash
            );
            from_ = txn.from;
            let method = txn.input.slice(2, 10);
            let remove = txn.input.replace(method, "");
            let inputs = await getInputs(method, remove);
            let tempRet = {
                amount: inputs._amount,
                tokenAddress: eventsMantle[i].returnValues.tokenAddress,
                tokenId: inputs._assetId,
                message: eventsMantle[i].returnValues.message,
                fromAddress: from_,
                network: "mantle",
            };

            tempNewDonations.push(tempRet);
            txnHashes.push(eventsMantle[i].transactionHash);
        }
    }

    await setCurrBlock();

    return tempNewDonations;
}

async function getVal(tippingAmount, tokenPerDollar, decimals) {
    return roundUp(tippingAmount / Math.pow(10, decimals) / tokenPerDollar, 2);
}

async function calculateDollar(_assetAddr, _amount, _network) {
    let amount_per_dollar = "1";
    if (_assetAddr == NULL_ADDRESS) {
        _assetAddr = NATIVE_ADDRESS;
    }
    let decimals =
        DECIMALS_BY_NETWORK_AND_TOKEN[_network.toLowerCase()][
            _assetAddr.toLowerCase()
        ];

    if (
        SELL_TOKEN_BY_NETWORK[_network.toLowerCase()] !=
        _assetAddr.toLowerCase()
    ) {
        let url = `https://api.idriss.xyz/token-price?sellToken=${
            SELL_TOKEN_BY_NETWORK[_network]
        }&buyToken=${_assetAddr.toLowerCase()}&network=${
            NETWORK_IDS[_network.toLowerCase()]
        }&sellAmount=1000000`;
        let responseNew = await (await fetch(url)).json();
        amount_per_dollar = responseNew["price"];
    }
    let val = this.getVal(_amount, amount_per_dollar, decimals);
    return val;
}

let useWebSocket = false;
let ws;
let interval;

function retryWebSocketConnection() {
    if (useWebSocket) return; // Skip if WebSocket is already connected

    console.log("Retrying WebSocket connection...");
    ws = new WebSocket("ws://localhost:8080");

    ws.onopen = () => {
        console.log("Connected to WebSocket server!");
        useWebSocket = true;
        stopQueryingChain();
        init();
    };

    ws.onmessage = (event) => {
        try {
            const {action, data} = JSON.parse(event.data);

            if (action === "show") {
                document.getElementById("baseInfo").innerHTML =
                    data.baseInfo || "Unknown Address";
                document.getElementById("message").innerHTML =
                    data.message || "Thank you!";

                document.getElementById("fader").style.opacity = 1;

                setTimeout(() => {
                    document.getElementById("fader").style.opacity = 0;
                }, 10000);
            }
        } catch (err) {
            console.error("Invalid WebSocket message:", err);
        }
    };

    ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        useWebSocket = false;
        init();
    };

    ws.onclose = () => {
        console.log("WebSocket connection closed.");
        if (useWebSocket) {
            useWebSocket = false;
            init();
        }
    };
}

// Start the WebSocket and retry logic
function setupWebSocket() {
    retryWebSocketConnection(); // Attempt initial connection
    try {
        setInterval(retryWebSocketConnection, 60000); // Retry every minute
    } catch {
        console.log("Websocket not online");
    }
}

// Blockchain querying fallback
function stopQueryingChain() {
    if (interval) {
        clearInterval(interval);
        interval = null;
        console.log("Stopped blockchain querying.");
    }
}

displayAlerts = setInterval(async function () {
    if (useWebSocket) return; // Skip polling if WebSocket is active

    if (resTip.length > 0) {
        if (document.getElementById("fader").style.opacity == 0) {
            const audio = document.getElementById("notification-sound");
            document.getElementById("baseInfo").innerHTML = resTip[0][0];
            document.getElementById("message").innerHTML = resTip[0][1];
            document.getElementById("fader").style.opacity = 1;

            audio.currentTime = 0;
            audio.play().catch((error) => {
                console.warn("Audio playback failed:", error);
            });

            resTip.shift();
            console.log("timeout start");
            await setTimeout(function () {
                document.getElementById("fader").style.opacity = 0;
            }, 10000);
            console.log("timeout end");
        }
    }
}, 2000);

document.addEventListener("keydown", function (event) {
    if (event.ctrlKey && event.shiftKey && event.key === "!") {
        triggerTestAlert();
    }
});

function triggerTestAlert() {
    if (useWebSocket && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({action: "test"}));
    } else {
        // Fallback to local test
        const audio = document.getElementById("notification-sound");
        document.getElementById("baseInfo").innerHTML = "Test Donation!";
        document.getElementById("message").innerHTML = "Great Stream!!";
        document.getElementById("fader").style.opacity = 1;

        audio.currentTime = 0;
        audio.play().catch((error) => {
            console.warn("Audio playback failed:", error);
        });

        setTimeout(function () {
            document.getElementById("fader").style.opacity = 0;
        }, 10000);
    }
}

async function init() {
    if (useWebSocket) {
        console.log(
            "Using WebSocket connection; skipping blockchain querying."
        );
        return;
    }

    console.log("No WebSocket connection; initializing blockchain querying.");
    await loadTippingContracts();
    await setCurrBlock();
    txnHashes = new Array();
    startQueryingChain();
}

// Start the interval for querying the blockchain
function startQueryingChain() {
    if (interval) {
        console.log("Blockchain querying is already active.");
        return; // Prevent multiple intervals from being set
    }

    interval = setInterval(async function () {
        ret = await fetchDonations();
        retString = "";
        for (let i = 0; i < ret.length; i++) {
            fromAccount = ret[i].fromAddress;
            if (typeof ret[i].tokenId == "undefined") {
                let reverse = (await resolveENS(fromAccount, web3Ethereum)).ens;
                fromAccountIdentifier = reverse
                    ? reverse
                    : fromAccount
                          .substring(0, 4)
                          .concat("...")
                          .concat(fromAccount.substr(-2));
                basicInfo =
                    fromAccountIdentifier +
                    " sent " +
                    "$" +
                    (await calculateDollar(
                        ret[i].tokenAddress,
                        ret[i].amount,
                        ret[i].network.toLowerCase()
                    ));
            } else {
                continue;
            }

            message = ret[i].message;
            resTip.push([basicInfo, message]);
        }
    }, 5000);
}
