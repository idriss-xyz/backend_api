DEFAULT_NETWORK = "1"
NATIVE_ADDRESS = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
ABSTRACT_PENGU_ADDRESS = "0x9ebe3a824ca958e4b3da772d2065518f009cba62"
WRAPPED_MANTLE_ON_ETH = "0x3c3a81e81dc49a522a592e7622a7e711c06bf354"
USDC_ADDRESS_ON_ETH = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
USDC_ADDRESS_ON_ALEPH = "0x4ca4b85ead5ea49892d3a81dbfae2f5c2f75d53d"
USDC_ADDRESS_ON_ABSTRACT = "0x84a71ccd554cc1b02749b35d22f684cc8ec987e1"
DAI_ADDRESS_ON_ETH = "0x6b175474e89094c44da98b954eedeac495271d0f"
NULL_ADDRESS = "0x0000000000000000000000000000000000000000"

INELIGIBLE = {
    "paid": 0,
    "free": 0,
    "extension": 0,
    "registration": "2022-06-01T00:00:00",
    "invites": 0.0,
    "farcaster": 0,
    "hacker": 0,
    "ardent": 0,
    "aavegotchi": 0,
    "gitcoin": 0,
    "across": 0,
    "polymarket": 0,
    "snapshot": 0,
    "tally": 0,
    "jumper": 0,
    "allocation_gitcoin": 0,
    "time_multiplier": 1.0,
    "invite_multiplier": 1.0,
    "allocation_usage": 0,
    "allocation_paid": 0.0,
    "allocation_free": 0.0,
    "allocation_extension": 0.0,
    "allocation_partner": 0,
    "allocation": 0,
}

USDC_DECIMALS = 6

PRIORITY_GITCOIN_ROUNDS = [("388", 42161), ("389", 42161)]
PRIORITY_GITCOIN_ROUNDS_MAPPING = {
    combo: index for index, combo in enumerate(PRIORITY_GITCOIN_ROUNDS)
}

PRICING_API_URL = {
    "1": "https://api.0x.org",
    "10": "https://optimism.api.0x.org",
    "56": "https://bsc.api.0x.org",
    "137": "https://polygon.api.0x.org",
    "8453": "https://base.api.0x.org",
    "42161": "https://arbitrum.api.0x.org",
}


TOKEN_ROUTE = {
    f"5000:{NATIVE_ADDRESS}": WRAPPED_MANTLE_ON_ETH,
    f"324:{NATIVE_ADDRESS}": NATIVE_ADDRESS,
    f"59144:{NATIVE_ADDRESS}": NATIVE_ADDRESS,
    f"534352:{NATIVE_ADDRESS}": NATIVE_ADDRESS,
    f"41455:{USDC_ADDRESS_ON_ALEPH}": USDC_ADDRESS_ON_ETH,
    f"2741:{NATIVE_ADDRESS}": NATIVE_ADDRESS,
    f"2741:{USDC_ADDRESS_ON_ABSTRACT}": USDC_ADDRESS_ON_ETH,
    "41455:0xb3f0ee446723f4258862d949b4c9688e7e7d35d3": NATIVE_ADDRESS,
    "324:0x3355df6d4c9c3035724fd0e3914de96a5a83aaf4": USDC_ADDRESS_ON_ETH,
    "5000:0x09bc4e0d864854c6afb6eb9a9cdf58ac190d0df9": USDC_ADDRESS_ON_ETH,
    "59144:0x176211869ca2b568f2a7d4ee941e073a821ee1ff": USDC_ADDRESS_ON_ETH,
    "534352:0x06efdbff2a14a7c8e15944d1f4a48f9f95f663a4": USDC_ADDRESS_ON_ETH,
    "324:0x4b9eb6c0b6ea15176bbf62841c6b2a8a398cb656": DAI_ADDRESS_ON_ETH,
    "59144:0x4af15ec2a0bd43db75dd04e62faa3b8ef36b00d5": DAI_ADDRESS_ON_ETH,
    "534352:0xca77eb3fefe3725dc33bccb54edefc3d9f764f97": DAI_ADDRESS_ON_ETH,
}

UNSUPPORTED_0x_NETWORKS = ["324", "2741", "5000", "41455", "59144", "534352"]

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
