VERIFIED_ADDRESSES_QUERY = """
  query GetMostRecentVerifiedAddresses($fc_name: String!) {
  Socials(
    input: {filter: {profileName: {_eq: $fc_name}, dappName: {_eq: farcaster}}, blockchain: ethereum, order: {updatedAt: ASC}, limit: 10}
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

FOLLOWER_QUERY = """query MyQuery($cursor: String!) {
  SocialFollowers(
    input: {filter: {dappName: {_eq: farcaster}, identity: {_eq: "fc_fname:idriss"}}, blockchain: ALL, limit: 200, cursor: $cursor}
  ) {
    Follower {
      followerAddress {
        socials(input: {filter: {dappName: {_eq: farcaster}}}) {
          profileName
          userId
          connectedAddresses {
            address
            timestamp
          }
        }
      }
    }
    pageInfo {
      nextCursor
      hasNextPage
    }
  }
}"""