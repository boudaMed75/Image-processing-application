import customtkinter as ctk
from panel import *
from algoritme import *
from PIL import Image

class Menu(ctk.CTkTabview):
    def __init__(self,parent,pos_var,col_var,Effects_var,save_img,median,moyenneur,minmax,goussein,binaraiser_image,conversion_dynamique,histogram):
        super().__init__(master=parent)
        self.grid(row=0,column=0,sticky='nsew',padx=10,pady=10)

        # tabs
        self.add('Position')
        self.add('color')
        self.add('Effects')
        self.add('save')

        # widgets
        PositionFrame(self.tab('Position'),pos_var,binaraiser_image,conversion_dynamique,histogram)
        ColorFrame(self.tab('color'),col_var)
        EffectsFrame(self.tab('Effects'),Effects_var,median,moyenneur,minmax,goussein)
        # ExportFrame(self.tab('Export'))
        Save(self.tab('save'),save_img)

class PositionFrame(ctk.CTkFrame):
    def __init__(self,parent,pos_var,binaraiser_image,conversion_dynamique,histogram):
        super().__init__(master=parent,fg_color='transparent')
        self.pack(expand=True,fill='both')

        self.fleep_option = ['none','y','x','both']

        SliderPanel(self,'Rottation',pos_var['rotate'],0,360)
        SliderPanel(self,'zoom',pos_var['zoom'],0,200)
        ChoisirPanel(self,'invert',pos_var['flip'],self.fleep_option)

        ctk.CTkButton(self,text="binaraiser l'image",command=binaraiser_image).pack()
        ctk.CTkButton(self,text="inverse dynamique d'image",command=conversion_dynamique).pack()
        ctk.CTkButton(self,text="histogram",command=histogram).pack()



class ColorFrame(ctk.CTkFrame):
    def __init__(self,parent,col_var):
        super().__init__(master=parent,fg_color='transparent')
        self.pack(expand=True,fill="both")

        # SwitchPanel(self)

        SliderPanel(self,'balance',col_var['balance'],-20,20)
        SliderPanel(self,'luminosite',col_var['luminosite'],0,2)
        SliderPanel(self,'constraste',col_var['constraste'],-20,20)
        SliderPanel(self,'nettete',col_var['nettete'],-20,20)
        
class EffectsFrame(ctk.CTkFrame):
    def __init__(self,parent,Effects_var,median,moyenneur,minmax,goussein):
        super().__init__(master=parent,fg_color='transparent')
        self.pack(expand=True,fill="both")
        self.effect = ['3X3','5X5']
        self.moyenneur = ['3X3-9','3X3-5','3X3-3']

        self.filter = Effects_var
        
        # minmax
        filter_panel(self,"Filter Min Max",self.filter['minmax'],self.effect)
        ctk.CTkButton(self,text="appliquer filter minmax",command=minmax).pack()

        # median
        filter_panel(self,"Filter Median",Effects_var['median'],self.effect)
        ctk.CTkButton(self,text="appliquer median",command=median).pack()

        # moyenneur
        filter_panel(self,"Filter Moyenneur",Effects_var['moyenneur'],self.moyenneur)
        ctk.CTkButton(self,text="appliquer moyenneur",command=moyenneur).pack()


        ctk.CTkEntry(self,textvariable = Effects_var['gaussien']).pack()
        ctk.CTkButton(self,text="appliquer filter goussien",command=goussein).pack()
    


class ExportFrame(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(master=parent,fg_color='blue')


class Save(ctk.CTkFrame):
    def __init__(self,parent,save_img):
        super().__init__(master=parent,fg_color='transparent')
        self.pack(expand=True,fill="both")

        self.nom = ctk.StringVar()
        self.fichier = ctk.StringVar(value='jpg')
        self.path = ctk.StringVar()

        NomFichier(self,self.nom,self.fichier)
        SelectionnerDossier(self,self.path)
        Sovgarder(self,save_img,self.nom,self.fichier,self.path)

