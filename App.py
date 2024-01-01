import customtkinter as ctk 

from image_widgets import *
from PIL import Image,ImageTk,ImageOps
from menu import Menu
from PIL import ImageEnhance
from algoritme import *
import matplotlib.pyplot as plt
import shutil
import numpy as np




class App(ctk.CTk):
    def __init__(self):
        # setup
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.geometry('1000x600+100+50')
        self.title('Bouda Mohamed Project multimedia')
        self.minsize(700,400)

        self.flip_option = ['None','X','Y','Both']

        self.init_parametres()

        # Layout
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=2,uniform='a')
        self.columnconfigure(1,weight=6,uniform='a')

        # canvas data
        self.img_width = 0
        self.img_height = 0
        self.canvas_width = 0
        self.canvas_height = 0
        
        

        # widgets
        self.Ovrir_Image = Ovrir_Image(self,self.Importation_une_image)
        

        # run 
        self.mainloop()
    def init_parametres(self):

        self.pos_vars = {
            'rotate' : ctk.DoubleVar(value = 0),
            'zoom' : ctk.DoubleVar(value = 0),
            'flip' : ctk.StringVar(value = "none")
        }
        self.colors_vars = {
            'balance' : ctk.DoubleVar(value= 1),
            'luminosite' : ctk.DoubleVar(value= 1),
            'constraste' : ctk.DoubleVar(value= 1),
            'nettete' : ctk.DoubleVar(value= 1)
        }
        self.Filter = {
            'minmax' : ctk.StringVar(value='none'),
            'moyenneur' : ctk.StringVar(value='none'),
            'median' :ctk.StringVar(value='none') ,
            'gaussien' : ctk.StringVar(value=1),
        }

        # tracing
        fenetrer_var = list(self.pos_vars.values()) + list(self.colors_vars.values()) + list(self.Filter.values())
        # print(self.pos_vars.values())
        for item in fenetrer_var :

            # print(item.get())
            item.trace("w",self.manipilate_image)



    def manipilate_image(self,*args):
        self.img = self.original_img

        # rotate
        
        self.img = self.img.rotate(self.pos_vars['rotate'].get())
        self.img = ImageOps.crop(self.img,border=self.pos_vars['zoom'].get())
        
                
                
        balance = ImageEnhance.Color(self.img)
        self.img = balance.enhance(self.colors_vars['balance'].get())
        # colo.show()
        # # Question b

        luminosite = ImageEnhance.Brightness(self.img)
        self.img = luminosite.enhance(self.colors_vars['luminosite'].get())
        # colo1.show()
        # # Question c

        contrast = ImageEnhance.Contrast(self.img)
        self.img = contrast.enhance(self.colors_vars['constraste'].get())
        # colo2.show()
        # # Question d

        nettete = ImageEnhance.Sharpness(self.img)
        self.img = nettete.enhance(self.colors_vars['nettete'].get())
        # colo3.show()

        if self.pos_vars['flip'].get() == "x" :
            self.img = ImageOps.mirror(self.img)
        if self.pos_vars['flip'].get() == "y" :
            self.img = ImageOps.flip(self.img)
        if self.pos_vars['flip'].get() == "both" :
            self.img = ImageOps.mirror(self.img)
            self.img = ImageOps.flip(self.img)


        # les filter

        # match self.Filter['minmax'].get() :
        #     case '3X3' : self.img = Image.fromarray(minmax(self.img))
        #     case '5X5' : self.img = Image.fromarray(minmax(self.img))

        # match self.Filter['median'].get():
        #     case '3X3' : self.img = Image.fromarray(Median3(self.img))
        #     case '5X5' : self.img = Image.fromarray(Median5(self.img))

        # match self.Filter['moyenneur'].get():
        #     case '3X3-9' : self.img = Image.fromarray(moyenneur3(self.img,9))
        #     case '3X3-5' : self.img = Image.fromarray(moyenneur3(self.img,5))
        #     case '3X3-4' : self.img = Image.fromarray(moyenneur3(self.img,4))
            


        self.place_img()


    def Importation_une_image(self,path):
        self.original_img = Image.open(path)
        self.img = self.original_img
        self.img_ratio = self.img.size[0] / self.img.size[1] 
        
        self.imgTk = ImageTk.PhotoImage(self.img)


        self.Ovrir_Image.grid_forget()
        self.affiche_iamge = Affichae_Image(self,self.resize_img)
        self.suprimer = Close_img(self,self.close_edit)
        self.menu = Menu(self,self.pos_vars,self.colors_vars,self.Filter,self.Save_img,self.median,self.moyenneur,self.minmax,self.goussein,self.binaraiser_image,self.conversion_dynamique,self.histogram)
    def close_edit(self):
        self.affiche_iamge.grid_forget()
        self.suprimer.place_forget()
        self.menu.grid_forget()

        self.Ovrir_Image = Ovrir_Image(self,self.Importation_une_image)
    def median(self):
        self.img = self.original_img

        match self.Filter['median'].get():
            case '3X3' : self.img = Image.fromarray(Median3(self.img))
            case '5X5' : self.img = Image.fromarray(Median5(self.img))
        

        self.place_img()
    def moyenneur(self):
        self.img = self.original_img
        match self.Filter['moyenneur'].get():
            case '3X3-9' : self.img = Image.fromarray(moyenneur3(self.img,9))
            case '3X3-5' : self.img = Image.fromarray(moyenneur3(self.img,5))
            case '3X3-4' : self.img = Image.fromarray(moyenneur3(self.img,4))
        self.place_img()

    def minmax(self):
        self.img = self.original_img
        match self.Filter['minmax'].get() :
            case '3X3' : self.img = Image.fromarray(minmax(self.img))
            case '5X5' : self.img = Image.fromarray(minmax(self.img))
        self.place_img()
    def goussein(self):
        self.img = self.original_img
        sigma = float(self.Filter['gaussien'].get())
        P = int(sigma * 3)
        h = filtreGaussien(P, sigma)
        img_array = np.array(self.img)
        filtered_image = convolution2D(img_array, h)
        self.img = Image.fromarray(filtered_image.astype('uint8'))

        self.place_img()
    def binaraiser_image(self):
        self.img = self.original_img
        self.convert('L')

        
        seuil = 128 
        self.img = self.img.point(lambda p: p > seuil and 255)

        self.place_img()
    def conversion_dynamique(self):
        self.img = self.original_img
        largeur, hauteur = self.img.size
        inverted_img_rgb = Image.new("RGB", (largeur, hauteur))
        inverted_img_ng = Image.new("L", (largeur, hauteur))

        for y in range(hauteur):
            for x in range(largeur):
                if self.img.mode == "L":
                    l = self.img.getpixel((x, y))
                    inverted_img_ng.putpixel((x, y), (255 - l))
                else:
                    r, v, b = self.img.getpixel((x, y))
                    inverted_r = 255 - r
                    inverted_v = 255 - v
                    inverted_b = 255 - b
                    inverted_img_rgb.putpixel((x, y), (inverted_r, inverted_v, inverted_b))

        self.img = inverted_img_rgb if self.img.mode != "L" else inverted_img_ng

        self.place_img()
    def histogram(self):
        self.img = self.original_img
        largeur, hauteur = self.img.size
        if self.img.mode == "RGBA" or self.img.mode == "RGB":
            # Convert RGBA to RGB
            copyimage_rgb = self.img.convert("RGB")
            copyimage_l = self.img.convert("L")
            histogram = [0] * 256
            r_channel, g_channel, b_channel = copyimage_rgb.split()
            r_histogram = [0] * 256
            g_histogram = [0] * 256
            b_histogram = [0] * 256
            for x in range(largeur):
                for y in range(hauteur):
                    pixel_value = copyimage_l.getpixel((x, y))
                    r_value = r_channel.getpixel((x, y))
                    g_value = g_channel.getpixel((x, y))
                    b_value = b_channel.getpixel((x, y))
                    histogram[pixel_value] += 1
                    r_histogram[r_value] += 1
                    g_histogram[g_value] += 1
                    b_histogram[b_value] += 1

            plt.figure(figsize=(12, 6))
            plt.subplot(231)
            plt.title('Niveau de Grie Channel Histogram')
            plt.xlabel('Pixel Value')
            plt.ylabel('Frequency')
            plt.xlim(0, 255)
            plt.grid()
            plt.bar(range(len(histogram)), histogram, color='gray')
            
            # red Channel Histogram
            plt.subplot(232)
            plt.title('Red Channel Histogram')
            plt.xlabel('Pixel Value')
            plt.ylabel('Frequency')
            plt.xlim(0, 255)
            plt.grid()
            plt.bar(range(len(r_histogram)), r_histogram, color='red')

            # Green Channel Histogram
            plt.subplot(233)
            plt.title('Green Channel Histogram')
            plt.xlabel('Pixel Value')
            plt.ylabel('Frequency')
            plt.xlim(0, 255)
            plt.grid()
            plt.bar(range(len(g_histogram)), g_histogram, color='green')

            # Blue Channel Histogram
            plt.subplot(234)
            plt.title('Blue Channel Histogram')
            plt.xlabel('Pixel Value')
            plt.ylabel('Frequency')
            plt.xlim(0, 255)
            plt.grid()
            plt.bar(range(len(b_histogram)), b_histogram, color='blue')
            plt.tight_layout()
            plt.show()

        elif self.img.mode == "LA" or self.img.mode == "L":
            # Convert LA to L
            copyimage_l= self.img.convert("L")
            histogram = [0] * 256
            for x in range(largeur):
                for y in range(hauteur):
                    pixel_value = copyimage_l.getpixel((x, y))
                    histogram[pixel_value] += 1
            plt.figure(figsize=(12, 6))
            plt.subplot(231)
            plt.title('Niveau de Grie Channel Histogram')
            plt.xlabel('Pixel Value')
            plt.ylabel('Frequency')
            plt.xlim(0, 255)
            plt.grid()
            plt.bar(range(len(histogram)), histogram, color='gray')
            plt.tight_layout()
            plt.show()
    






        
        
    def resize_img(self,event):

        # curent cnavs ratio
        demo_ratio = event.width / event.height

        # update canvas att

        self.canvas_width = event.width
        self.canvas_height = event.height

        # resizing
        if demo_ratio > self.img_ratio:
            self.img_height = int(event.height)
            self.img_width = int(self.img_height * self.img_ratio)
        else:
            self.img_width = int(event.width)
            self.img_height = int(self.img_width / self.img_ratio)
        self.place_img()
    def place_img(self):
        self.affiche_iamge.delete('all')
        img_resize = self.img.resize((self.img_width,self.img_height))
        self.imgTk = ImageTk.PhotoImage(img_resize)
        self.affiche_iamge.create_image(self.canvas_width/2,self.canvas_height/2,image = self.imgTk)

    def Save_img(self,nom,fichier,path) :
        img_final = f"{path}/{nom}.{fichier}"
        self.img.save(img_final)
    

App()
