DEFAULT_NETWORK="1"
NATIVE_ADDRESS="0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
WRAPPED_MANTLE_ON_ETH = "0x3c3a81e81dc49a522a592e7622a7e711c06bf354"
USDC_ADDRESS_ON_ETH="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
DAI_ADDRESS_ON_ETH="0x6b175474e89094c44da98b954eedeac495271d0f"
NULL_ADDRESS = "0x0000000000000000000000000000000000000000"

DONATION_CONTRACT_ADDRESS_PER_CHAIN_ID = {
  8453: '0x7960312ca63e291244d180E75A8A0AC4a18032F7',
  59144: '0x63c461A407FaE2E7F743B9be79A8DdF815D0F487',
  10: '0x0c51AE117e8e4028e653FA3Bd5ccBaB97861c045',
  324: '0x13B73661A4B601f22346421c19Cf97628ba1FdCF',
  42161: '0xF3D400cA68F79d27DDa6cc7B1E6fEf8b444FE016',
  1: '0x63c461A407FaE2E7F743B9be79A8DdF815D0F487',
}

PRICING_API_URL = {
    "1": "https://api.0x.org",
    "10": "https://optimism.api.0x.org",
    "56": "https://bsc.api.0x.org",
    "137": "https://polygon.api.0x.org",
    "8453": "https://base.api.0x.org",
    "42161": "https://arbitrum.api.0x.org"
}


TOKEN_ROUTE = {
    f"5000:{NATIVE_ADDRESS}": WRAPPED_MANTLE_ON_ETH,
    f"324:{NATIVE_ADDRESS}": NATIVE_ADDRESS,
    f"59144:{NATIVE_ADDRESS}": NATIVE_ADDRESS,
    f"534352:{NATIVE_ADDRESS}": NATIVE_ADDRESS,
    "324:0x3355df6d4c9c3035724fd0e3914de96a5a83aaf4": USDC_ADDRESS_ON_ETH,
    "5000:0x09bc4e0d864854c6afb6eb9a9cdf58ac190d0df9": USDC_ADDRESS_ON_ETH,
    "59144:0x176211869ca2b568f2a7d4ee941e073a821ee1ff": USDC_ADDRESS_ON_ETH,
    "534352:0x06efdbff2a14a7c8e15944d1f4a48f9f95f663a4": USDC_ADDRESS_ON_ETH,
    "324:0x4b9eb6c0b6ea15176bbf62841c6b2a8a398cb656": DAI_ADDRESS_ON_ETH,
    "59144:0x4af15ec2a0bd43db75dd04e62faa3b8ef36b00d5": DAI_ADDRESS_ON_ETH,
    "534352:0xca77eb3fefe3725dc33bccb54edefc3d9f764f97": DAI_ADDRESS_ON_ETH
}

UNSUPPORTED_0x_NETWORKS = ["324", "5000", "59144", "534352"]

TALLY_QUERY = """
    query Proposals($input: ProposalsInput!) {
  proposals(input: $input) {
    nodes {
      ... on Proposal {
        id
        end {
          ... on Block {
            timestamp
          }
          ... on BlocklessTimestamp {
            timestamp
          }
        }
        metadata {
          title
          description
        }
        status
        creator {
          address
          name
          ens
        }
        organization {
          id
          name
          slug
        }
      }
    }
    pageInfo {
      firstCursor
      lastCursor
      count
    }
  }
}
"""

FALLBACK_IMG_URL = (
    "https://pbs.twimg.com/profile_images/1712233319411183616/s3skd3R4_400x400.jpg"
)