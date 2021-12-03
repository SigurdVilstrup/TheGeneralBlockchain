# The General Blockchain

The purpose of the general blockchain is to create a blockchain that enables easier understanding and general knowledge of how a blockchain works and how it might help organisations structure their data in a secure manner.

The General Blockchain project has been developed as part of Sigurd PvA Vilstrup's Master thesis in Technology Based Business Development at Aarhus University.

The blockchain is python based, and should be easily understood and very accesible.

Currently this project is a work in progress. It is currently able to display how a blockchain stores data and communicates with nodes, but is missing alot of the actual functionality of an actual blockchain. It's mainly a GUI that displays blockchain functionality, with a load of non-functioning machine code underneath.

## Todo

- Interfacing between the modules, i.e.:
  - Local blockchain
    - WIP // Main functionality thats missing is calculation of PoW 
  - Communication
    - Can send all information back and forth, but optmization and such is needed
  - ~~GUI~~ ✔
- In general refactoring and optimization of all code

### Communication protocol

- Optimized dynamic communication protocol
- ~~Defined number of functions to call from nodes, i.e.: updateBlockchain(), addBlock(), etc.~~ ✔

### Local Blockchain

- More JSON support

### Graphic

- ~~Tkinter to create graphic user interface~~ ✔

  - ~~Main window~~ ✔
  - ~~TGB canvas~~ ✔
  - ~~Block overview~~ ✔
  - ~~Nodes overview~~ ✔

- UI improvements

  - ~~Search fuctionality~~ ✔
  - ~~Node information functionality~~ ✔
  - ~~Block information functionality~~ ✔

- Interfacing with:
  - ~~other elements user interaction, i.e.: buttons etc.~~ ✔
  - ~~local blockchain - i.e.: showing state of the blockchain~~ ✔
  - ~~other nodes in network~~ ✔
