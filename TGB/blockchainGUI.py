from base64 import decode
import binascii
from copy import copy
import datetime
import hashlib
from pydoc import text
from telnetlib import IP
import tkinter as tk

import re as re
from turtle import width

import jsonpickle

from LocalBlockchain import Blockchain

from secp256k1Crypto import PrivateKey, PublicKey, ECDSA


class tgbGUI:
    def __init__(self, root, blockchainRef: Blockchain):
        self.blockchain = blockchainRef
        self.blocks = blockchainRef.blocks
        self.nodeList = [Blockchain.tgbNode('Example', 'localhost'), ]

        for node in blockchainRef.nodeList:
            self.nodeList.append(node)

        self.root = root
        self.root.iconphoto(False, tk.PhotoImage(
            file='Graphics/icon.drawio.png'))
        self.root.title('The General Blockchain')
        self.root.geometry('1200x900')
        self.root.configure(background='white')

        self._tgbHeader()

        self.frm_blockRep = tk.Frame(master=self.root,
                                     relief='sunken',
                                     borderwidth=2, background='white')

        self._blockRepresentation(masterFrame=self.frm_blockRep)

        self.frm_nodeRep = tk.Frame(master=self.root, relief='sunken',
                                    borderwidth=2,
                                    background='white')
        self._nodeRepresentation(
            masterFrame=self.frm_nodeRep, dimensions=(1200, 550))

    def _forceUpdate(self):
        self._forceUpdateNodes()
        self._forceUpdateBlocks()

    def _forceUpdateBlocks(self, destroyWindow=None):
        self.frm_blockRep.destroy()
        self.frm_blockRep = tk.Frame(master=self.root,
                                     relief='sunken',
                                     borderwidth=2, background='white')

        self._blockRepresentation(masterFrame=self.frm_blockRep)

        if destroyWindow:
            destroyWindow.destroy()

    def _openNewTransactionsWindow(self):
        self.newTransactionWindow = tk.Toplevel(self.root)
        self.newTransactionWindow.title('Broadcast new transaction')
        self.newTransactionWindow.iconphoto(False, tk.PhotoImage(
            file='Graphics/icon.drawio.png'))
        self.newTransactionWindow.configure(background='white')

        tk.Label(master=self.newTransactionWindow, text='Batch no.: ',
                 background='white').grid(padx=5, pady=5, column=0, row=0)

        productList = ['Milk#8751', 'Milk#5214', 'Cheese#6701', 'Cheese#6011']

        option_var_product = tk.StringVar()
        option_var_product.set(productList[0])

        tk.OptionMenu(self.newTransactionWindow,
                      option_var_product,
                      *productList).grid(padx=5, pady=5, column=1, row=0)

        tk.Label(master=self.newTransactionWindow, text='Transaction author: ',
                 background='white').grid(padx=5, pady=5, column=0, row=1)

        authorList = []

        for node in self.nodeList:
            authorList.append(node.name)

        option_var = tk.StringVar()
        option_var.set(authorList[0])

        tk.OptionMenu(self.newTransactionWindow,
                      option_var,
                      *authorList).grid(padx=5, pady=5, column=1, row=1)

        tk.Label(master=self.newTransactionWindow,
                 text='Transactional data:', background='white').grid(padx=5, pady=5, column=0, row=2)
        ent_data = tk.Entry(
            master=self.newTransactionWindow, width=100)
        ent_data.grid(padx=5, pady=5, column=1, row=2)

        tk.Button(
            master=self.newTransactionWindow,
            text='Broadcast transaction',
            command=lambda t=ent_data, a=option_var, p=option_var_product: self._addNewBlock(transactionEnt=t, author=a, product=p)).grid(padx=5, pady=5, column=1, row=3)

    def _addNewBlock(self, transactionEnt, author, product):
        transData = transactionEnt.get()
        authorName = author.get()
        productID = product.get()

        print(authorName)

        authorNode = None

        for node in self.nodeList:
            if authorName == node.name:
                authorNode = node

        signature = authorNode.private_key.ecdsa_sign(
            transData.encode('utf-8'))

        transaction = Blockchain.Block.Body.Transaction(
            epochTimestamp=datetime.datetime.now().timestamp(),
            data=transData,
            author=authorNode.name,
            signature=binascii.hexlify(
                node.private_key.ecdsa_serialize(signature)).decode('utf-8'),
            productID=productID)

        previousHash = self.blocks[-1].header.calcHash() if (
            len(self.blocks) != 0) else '0'

        self.blocks.append(Blockchain.Block(
            datetime.datetime.now(),
            transaction,
            previousHash))

        self._forceUpdateBlocks(destroyWindow=self.newTransactionWindow)
        pass

    def _openNewNodeWindow(self):
        self.newNodeWindow = tk.Toplevel(self.root)
        self.newNodeWindow.title('Add new node')
        self.newNodeWindow.iconphoto(False, tk.PhotoImage(
            file='Graphics/icon.drawio.png'))
        self.newNodeWindow.configure(background='white')

        # Display info with ability to change name
        frm_newNode = tk.Frame(master=self.newNodeWindow, background='white')

        tk.Label(
            master=frm_newNode,
            text="ip:\t",
            anchor='w',
            background='white').grid(column=0, row=0, sticky='w', padx=5, pady=5)
        tk.Label(
            master=frm_newNode,
            text="name:\t",
            anchor='w',
            background='white').grid(column=0, row=1, padx=5, pady=5)

        ent_ip = tk.Entry(master=frm_newNode)
        ent_ip.grid(column=1, row=0, padx=5, pady=5)

        ent_name = tk.Entry(master=frm_newNode)
        ent_name.grid(column=1, row=1, padx=5, pady=5)

        tk.Button(
            master=frm_newNode,
            text='Add new node',
            command=lambda ip=ent_ip, name=ent_name: self._addNewNode(ip, name)).grid(column=3, row=3, padx=15, pady=15)

        frm_newNode.pack()

    def _addNewNode(self, ip, name):
        self.nodeList.append(Blockchain.tgbNode(
            name=name.get(), ip=name.get()))

        self._forceUpdateNodes(destroyWindow=self.newNodeWindow)

    def _nameNode(self, nodeIndex, newNameEnt):
        self.nodeList[nodeIndex].name = newNameEnt.get()

        self._forceUpdateNodes(destroyWindow=self.nodeWindow)
        # Update the main Node rep screen

    def _forceUpdateNodes(self, destroyWindow=None):
        self.frm_nodeRep.destroy()
        self.frm_nodeRep = tk.Frame(master=self.root, relief='sunken',
                                    borderwidth=2,
                                    background='white')
        self._nodeRepresentation(
            masterFrame=self.frm_nodeRep,
            dimensions=(1200, 550))

        if destroyWindow:
            destroyWindow.destroy()

    def _openNodeWindow(self, index):
        self.nodeWindow = tk.Toplevel(self.root)
        self.nodeWindow.title('Node %s Information' % index)
        self.nodeWindow.iconphoto(False, tk.PhotoImage(
            file='Graphics/icon.drawio.png'))
        self.nodeWindow.geometry('825x520')
        self.nodeWindow.configure(background='white')

        # Get info: IP, Network, Name, Index

        # Display info with ability to change name
        frm_info = tk.Frame(master=self.nodeWindow, background='white')

        tk.Label(
            master=frm_info,
            text="Ip address:\t",
            anchor='w',
            background='white').grid(column=0, row=0, sticky='w', padx=5, pady=5)
        lbl_ip = tk.Label(
            master=frm_info,
            text=self.nodeList[index].ip,
            justify='left',
            anchor='w',
            background='white').grid(column=1, row=0, sticky='w', padx=5, pady=5)
        tk.Label(
            master=frm_info,
            text="Name:\t",
            anchor='w',
            background='white').grid(column=0, row=1, sticky='w', padx=5, pady=5)
        lbl_name = tk.Label(
            master=frm_info,
            text=self.nodeList[index].name,
            justify='left',
            anchor='w',
            background='white').grid(column=1, row=1, sticky='w', padx=5, pady=5)
        tk.Label(
            master=frm_info,
            text="Private key:\t",
            anchor='w',
            background='white').grid(column=0, row=2, padx=5, pady=5)
        lbl_name = tk.Label(
            master=frm_info,
            text=self.nodeList[index].show_private(),
            justify='left',
            anchor='w',
            background='white').grid(column=1, row=2, sticky='w', padx=5, pady=5)
        tk.Label(
            master=frm_info,
            text="Public key:\t",
            anchor='w',
            background='white').grid(column=0, row=3, sticky='w', padx=5, pady=5)
        lbl_name = tk.Label(
            master=frm_info,
            text=self.nodeList[index].show_public(),
            justify='left',
            anchor='w',
            background='white').grid(column=1, row=3, sticky='w', padx=5, pady=5)

        ent_name = tk.Entry(master=frm_info)
        ent_name.grid(column=2, row=1, padx=5, pady=5)
        btn_save = tk.Button(
            master=frm_info,
            text='Save new name',
            command=lambda i=index, n=ent_name: self._nameNode(i, n)).grid(column=4, row=1, padx=5, pady=5)

        frm_info.columnconfigure(5, weight=2)

        frm_info.pack(pady=10, padx=10, expand=True, fill='x')

        self.frm_nodeWindow = tk.Frame(master=self.nodeWindow, relief='sunken',
                                       borderwidth=2,
                                       background='white')
        # Display Network
        self._nodeRepresentation(
            masterFrame=self.frm_nodeWindow, dimensions=(800, 400,), buttons=False, homeNodeIndex=index)

    def _openBlockWindow(self, index):
        self.blockwindow = tk.Toplevel(self.root)
        self.blockwindow.title('Block %s Information' % index)
        self.blockwindow.iconphoto(False, tk.PhotoImage(
            file='Graphics/icon.drawio.png'))
        self.blockwindow.configure(background='white')

        # Frame for top information
        frm_info = tk.Frame(master=self.blockwindow, background='white')

        tk.Label(master=frm_info, text='Block:             ',
                 justify='left', background='white').grid(
            column=0, row=0, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text='Hash:              ',
                 justify='left', background='white').grid(
            column=0, row=1, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text='Merkleroot:        ',
                 justify='left', background='white').grid(
            column=0, row=2, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text='Blockchain version:',
                 justify='left', background='white').grid(
            column=0, row=3, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text='Body size:        ',
                 justify='left', background='white').grid(
            column=0, row=4, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text='Previous hash:        ',
                 justify='left', background='white').grid(
            column=0, row=5, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text='Difficulty:        ',
                 justify='left', background='white').grid(
            column=0, row=6, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text='Nonce:             ',
                 justify='left', background='white').grid(
            column=0, row=7, pady=1, padx=5, sticky='nw')

        tk.Label(master=frm_info, text=index,
                 justify='left', background='white').grid(
            column=1, row=0, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text=self.blocks[index].header.calcHash(),
                 justify='left', background='white').grid(
            column=1, row=1, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text=self.blocks[index].header.merkleroot,
                 justify='left', background='white').grid(
            column=1, row=2, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text=self.blocks[index].header.version,
                 justify='left', background='white').grid(
            column=1, row=3, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text=self.blocks[index].header.bodySize,
                 justify='left', background='white').grid(
            column=1, row=4, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text=self.blocks[index].header.preHash,
                 justify='left', background='white').grid(
            column=1, row=5, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text=self.blocks[index].header.difficulty,
                 justify='left', background='white').grid(
            column=1, row=6, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text=self.blocks[index].header.nonce,
                 justify='left', background='white').grid(
            column=1, row=7, pady=1, padx=5, sticky='nw')

        # Frame for transactions
        frm_trans = tk.Frame(master=self.blockwindow,
                             background='white', relief='sunken')

        tk.Label(master=frm_trans, text='All transactions in block:', font='roboto 12 bold', background='white').grid(
            column=1, row=1, pady=5, padx=5)

        frm_list = tk.Frame(master=frm_trans, background='white')
        scb_vert = tk.Scrollbar(master=frm_list)
        scb_vert.pack(side='right', fill='y')

        lsb_trans = tk.Listbox(
            master=frm_list,
            height=15,
            yscrollcommand=scb_vert.set,
            width=250)

        for transaction in self.blocks[index].body.transactions:
            timestamp = datetime.datetime.fromtimestamp(
                transaction.epochTimestamp).strftime('%d-%m-%Y/%H:%M:%S')
            lsb_trans.insert('end', 'ID: %s, Author: %s, Signed: ["%s"] @%s : With data: %s' %
                             (transaction.productID, transaction.author, transaction.signature, timestamp, transaction.data))

        lsb_trans.pack(fill='both', padx=3, pady=3, side='bottom')
        scb_vert.config(command=lsb_trans.yview)

        frm_list.grid(
            column=1, row=2, pady=5, padx=5, sticky='w')

        frm_info.pack(padx=10, pady=10, expand=True,
                      fill='x', side='top', anchor='nw')

        frm_trans.pack(padx=10, pady=10, expand=True,
                       fill='both', side='bottom', anchor='sw')

    def _openSearchResults(self, entry):
        searchString = entry.get()
        entry.delete(0, len(searchString))

        self.searchWindow = tk.Toplevel(self.root)
        self.searchWindow.title(
            'Search results in blockchain for \'%s\'' % searchString)
        self.searchWindow.iconphoto(False, tk.PhotoImage(
            file='Graphics/icon.drawio.png'))
        self.searchWindow.configure(background='white')

        # How many blocks was found containing SearchString at least once.
        resultBlocks = self._search(searchString)
        noOfBlocks = len(resultBlocks[0])

        # Display search in blocks
        tk.Label(master=self.searchWindow,
                 text='"%s" was found in %s blocks, listed below:' % (
                     searchString, noOfBlocks),
                 font='Roboto 12',
                 background='white',
                 justify='left').grid(row=0, column=0, pady=5, padx=5)

        frm_list_blocks = tk.Frame(
            master=self.searchWindow, background='white')

        lsb_blocks = tk.Listbox(
            master=frm_list_blocks,
            height=15,
            width=50)

        for blockIndex in resultBlocks[0]:
            lsb_blocks.insert('end', 'Block number %s' % (blockIndex))

        lsb_blocks.pack(pady=5, padx=5)

        frm_list_blocks.grid(column=0, row=1, pady=5, padx=5)

        # Display search in nodes
        noOfNodes = len(resultBlocks[1])

        tk.Label(master=self.searchWindow,
                 text='"%s" was found in %s nodes, listed below:' % (
                     searchString, noOfNodes),
                 font='Roboto 12',
                 background='white',
                 justify='left').grid(row=0, column=1, pady=5, padx=5)

        frm_list_nodes = tk.Frame(master=self.searchWindow, background='white')

        lsb_nodes = tk.Listbox(
            master=frm_list_nodes,
            height=15,
            width=50)

        for nodeIndex in resultBlocks[1]:
            lsb_nodes.insert('end', 'Node number %s' % (nodeIndex))

        lsb_nodes.pack(pady=5, padx=5)

        frm_list_nodes.grid(column=1, row=1, pady=5, padx=5)

    def _search(self, searchStr):
        return self._searchBlocks(searchStr), self._searchNodes(searchStr)

    def _searchBlocks(self, searchStr):
        blocksWithResult = []

        for idx, block in enumerate(self.blocks):
            rawData = jsonpickle.encode(block)

            if re.search(searchStr.lower(), rawData.lower()):
                blocksWithResult.append(idx)

        return blocksWithResult

    def _searchNodes(self, searchStr):
        nodesWithResult = []

        for idx, block in enumerate(self.nodeList):
            rawData = jsonpickle.encode(block)

            if re.search(searchStr.lower(), rawData.lower()):
                nodesWithResult.append(idx)

        return nodesWithResult

    def _buildNode(self, canvas, center, height, width, index, ip, name, buttons=True):
        h = height/2
        w = width/2

        cX, cY = center

        tempRect = canvas.create_rectangle(
            cX-w,
            cY-h,
            cX+w,
            cY+h,
            fill='white',
            outline='black'

        )
        canvas.tag_raise(tempRect)

        text = '%s\n\n%s' % (name, ip)

        tempText = canvas.create_text(
            cX,
            cY,
            text=text,
            justify='center',
            font='Roboto 8',
            anchor='s'
        )
        canvas.tag_raise(tempText)

        if buttons:
            btn_temp = tk.Button(
                master=self.frm_nodeRep,
                text='Open Node',
                command=lambda i=index: self._openNodeWindow(i),
                background='white',
            )

            tempBtn = canvas.create_window(
                (cX, cY+h-3),
                window=btn_temp,
                anchor='s'
            )
            canvas.tag_raise(tempBtn)

    def _buildRemoteNode(self, canvas, index, buildpos, hostaddress, height, width, global_center, buttons, name):
        start = global_center

        # End is calculated as the middle of the remote node being build
        match buildpos:
            case 0:
                end = (global_center[0], global_center[1])
            case 1:
                end = (global_center[0], global_center[1]-(height*1.5))
            case 2:
                end = (global_center[0]+(width*2),
                       global_center[1]-(height*1.5))
            case 3:
                end = (global_center[0]+(width*4),
                       global_center[1]-(height*1.5))
            case 4:
                end = (global_center[0]+(width*6),
                       global_center[1]-(height*1.5))
            case 5:
                end = (global_center[0]+(width*6), global_center[1])
            case 6:
                end = (global_center[0]+(width*6),
                       global_center[1]+(height*1.5))
            case 7:
                end = (global_center[0]+(width*4),
                       global_center[1]+(height*1.5))
            case 8:
                end = (global_center[0]+(width*2),
                       global_center[1]+(height*1.5))
            case 9:
                end = (global_center[0], global_center[1]+(height*1.5))
            case 10:
                end = (global_center[0]-(width*2),
                       global_center[1]+(height*1.5))
            case 11:
                end = (global_center[0]-(width*4),
                       global_center[1]+(height*1.5))
            case 12:
                end = (global_center[0]-(width*6),
                       global_center[1]+(height*1.5))
            case 13:
                end = (global_center[0]-(width*6), global_center[1])
            case 14:
                end = (global_center[0]-(width*6),
                       global_center[1]-(height*1.5))
            case 15:
                end = (global_center[0]-(width*4),
                       global_center[1]-(height*1.5))
            case 16:
                end = (global_center[0]-(width*2),
                       global_center[1]-(height*1.5))
            case _:
                end = (100, 100)

        temp_line = canvas.create_line(
            start[0],
            start[1],
            end[0],
            end[1],
            fill='black',
            width=1)
        canvas.tag_lower(temp_line)

        # Width halfhazerdly adjusted to be a bit more....
        self._buildNode(
            canvas,
            end,
            height=height,
            width=width*1.2,
            index=index,
            name=name,
            ip=hostaddress,
            buttons=buttons)

    def _buildNodesWithConnections(self, canvas, height, width, buttons, centerNode):
        center = (width/2, height/2)

        ratioh = height/5

        nodes = copy(self.nodeList)
        if centerNode != 0:
            nodes[0], nodes[centerNode] = nodes[centerNode], nodes[0]

        # Build 5 remote nodes for show
        for index, node in enumerate(nodes):
            self._buildRemoteNode(
                canvas=canvas,
                index=index,
                buildpos=index,
                name=node.name,
                hostaddress=node.ip,
                height=ratioh,
                width=ratioh*0.75,
                global_center=center,
                buttons=buttons)

    def _createBlocks(self, frame, test: bool):
        if test:
            # Input fake data
            for c in range(250):
                frm_Temp = tk.Frame(frame, relief='raised',
                                    borderwidth=1, height=100, width=100)
                temp_hash = hashlib.sha256()
                temp_hash.update(str(c).encode())
                temp_hash = temp_hash.hexdigest()
                tk.Button(
                    master=frm_Temp,
                    text='Block %s\nwith hash:\n%s...' % (
                        c, temp_hash[:8]),
                    image=self.pixelVirtual,
                    anchor='center',
                    width=75,
                    height=125,
                    background='white',
                    compound='c',
                    font='Roboto 9',
                    command=lambda index=c: self._openBlockWindow(index=index)).pack(anchor='center')
                frm_Temp.grid(row=0, column=c, pady=10, padx=10)
        else:
            for idx, block in enumerate(self.blocks):
                frm_Temp = tk.Frame(frame, relief='raised',
                                    borderwidth=1, height=100, width=100)
                temp_hash = block.header.calcHash()
                tk.Button(
                    master=frm_Temp,
                    text='Block %s\nwith hash:\n%s...' % (
                        idx, temp_hash[:8]),
                    image=self.pixelVirtual,
                    anchor='center',
                    width=75,
                    height=125,
                    background='white',
                    compound='c',
                    font='Roboto 9',
                    command=lambda index=idx: self._openBlockWindow(index=index)).pack(anchor='center')
                frm_Temp.grid(row=0, column=idx, pady=10, padx=10)
                pass

    def _setScrollRegion(self, canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _tgbHeader(self):
        self.frm_tgb = tk.Frame(
            master=self.root, relief="flat", background='white')

        # Creating logo on the left
        self.frm_logo = tk.Frame(
            master=self.frm_tgb, background='white')
        self.img_logo = tk.PhotoImage(file='Graphics/icon.drawio.png')
        tk.Label(
            master=self.frm_logo,
            image=self.img_logo,
            height=100,
            width=100,
            background='white').grid(
            column=0, row=1)

        self.lbl_tgb = tk.Label(
            master=self.frm_logo,
            text='The\nGeneral\nBlockchain',
            justify='left',
            font='Roboto 20 bold',
            background='white').grid(column=1, row=1)

        # Creating buttons on the right
        self.frm_buttons = tk.Frame(
            master=self.frm_tgb, background='white')

        self.btn_forceUpdate = tk.Button(
            master=self.frm_buttons,
            text='Force Update',
            font='Roboto 10',
            background='white',
            command=lambda: self._forceUpdate()).grid(row=1, column=1, pady=5, padx=5, sticky='e')
        self.btn_newTransaction = tk.Button(
            master=self.frm_buttons,
            text='New Transactions',
            font='Roboto 10',
            background='white',
            command=lambda: self._openNewTransactionsWindow()).grid(row=2, column=1, pady=5, padx=5, sticky='e')
        self.btn_newTransaction = tk.Button(
            master=self.frm_buttons,
            text='Add New Node',
            font='Roboto 10',
            background='white',
            command=lambda: self._openNewNodeWindow()).grid(row=3, column=1, pady=5, padx=5, sticky='e')

        self.frm_tgb.columnconfigure(1, weight=2)
        self.frm_tgb.columnconfigure(2, weight=2)
        self.frm_tgb.columnconfigure(3, weight=3)

        self.frm_buttons.grid(row=0, column=3, sticky='e')

        self.frm_search = tk.Frame(master=self.frm_tgb, background='white')
        self._searchbar(frame=self.frm_search)
        self.frm_search.grid(row=0, column=2, sticky='s')

        self.frm_logo.grid(row=0, column=1, sticky='w')

        self.frm_tgb.pack(fill="x", padx=10, pady=10, expand=True, side='top')

    def _searchbar(self, frame):

        self.lbl_search = tk.Label(
            master=frame,
            text='Search in all transactions and blocks using regex:',
            anchor='e',
            background='white').pack(padx=5, pady=5)

        self.frm_searchbar = tk.Frame(master=frame, background='white')

        ent_search = tk.Entry(
            master=self.frm_searchbar,
            width=40,
            background='white')
        ent_search.grid(row=0, column=0, padx=5)
        tk.Button(
            master=self.frm_searchbar,
            background='white',
            text='Search',
            command=lambda entry=ent_search: self._openSearchResults(entry=entry)).grid(row=0, column=1)

        self.frm_searchbar.pack()

    # Blockchain representation frame ################################################
    def _blockRepresentation(self, masterFrame):
        self.pixelVirtual = tk.PhotoImage(width=1, height=1)

        self.cvs_blocks = tk.Canvas(master=masterFrame,
                                    background='white', height=150)
        self.frm_blocks = tk.Frame(
            master=self.cvs_blocks, background='white')
        self.scb_hor = tk.Scrollbar(master=masterFrame, orient='horizontal',
                                    command=self.cvs_blocks.xview)
        self.cvs_blocks.configure(xscrollcommand=self.scb_hor.set)

        self.scb_hor.pack(side='bottom', fill='x')
        self.cvs_blocks.pack(fill='x', expand=True)

        self.cvs_blocks.create_window(
            (0, 0), window=self.frm_blocks, anchor='w')

        self.cvs_blocks.bind("<Configure>", lambda event,
                             c=self.cvs_blocks: self._setScrollRegion(c))

        self._createBlocks(self.frm_blocks, test=False)

        masterFrame.pack(padx=10, pady=10, expand=True, fill='x')

    # Master frame

    def _nodeRepresentation(self, masterFrame, dimensions, buttons: bool = True, homeNodeIndex=0):
        w, h = dimensions

        cvs_nodeRep = tk.Canvas(master=masterFrame,
                                height=h,
                                width=w,
                                background='white')

        cvs_nodeRep.pack()

        self._buildNodesWithConnections(
            cvs_nodeRep,
            h,
            w,
            buttons,
            centerNode=homeNodeIndex)

        masterFrame.pack(fill='both',
                              padx=10, pady=10, expand=True, side='bottom')


if __name__ == '__main__':
    # For testing the GUI
    testNodes = [Blockchain.tgbNode('Dairy', '1.1.1.1'),
                 Blockchain.tgbNode('Logistics', '2.2.2.2'),
                 Blockchain.tgbNode('Treatment', '3.3.3.3'),
                 Blockchain.tgbNode('Distribution', '4.4.4.4')]
    testBC = Blockchain(nodeList=testNodes)

    # testBC.addBlock(testBlock)

    root = tk.Tk()
    tester = tgbGUI(root=root, blockchainRef=testBC)
    root.mainloop()
