import customtkinter as ctk 
from tkinter import filedialog,Canvas

class Ovrir_Image(ctk.CTkFrame):
    def __init__(self,parent,Importation_une_image):
        super().__init__(master=parent,bg_color='red')
        self.grid(column=0 , columnspan = 2 , row = 0 , sticky = 'nsew')
        self.import_image = Importation_une_image
        ctk.CTkButton(self,text='Ovrir Une Image',command=self.Image_Fenetre).pack(expand=True)
    def Image_Fenetre(self):
        path = filedialog.askopenfile().name
        self.import_image(path)
class Affichae_Image(Canvas):
    def __init__(self,parent,resize_img):
        super().__init__(master=parent,background='red',bd=0,highlightthickness=0,relief='ridge')
        self.grid(row=0,column=1,sticky='nsew',padx=10,pady=10)
        self.bind('<Configure>',resize_img)
class Close_img(ctk.CTkButton):
    def __init__(self,parent,close_func):
        super().__init__(
            master=parent,
            command=close_func,
            text='X',
            fg_color= 'transparent',
            text_color= '#FFF',
            width=40,
            height=40,
            corner_radius=0,
            hover_color= '#8a0606'
            )
        self.place(relx=0.99,rely=0.01,anchor='ne')


