VERIFIED_ADDRESSES_QUERY = """
  query GetMostRecentVerifiedAddresses($fc_name: String!) {
  Socials(
    input: {filter:
              {profileName: {_eq: $fc_name}, dappName: {_eq: farcaster}},
              blockchain: ethereum,
              order: {updatedAt: ASC},
              limit: 10
            }
  ) {
    Social {
      profileName
      connectedAddresses {
        address
        blockchain
        timestamp
      }
      userId
    }
  }
}
"""
