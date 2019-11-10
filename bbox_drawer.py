import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import pandas as pd



class Bounder(tk.Tk):
    def __init__(self, images_path, output_path, output_name):
        self.images_path = None
        self.path_to_bbox = os.getcwd()
        self.output_name = '/bbox_coords.pkl'
        self.image_indexer = 0
        self.scaledBbox = [None, None, None, None]
        

        
        self.canvas_width = 750
        self.canvas_height = 600
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.bbox_height = None
        self.bbox_width = None
        self.bbox = None
        self.drawing = False
        self.im = None
        self.scaled_im = None
        self.im_height = None
        self.im_width = None
        self.aspect_ratio = None
        self.scaled_im_height = 300
        self.scaled_im_width = None
        
        self.current_image_obj = None
        
        
        
        tk.Tk.__init__(self)
        self.w = tk.Canvas(self, 
                   width=self.canvas_width, 
                   height=self.canvas_height)
        self.w.pack(expand = tk.YES, fill = tk.BOTH)
        
        self.w.bind( "<B1-Motion>", self.startRect)
        self.w.bind( "<ButtonRelease-1>", self.setRect)
        nextImageBut = tk.Button(self, text = "Next Image", command = self.nextImage, anchor = "s", bg='#388E8E')
        nextImageBut.configure(width = 15, activebackground = "#D1EEEE", relief = tk.FLAT)
        nextImageBut = self.w.create_window(self.canvas_height/2+70, self.canvas_height/2+self.scaled_im_height/2+20, anchor="nw", window=nextImageBut)
        
        prevImageBut = tk.Button(self, text = "Previous Image", command = self.prevImage, anchor = "s", bg='#388E8E')
        prevImageBut.configure(width = 15, activebackground = "#D1EEEE", relief = tk.FLAT)
        prevImageBut = self.w.create_window(self.canvas_height/2-70, self.canvas_height/2+self.scaled_im_height/2+20, anchor="nw", window=prevImageBut)
        
        browseInputBut = tk.Button(self, text = "Directory With Images", command = self.browseInput, anchor = "s", bg='#388E8E')
        browseInputBut.configure(width = 20, activebackground = "#D1EEEE", relief = tk.FLAT)
        browseInputBut = self.w.create_window(10, 95, anchor="nw", window=browseInputBut)
        
        browseOutputBut = tk.Button(self, text = "Output bbox Coords", command = self.browseOutput, anchor = "s", bg='#388E8E')
        browseOutputBut.configure(width = 20, activebackground = "#D1EEEE", relief = tk.FLAT)
        browseOutputBut = self.w.create_window(10, 135, anchor="nw", window=browseOutputBut)
        
        saveBut = tk.Button(self, text = "Save Coords", command = self.save, anchor = "s", bg='#388E8E')
        saveBut.configure(width = 10, activebackground = "#D1EEEE", relief = tk.FLAT)
        saveBut = self.w.create_window(10, 185, anchor="nw", window=saveBut)
        

    def browseInput(self):
        self.images_path =  tk.filedialog.askdirectory(initialdir = "/",title = "Images Directory")
        self.image_names = self.getImageIndexes()
        self.bbox_coords = self.startBbox()
        self.current_image_name = self.image_names[self.image_indexer]
        self.readImage(os.path.join(self.images_path, self.current_image_name))
        
        
    def browseOutput(self):
        self.path_to_bbox = tk.filedialog.askdirectory(initialdir = "/",title = "Output Directory")
    
        
                    
    def readImage(self, path):
        self.im = Image.open(path)
        self.im_width, self.im_height = self.im.size
        self.setScales(self.im_height, self.im_width)
        self.tk_im = ImageTk.PhotoImage(self.scaled_im)
        self.current_image_obj = self.w.create_image(self.canvas_width/2, self.canvas_height/2, anchor="center",image=self.tk_im)

    def setScales(self, h, w):
        self.aspect_ratio = w/h
        self.scaled_im_width = int(self.scaled_im_height*self.aspect_ratio)
        self.scaled_im = self.im.resize((self.scaled_im_width, self.scaled_im_height), Image.ANTIALIAS)
        print("Height "+str(h))
        print("Width "+str(w))
        print(self.scaled_im.size)
    
    # Issues: startlocations  are skewed when began out of the image
    # Issues: need to check width , height + x, y to make sure box does not extend out
    # Issues: Not start at 1st image
    def startRect(self, event):
        if self.drawing == False:
            if event.x < self.canvas_width/2 - self.scaled_im_width/2:
                self.x0 = self.canvas_width/2 - self.scaled_im_width/2
            elif event.x > self.canvas_width/2 + self.scaled_im_width/2:
                self.x0 = self.canvas_width/2 + self.scaled_im_width/2
            else:
                self.x0 = event.x
            
            if event.y < self.canvas_height/2 - self.scaled_im_height/2:
                self.y0 = self.canvas_height/2 - self.scaled_im_height/2
            elif event.y > self.canvas_height/2 + self.scaled_im_height/2:
                self.y0 = self.canvas_height/2 + self.scaled_im_height/2
            else:            
                self.y0 = event.y
            self.drawing = True
        
        if self.drawing == True:   
            self.w.delete(self.bbox)
            self.bbox = self.getRect(event.x, event.y)

        
    def setRect(self, event):        
        if self.drawing == True:
            self.drawing = False
            print('set!')
            print("x: " + str(self.x0))
            print("y: " + str(self.y0))
            print("Width: " + str(abs(self.x0 - event.x)))
            print("Height: " + str(abs(self.y0 - event.y)))
            self.x1 = event.x
            self.y1 = event.y
            self.w.delete(self.bbox)
            self.bbox = self.getRect(event.x, event.y)
            self.setImageLoc()
            
            
            #------------ Temporary
            '''
            print("Scalled BBOX: "+str(self.scaledBbox))
            fig = plt.imshow(self.im)
            ax = plt.gca()
            ax.add_patch(patches.Rectangle((self.scaledBbox[0], self.scaledBbox[1]), self.scaledBbox[2], self.scaledBbox[3], edgecolor='#ff0000', linewidth=2, fill=False))
            plt.show()
            '''
            
    def checkStartLocation(self, x0, y0):
        if (self.canvas_width/2) - (self.scaled_im_width/2)<x0<(self.canvas_width/2) + (self.scaled_im_width/2):
            if (self.canvas_height/2) - (self.scaled_im_height/2) <y0<(self.canvas_height/2) +(self.scaled_im_height/2):
                return True
        return False
    
    def getRect(self, x1, y1):
        if x1 > (self.canvas_width/2) + (self.scaled_im_width/2):
            x1 = (self.canvas_width/2) + (self.scaled_im_width/2)
        elif x1 < (self.canvas_width/2) - (self.scaled_im_width/2):
            x1 = (self.canvas_width/2) - (self.scaled_im_width/2)
            
        if y1 > (self.canvas_height/2) + (self.scaled_im_height/2):
            y1 = (self.canvas_height/2) + (self.scaled_im_height/2)
        elif y1 < (self.canvas_height/2) - (self.scaled_im_height/2):
            y1 = (self.canvas_height/2) - (self.scaled_im_height/2)
            
        return self.w.create_rectangle(self.x0, self.y0, x1, y1, outline="#ff0000") 
    
    def getImageIndexes(self):
        self.imagesIndex = os.listdir(self.images_path)
        #self.imagesIndex = [i for i in self.imagesIndex if i not in self.bbox['image']]
        return self.imagesIndex
        
    def startBbox(self):
        
        if os.path.exists(self.path_to_bbox+self.output_name):
            self.bbox_coords = pd.read_pickle(self.path_to_bbox+self.output_name)
            for index, im in enumerate(self.image_names):
                if im not in self.bbox_coords.index:
                    self.image_indexer = index
                    print(self.image_indexer)
                    break
                    
        else:
            columns = ['x0', 'y0', 'width', 'height']
            self.bbox_coords = pd.DataFrame(columns=columns)
            self.bbox_coords.index.name = 'image'
        return self.bbox_coords
    
    def setImageLoc(self):
        topy = self.canvas_height/2 - self.scaled_im_height/2
        leftx = self.canvas_width/2 - self.scaled_im_width/2
        rel_x0 = min(self.x0, self.x1) - leftx
        rel_y0 = min(self.y0, self.y1) - topy
        rel_width = max(self.x0, self.x1) - min(self.x0, self.x1)
        rel_height = max(self.y0, self.y1) - min(self.y0, self.y1)
        if rel_x0 < 0:
            rel_width = rel_width + rel_x0
            rel_x0 = 0
        if rel_y0 < 0:
            rel_height = rel_height + rel_y0
            rel_y0 = 0
        
        self.scaledBbox = self.scaleBbox(rel_x0, rel_y0, rel_width, rel_height)
        
        
    
    def scaleBbox(self, rel_x, rel_y, rel_width, rel_height):
        scaleX = (self.im_width / self.scaled_im_width)
        scaleY = (self.im_height / self.scaled_im_height)
        x = scaleX * rel_x
        y = scaleY * rel_y 
        width = scaleX * rel_width
        height = scaleY * rel_height
        return (x, y, width, height)
    
    def nextImage(self):
        self.w.delete(self.bbox)
        if self.images_path == None:
            print('Browse to image directory!')
        else:
            row = [self.scaledBbox[0],
                   self.scaledBbox[1],
                   self.scaledBbox[2], 
                   self.scaledBbox[3]
                   ]
            self.bbox_coords.loc[self.current_image_name] = row
            print(self.bbox_coords)
            self.w.delete(self.current_image_obj)
            self.image_indexer += 1
            self.current_image_name = self.image_names[self.image_indexer]
            self.scaledBbox = [None, None, None, None]
            self.readImage(os.path.join(self.images_path, self.current_image_name))
                
    def prevImage(self):
        if self.images_path == None:
            print('Browse to image directory!')
        else:
            row = [self.scaledBbox[0],
                   self.scaledBbox[1],
                   self.scaledBbox[2], 
                   self.scaledBbox[3]
                   ]
            self.bbox_coords.loc[self.current_image_name] = row
            print(self.bbox_coords)
            self.w.delete(self.current_image_obj)
            self.image_indexer -= 1
            self.current_image_name = self.image_names[self.image_indexer]
            self.scaledBbox = [None, None, None, None]
            self.readImage(os.path.join(self.images_path, self.current_image_name))
        

    
    def save(self):
        if self.path_to_bbox == None:
            print('Please select directory to output bbox data!')
        else:
            self.bbox_coords.to_pickle(self.path_to_bbox+ self.output_name)
        
if __name__ == "__main__":
    images_path = r'C:\Users\nedhu\Desktop\test-insta\Empire State Building'
    '''
    import tkinter

    root = tk.Tk()

    def key(event):
        print("pressed"), repr(event.char)

    def callback(event):
        frame.focus_set()
        print("clicked at"), event.x, event.y

    frame = tk.Canvas(root, width=100, height=100)
    frame.bind("<Return>", key)
    frame.bind("<Button-1>", callback)
    frame.pack()

    root.mainloop()
    '''
    app = Bounder(images_path, '', '')
    app.mainloop()
   
        
        
        
        
        
        
        
        
        

