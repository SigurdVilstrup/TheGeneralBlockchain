from copy import copy
from ctypes import alignment
import hashlib
from os import name
import tkinter as tk

from LocalBlockchain import Blockchain


class tgbGUI:
    def __init__(self, root, blockchainRef: Blockchain):
        self.blockchain = blockchainRef
        self.nodeList = [('localhost', 'local node')]
        for node in blockchainRef.nodeList:
            self.nodeList.append((node, 'Unnamed'))

        self.root = root
        self.root.iconphoto(False, tk.PhotoImage(
            file='Graphics/icon.drawio.png'))
        self.root.title('The General Blockchain')
        self.root.geometry('1200x900')
        self.root.configure(background='white')

        self._tgbHeader()
        self._blockRepresentation()

        self.frm_nodeRep = tk.Frame(master=self.root, relief='sunken',
                                    borderwidth=2,
                                    background='white')
        self._nodeRepresentation(
            masterFrame=self.frm_nodeRep, dimensions=(1200, 550))

    def _openNewNodeWindow(self):
        self.newNodeWindow = tk.Toplevel(self.root)
        self.newNodeWindow.title('Add new node')
        self.newNodeWindow.iconphoto(False, tk.PhotoImage(
            file='Graphics/icon.drawio.png'))
        self.newNodeWindow.configure(background='white')

        # Get info: IP, Network, Name, Index

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
        self.nodeList.append((ip.get(), name.get()))

        self._forceUpdateNodes(destroyWindow=self.newNodeWindow)

    def _nameNode(self, nodeIndex, newNameEnt):
        self.nodeList[nodeIndex] = (
            self.nodeList[nodeIndex][0], newNameEnt.get())

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
            text="ip:\t",
            anchor='w',
            background='white').grid(column=0, row=0, sticky='w', padx=5, pady=5)
        lbl_ip = tk.Label(
            master=frm_info,
            text=self.nodeList[index][0],
            justify='left',
            anchor='w',
            background='white').grid(column=1, row=0, sticky='w', padx=5, pady=5)
        tk.Label(
            master=frm_info,
            text="name:\t",
            anchor='w',
            background='white').grid(column=0, row=1, padx=5, pady=5)
        lbl_name = tk.Label(
            master=frm_info,
            text=self.nodeList[index][1],
            justify='left',
            anchor='w',
            background='white').grid(column=1, row=1, padx=5, pady=5)
        ent_name = tk.Entry(master=frm_info)
        ent_name.grid(column=2, row=1, padx=5, pady=5)
        btn_save = tk.Button(
            master=frm_info,
            text='Save new name',
            command=lambda i=index, n=ent_name: self._nameNode(i, n)).grid(column=3, row=1, padx=5, pady=5)

        frm_info.columnconfigure(5, weight=2)

        tk.Button(
            master=frm_info,
            text='OK / CLOSE',
            command=lambda: self.nodeWindow.destroy()).grid(column=5, row=0, pady=10, padx=10, sticky='e')

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
        self.blockwindow.geometry('300x600')
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
        tk.Label(master=frm_info, text='Difficulty:        ',
                 justify='left', background='white').grid(
            column=0, row=4, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text='Nonce:             ',
                 justify='left', background='white').grid(
            column=0, row=5, pady=1, padx=5, sticky='nw')

        tk.Label(master=frm_info, text=index,
                 justify='left', background='white').grid(
            column=1, row=0, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text='',
                 justify='left', background='white').grid(
            column=1, row=1, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text='',
                 justify='left', background='white').grid(
            column=1, row=2, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text='',
                 justify='left', background='white').grid(
            column=1, row=3, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text='',
                 justify='left', background='white').grid(
            column=1, row=4, pady=1, padx=5, sticky='nw')
        tk.Label(master=frm_info, text='',
                 justify='left', background='white').grid(
            column=1, row=5, pady=1, padx=5, sticky='nw')

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
            height=20,
            yscrollcommand=scb_vert.set,
            width=40)

        for line in range(0, 100):
            lsb_trans.insert('end', 'transaction no: %s' % line)

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
        self.searchWindow.geometry('600x300')
        self.searchWindow.configure(background='white')

        # How many blocks was found containing SearchString at leas once.
        noOfBlocks = 10

        tk.Label(master=self.searchWindow,
                 text='%s was found in %s blocks, listed below:' % (
                     searchString, noOfBlocks),
                 font='Roboto 12',
                 background='white',
                 justify='left').pack(side='top', anchor='nw', pady=5, padx=5)

        # TODO show way of showing results of searchString
        # Note: probably for all blocks (re.search(searchString) - if not null, string is present in block, return list of blocks and show their hash and index)

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
                name=node[1],
                hostaddress=node[0],
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
            blocks = self.blockchain.blocks
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
            background='white').grid(row=1, column=1, pady=5, padx=5, sticky='e')
        self.btn_newTransaction = tk.Button(
            master=self.frm_buttons,
            text='New Transaction',
            font='Roboto 10',
            background='white',).grid(row=2, column=1, pady=5, padx=5, sticky='e')
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
    def _blockRepresentation(self):
        self.pixelVirtual = tk.PhotoImage(width=1, height=1)

        self.frm_bcRep = tk.Frame(master=self.root, relief='sunken',
                                  borderwidth=2, background='white')

        self.cvs_blocks = tk.Canvas(master=self.frm_bcRep,
                                    background='white', height=150)
        self.frm_blocks = tk.Frame(
            master=self.cvs_blocks, background='white')
        self.scb_hor = tk.Scrollbar(master=self.frm_bcRep, orient='horizontal',
                                    command=self.cvs_blocks.xview)
        self.cvs_blocks.configure(xscrollcommand=self.scb_hor.set)

        self.scb_hor.pack(side='bottom', fill='x')
        self.cvs_blocks.pack(fill='x', expand=True)

        self.cvs_blocks.create_window(
            (0, 0), window=self.frm_blocks, anchor='w')

        self.cvs_blocks.bind("<Configure>", lambda event,
                             c=self.cvs_blocks: self._setScrollRegion(c))

        self._createBlocks(self.frm_blocks, test=False)
        self.frm_bcRep.pack(padx=10, pady=10, expand=True, fill='x')

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
    testNodes = ['1.1.1.1', 'Sigurd', 'Lars']
    testBC = Blockchain(nodeList=testNodes)

    root = tk.Tk()
    tester = tgbGUI(root=root, blockchainRef=testBC)
    root.mainloop()
