import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from PIL import ImageTk, Image


"""
class Photos:
    def __init__(self,paths=[]):
        for path in paths:
"""



class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        # VARIABLEs
        self.iteration_time = 5000 # ms

        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        self.title("Reference Desktop")
        self.geometry("600x600")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def loadStack(): return None

    def getTime(): return None


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.images = ['testData/boris.jpg','testData/women.jpg','testData/anime.jpg']
        self.currentPos = 0
        self.controller = controller
        self.currentCount = int(controller.iteration_time/1000)

        # Widgets
        self.img = self.loadImage()
        panel = tk.Label(self, image=self.img)
        back = tk.Button(self, text="<",command=lambda: previousImage())
        forward = tk.Button(self, text=">",command=lambda: nextImage(dontRun = False))
        timer = tk.Label(self, text=str(controller.iteration_time))

        # Packing
        panel.pack(side="top")
        back.pack(side="left")
        forward.pack(side="right")
        timer.pack()

        def countdown():
            timer['text'] = self.currentCount
            if self.currentCount > 0 :
                self.currentCount -= 1
                controller.after(1000, countdown)
            else:
                self.currentCount = int(controller.iteration_time/1000)
                nextImage()
                controller.after(0, countdown)

        def nextImage(e=None,dontRun=None):
            img2 = self.loadImage()
            panel.configure(image=img2)
            panel.image = img2
            if(e==None and dontRun==None):
                controller.after(controller.iteration_time,nextImage)

        def previousImage(e=None):
            img2 = self.loadImage(-1)
            panel.configure(image=img2)
            panel.image = img2

        countdown()
        #controller.after(controller.iteration_time,nextImage)
        def moveandreset(event):
            nextImage(dontRun=True)
            self.currentCount = int(controller.iteration_time/1000)
            timer['text'] = self.currentCount
        def moveandreset2(event):
            previousImage()
            self.currentCount = int(controller.iteration_time/1000)
            timer['text'] = self.currentCount

        controller.bind("<Return>",moveandreset)
        controller.bind("<Right>",moveandreset)
        controller.bind("<Left>",moveandreset2)



        """
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()
        """
    def loadImage(self, inc=1):
        index = self.currentPos + inc
        pos = index%len(self.images)
        print(pos)
        path = self.images[pos]
        self.currentPos = pos
        return ImageTk.PhotoImage(Image.open(path).resize((600,600)))

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
