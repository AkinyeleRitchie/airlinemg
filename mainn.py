##
from tkinter import *
root=Tk()
root.geometry("400x200+250+100")
root.configure(bg="#D3D3D3")
#root.resizable(0,0)
root.title("Email login")
lbl=Label(root, text="Registration Form", fg="black", font="sanserif 20", bg="#D3D3D3", underline=1)
lbl.pack()
lbl1=Label(root, text="FirstName:", fg="black", font="sanserif 14", bg="#D3D3D3", underline=1)
lbl1.pack(side=TOP)

ent=Entry(root, width=50)
ent.pack(side=TOP)

lbl2=Label(root, text="LastName:", fg="black", font="sanserif 14", bg="#D3D3D3", underline=1)
lbl2.pack(side=TOP)

ent1=Entry(root, width=50)
ent1.pack(side=TOP)
lbl3=Label(root, text="", fg="black", font="sanserif 14", bg="#D3D3D3", underline=1)
lbl3.pack(side=TOP)
btn=Button(root, text="Send", font="sanserif 10")
btn.pack(side=TOP)

root.mainloop()



