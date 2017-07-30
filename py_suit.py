from tkinter import *
from tkinter import ttk
import arp_send


def send_button(*args):#Push button event handler
    try:
        Destination_v = arp_send.Tokenizer(Destination.get())
        Source_v = arp_send.Tokenizer(Source.get())
        SenderHA_v = arp_send.Tokenizer(SenderHA.get())
        SenderIP_v = arp_send.Tokenizer(SenderIP.get())
        TargetHA_v = arp_send.Tokenizer(TargetHA.get())
        TargetIP_v = arp_send.Tokenizer(TargetIP.get())
        ARP_OPT_v = ARP_OPT.get()
        DEV_v = Dev_s.get()
        FRAME=arp_send.ARP_Pack(Destination_v,Source_v,ARP_OPT_v,SenderHA_v,SenderIP_v,TargetHA_v,TargetIP_v)
        arp_send.ARP_shoot(FRAME,DEV_v)
    except ValueError:
        pass


OPT=["ARP_REQUST","ARP_REPLY"]
device_list=arp_send.device_get()#Get network device list
root = Tk()
root.title("ARP SENDER")#GUI console Title

if __name__ == "__main__" :
    mainframe = ttk.Frame(root, padding="10 10 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)


    Destination = StringVar()
    Source = StringVar()
    SenderHA = StringVar()
    SenderIP = StringVar()
    TargetHA = StringVar()
    TargetIP = StringVar()
    ARP_OPT = StringVar()
    Dev_s = StringVar()
    
    """Set default value"""
    Dev_s.set(device_list[0])
    ARP_OPT.set("ARP_REQUEST")
    Destination.set(arp_send.DESTINATION)
    Source.set(arp_send.mac_get(device_list[0]))
    SenderIP.set(arp_send.ip_get(device_list[0]))


    """Set child item's layout"""
    Destination_en = ttk.Entry(mainframe, width=20, textvariable=Destination)
    Destination_en.grid(column=2, row=3, sticky=(W, E))
    Source_en = ttk.Entry(mainframe, width=20, textvariable=Source)
    Source_en.grid(column=2, row=4, sticky=(W, E))
    SenderHA_en = ttk.Entry(mainframe, width=20, textvariable=SenderHA)
    SenderHA_en.grid(column=2, row=5, sticky=(W, E))
    SenderIP_en = ttk.Entry(mainframe, width=20, textvariable=SenderIP)
    SenderIP_en.grid(column=2, row=6, sticky=(W, E))
    TargetHA_en = ttk.Entry(mainframe, width=20, textvariable=TargetHA)
    TargetHA_en.grid(column=2, row=7, sticky=(W, E))
    TargetIP_en = ttk.Entry(mainframe, width=20, textvariable=TargetIP)
    TargetIP_en.grid(column=2, row=8, sticky=(W, E))
    ARP_MENU = OptionMenu(mainframe,ARP_OPT,*OPT).grid(column=2,row=2)
    DEV_MENU = OptionMenu(mainframe, Dev_s, *device_list).grid(column=2, row=1)

    """It is just label"""
    ttk.Label(mainframe, text="DEVICE").grid(column=1, row=1, sticky=W)
    ttk.Label(mainframe, text="ARP_OPTION").grid(column=1, row=2, sticky=W)
    ttk.Label(mainframe, text="Destination").grid(column=1, row=3, sticky=W)
    ttk.Label(mainframe, text="Source").grid(column=1, row=4, sticky=W)
    ttk.Label(mainframe, text="SenderHA").grid(column=1, row=5, sticky=W)
    ttk.Label(mainframe, text="SenderIP").grid(column=1, row=6, sticky=W)
    ttk.Label(mainframe, text="TargetHA").grid(column=1, row=7, sticky=W)
    ttk.Label(mainframe, text="TargetIP").grid(column=1, row=8, sticky=W)
    ttk.Button(mainframe, text="Send", command=send_button).grid(column=2, row=9, sticky=W)

    """Give some padding between item and item """
    for child in mainframe.winfo_children(): child.grid_configure(padx=10, pady=10)
    
    """Focused item"""
    Destination_en.focus()

    root.bind('<Return>', send_button)
    root.mainloop()
