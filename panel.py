
import customtkinter as ctk
from tkinter import filedialog

class Panel(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(master=parent,fg_color='#4a4a4a')
        self.pack(fill='x',padx=4,pady=8)

class SliderPanel(Panel):
    def __init__(self,parent,text,rotate,min_value,max_value):
        super().__init__(parent=parent)

        # layout
        self.rowconfigure((0,1),weight=1)
        self.columnconfigure((0,1),weight=1)

        ctk.CTkLabel(self,text=text).grid(column=0,row=0,sticky='w',padx=5)

        self.num_label = ctk.CTkLabel(self,text= rotate.get())
        
        self.num_label.grid(column=1,row=0,sticky='E',padx=5)

        ctk.CTkSlider(self,
        fg_color='#64686b',
        variable=rotate,
        from_= min_value ,
        to = max_value ,
        command= self.update_value
        ).grid(row=1,column=0,columnspan=2,sticky='ew',padx=5,pady=5)
    def update_value(self,value):
        self.num_label.configure(text=f"{round(value,2)}")


class ChoisirPanel(Panel):
    def __init__(self, parent,text,data_var,option):
        super().__init__(parent=parent)
        ctk.CTkLabel(self,text=text).pack()
        ctk.CTkSegmentedButton(self,variable=data_var,values=option).pack(expand = True,fill='both',pady= 4 , padx=4)
class filter_panel(Panel):
    def __init__(self,parent,text,data_var,option):
        super().__init__(parent=parent)

        # layout
        self.rowconfigure((0,1),weight=1)
        self.columnconfigure((0,1),weight=1)

        ctk.CTkLabel(self,text=text).grid(column=0,row=0,sticky='w',padx=5)

        DropDownPanel(self,data_var,option)

        # ctk.CTkSlider(self,
        # fg_color='#64686b',
        # variable=rotate,
        # from_= min_value ,
        # to = max_value ,
        # command= self.update_value
        # ).grid(row=1,column=0,columnspan=2,sticky='ew',padx=5,pady=5)


class DropDownPanel(ctk.CTkOptionMenu):
    def __init__(self,parent,data_var,option):
        super().__init__(
            master = parent,
            values = option,
            fg_color= 'red',
            variable= data_var
        )
        # self.pack(fill='x',pady=4)
        self.grid(row=1,column=0,columnspan=2,sticky='ew',padx=5,pady=5)


class SwitchPanel(Panel):
    def __init__(self, parent , *args):
        super().__init__(parent= parent)
        for var,text in args :
            switch = ctk.CTkSwitch(self,text=text,variable= var ,button_color="red",fg_color="black" )
            switch.pack(side = 'left', expand = True , fill = "both",padx = 5 ,pady= 5)


class NomFichier(Panel):
    def __init__(self, parent , nom , fichier):
        super().__init__(parent= parent)

        self.nom = nom
        self.nom.trace('w',self.update_text)
        self.fichier = fichier
        self.fichier.trace('w',self.update_text)
        self.extension = ['png','jpg']

        ctk.CTkEntry(self,textvariable=self.nom).pack(fill='x',padx=20,pady=5)
        # DropDownPanel(self,self.fichier,self.extension)
        ctk.CTkOptionMenu(
            master = self,
            values = self.extension,
            fg_color= 'red',
            variable= self.fichier
        ).pack(fill='x',padx=20,pady=5)
        # self.pack(fill='x',pady=4)
        

        self.output = ctk.CTkLabel(self,text='bouda med')
        self.output.pack()
    def update_text(self,*args):
        if self.nom.get() :
            text = self.nom.get().replace(' ','_') + '.'+self.fichier.get()
            self.output.configure(text=text)
        # if self.fichier.get():
        #     print(self.fichier)


class SelectionnerDossier(Panel):
    def __init__(self, parent,path):
        super().__init__(parent = parent)

        self.path = path

        ctk.CTkButton(self,text='selectionner fichier',command=self.ovrir_dossier).pack(pady = 5)
        ctk.CTkEntry(self,textvariable = self.path).pack(expand = True , fill='both', pady = 5 , padx = 5)
    def ovrir_dossier(self) :
        self.path.set(filedialog.askdirectory())

class Sovgarder(ctk.CTkButton):
    def __init__(self,parent,save_img,nom,fichier,path) :
        super().__init__(master = parent , text = 'souvgarder',command = self.save)
        self.pack(side="bottom",pady = 10)

        self.save_img = save_img
        self.nom = nom
        self.fichier = fichier
        self.path = path

    def save(self):
        self.save_img(
            self.nom.get(),
            self.fichier.get(),
            self.path.get()
        )




        





