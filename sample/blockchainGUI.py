from ctypes import alignment
import hashlib
import tkinter as tk


# Master frame ################################################
class tgbGUI:
    def __init__(self, root):
        self.root = root
        self.root.iconphoto(False, tk.PhotoImage(
            file='Graphics/icon.drawio.png'))
        self.root.title('The General Blockchain')
        self.root.geometry('1200x900')
        self.root.configure(background='white')

        self._tgbHeader()
        self._blockRepresentation()
        self._nodeRepresentation()

        pass

    def _buildNode(self, canvas, center, height, width, text):
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

        tempText = canvas.create_text(
            cX,
            cY,
            text=text,
            justify='center',
            font='Roboto 8'
        )
        canvas.tag_raise(tempText)

    def _buildRemoteNode(self, canvas, index, hostaddress, height, width, global_center):
        start = global_center

        # End is calculated as the middle of the remote node being build
        match index:
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
                end = (0, 0)

        temp_line = canvas.create_line(
            start[0],
            start[1],
            end[0],
            end[1],
            fill='black',
            width=1)
        canvas.tag_lower(temp_line)

        self._buildNode(
            canvas,
            end,
            height=height,
            width=width,
            text='Index: %s\n\n%s\nremote node' % (index, hostaddress))

        pass

    def _buildNodesWithConnections(self, canvas, height, width):
        center = (width/2, height/2)

        ratioh = height/5

        # Build 5 remote nodes for show
        for index in range(0, 16):
            self._buildRemoteNode(
                canvas=canvas,
                index=index+1,
                hostaddress='192.%s.0.%s' % (index*51.5, index),
                height=ratioh,
                width=ratioh*0.75,
                global_center=center)

        # Building center node (localnode)
        self._buildNode(
            canvas=canvas,
            center=center,
            height=ratioh,
            width=ratioh*0.75,
            text='Index: 0\n\nlocalhost\nlocal node')

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
                    font='Roboto 9').pack(anchor='center')
                frm_Temp.grid(row=0, column=c, pady=10, padx=10)
        else:
            # TODO implement dynamically gettings the blocks from the local blockchain
            pass

    def _setScrollRegion(self, canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _tgbHeader(self):
        self.frm_tgb = tk.Frame(
            master=self.root, relief="flat", background='white')

        # Creating logo on the left
        self.frm_logo = tk.Frame(master=self.frm_tgb, background='white')
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
        self.frm_buttons = tk.Frame(master=self.frm_tgb, background='white')

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
            background='white',).grid(row=3, column=1, pady=5, padx=5, sticky='e')

        self.frm_buttons.pack(side='right')
        self.frm_logo.pack(side='left')

        self.frm_tgb.pack(fill="x", padx=10, pady=10, expand=True, side='top')

    # Blockchain representation frame ################################################

    def _blockRepresentation(self):
        self.pixelVirtual = tk.PhotoImage(width=1, height=1)

        self.frm_bcRep = tk.Frame(master=self.root, relief=tk.SUNKEN,
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

        self._createBlocks(self.frm_blocks, test=True)
        self.frm_bcRep.pack(padx=10, pady=10, expand=True, fill='x')

    # Master frame

    def _nodeRepresentation(self):
        self.frm_nodeRep = tk.Frame(master=self.root,
                                    relief='sunken',
                                    borderwidth=2,
                                    background='white')

        self.cvs_nodeRep = tk.Canvas(master=self.frm_nodeRep,
                                     height=550,
                                     width=1200,
                                     background='white')

        self.cvs_nodeRep.pack()

        self._buildNodesWithConnections(
            self.cvs_nodeRep,
            550,
            1200)

        self.frm_nodeRep.pack(fill='both',
                              padx=10, pady=10, expand=True, side='bottom')


if __name__ == '__main__':
    # For testing the GUI
    root = tk.Tk()
    tester = tgbGUI(root)
    root.mainloop()
