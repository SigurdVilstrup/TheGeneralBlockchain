# Protocol for communication in The General Blockchain

Description of the communication protocol for The General Blockchain.
The protocols are described here to enable optmization of the current methods as well as interfacing with the blockchain without running these scripts.

## Table of Contents

- [Basic protocol](#protocol)
- [Commands](#commands)
- [Data Transfer](#Data-transfer)

---

## Protocol

All communication in The General Blockchain consists of a Preheader followed by either a header or a body of information. The Preheader can be of type 'CMND' or 'DATA'. The Preheader is always of length 16 bytes and is prefaced with either 'CMND' or 'DATA' to tell the program what it is to do. The Preheader then consists of the size of the following piece of information/data. I.e.:

    preHeader = b'CMND723         '
    # Where preheader is type=CMND and of len=723

The transmitting node then received the preheader and requests either data or command of the size defined in the preHeader.

---

## Commands

**List of commands:**

- Update(BlockchainLen, latestHash)

Sends request to nodes in network to check whether the local blockchain is updated. This should be called before creating a new block in the network.

    - blockchainLen : int
    - latestHast    : str[32]

- updateNewBlock(blockLen, LatestHash)

Sends newly created block to known nodes.

    - blockLen      : int
    - latestHash    : str[32]

---

## Data Transfer

- getPreHeader()
- getHeader()
- getBody()
