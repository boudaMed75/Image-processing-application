from PIL import Image
import numpy as np
import math

def minmax(image):
    
    img = np.asanyarray(image)
    b = np.copy(img)

    largeur , hauteur = np.shape(img)

        
    voisin = []
    for x in range(1,largeur-1):
        for y in range(1,hauteur-1):
            voisin = np.array(
                
                    # img[x-1,y-1],img[x-1,y],img[x-1,y+1],
                    # img[x,y-1],img[x,y],img[x,y+1],
                    # img[x+1,y-1],img[x+1,y],img[x+1,y+1]
                    [img[x + i, y + j] for i in range(-1,2) for j in range(-1,2)]
            )
            mini = np.min(voisin)
            maxi = np.max(voisin)
            

            if img[x,y] < mini :
                b[x,y] = mini
            elif img[x,y]:
                b[x,y] = maxi
    return b

    

def Median3(image):
    img = np.asanyarray(image)
    b = np.copy(image)
    largeur , hauteur = np.shape(image)

    voisin = []
    for x in range(1,largeur-1):
        for y in range(1,hauteur-1):
            voisin = np.array(
                
                    # img[x-1,y-1],img[x-1,y],img[x-1,y+1],
                    # img[x,y-1],img[x,y],img[x,y+1],
                    # img[x+1,y-1],img[x+1,y],img[x+1,y+1]
                    [img[x + i, y + j] for i in range(-1,2) for j in range(-1,2)]
            )
            voisin.sort()
            b[x,y] = voisin[4]
    return b


def Median5(image):
    img = np.asanyarray(image)
    b = np.copy(image)
    largeur , hauteur = np.shape(image)

    voisin = []
    for x in range(1,largeur-2):
        for y in range(1,hauteur-2):
            voisin = np.array(
                
                    # img[x-1,y-1],img[x-1,y],img[x-1,y+1],
                    # img[x,y-1],img[x,y],img[x,y+1],
                    # img[x+1,y-1],img[x+1,y],img[x+1,y+1]
                    [img[x + i, y + j] for i in range(-2,3) for j in range(-2,3)]
            )
            voisin.sort()
            b[x,y] = voisin[12]
    return b


def moyenneur3(image,ntf):
    img = np.asanyarray(image)
    b = np.copy(img)
    largeur , hauteur = np.shape(img)

    if ntf==9 :
        n = np.array([
            [1,1,1],
            [1,1,1],
            [1,1,1]
        ])
    elif ntf==5 :
        n = np.array([
            [0,1,0],
            [1,1,1],
            [0,1,0]
        ])
    elif ntf==4 :
        n = np.array([
            [0,1,0],
            [1,0,1],
            [0,1,0]
        ])
    for x in range(largeur - 1):
        for y in range(hauteur - 1):
            b[x,y] = 1/ntf * (
                img[x-1,y-1]*n[0,0] + img[x-1,y] * n[0,1] + img[x-1,y+1]*n[0,2]+
                img[x,y-1]*n[1,0] + img[x,y] * n[1,1] + img[x,y+1]*n[1,2]+
                img[x+1,y-1]*n[2,0] + img[x+1,y] * n[2,1] + img[x+1,y+1]*n[2,2]
                # [img[x + i, y + j] for i in range(-1,2) for j in range(-1,2)]
            )
    return b


def convolution2D(img, h):
    nc, nl = np.shape(img)
    py = int((h.shape[0] - 1) / 2)
    px = int((h.shape[1] - 1) / 2)
    imax = int(nc - px)
    Y = np.zeros_like(img)
    for i in range(px, imax):
        for j in range(py, nl - py):
            somme = 0.0
            for k in range(-px, px + 1):
                for l in range(-py, py + 1):
                    somme += img[j + l][i + k] * h[l + py][k + px]
            Y[j][i] = somme
    return Y
def filtreGaussien(P, sigma):
    h = np.zeros((2 * P + 1, 2 * P + 1))
    som = 0
    for m in range(-P, P + 1):
        for n in range(-P, P + 1):
            h[m + P][n + P] = math.exp(-(n * n + m * m) / (2 * sigma * sigma))
            som += h[m + P][n + P]
    h = h / som
    return h


# def apply_gaussian_filter():
#     global copyimage, undo_stack
#     try:
#         if copyimage is not None:
#             sigma = float(gaussian_entry.get())
#             P = int(sigma * 3)
#             h = filtreGaussien(P, sigma)
#             img_array = np.array(copyimage)
#             filtered_image = convolution2D(img_array, h)
#             copyimage = Image.fromarray(filtered_image.astype('uint8'))
#             update_canvas_out()
#             undo_stack.append(copyimage.copy())  # Add current state to undo stack
#             status_label.config(text=f"Gaussian filter applied successfully")
#         else:
#             status_label.config(text="Error: Load an image first.")
#     except Exception as e:
#         status_label.config(text=f"Error in applying Gaussian filter: {e}")


