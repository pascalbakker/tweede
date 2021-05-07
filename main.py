import tkinter as tk
from tkinter import font as tkfont
from PIL import ImageTk, Image
from itertools import cycle
import random
import glob

# GLOBALS
# preset = dict{
#    "scalar": [5,30,60,120,240] # in seconds
#    "class": [[(30,5),(60,3),(1,120)]] # (time in seconds, number of images)
# }

# Main clas for project. Run as gui or command line


class DesktopReference:
    def __init__(self, args): pass

    def runApp(self): pass
    def runCommand(self): pass


class ImageIter:
    def __init__(self, path):
        self._c = glob.glob(path)
        random.shuffle(self._c)
        self._index = -1
        self._history = []

    def next(self):
        self._index += 1
        if self._index >= len(self._c):
            self._index = 0
        item = self._c[self._index]
        if item not in self._history:
            self._history.append(item)
        return item

    def prev(self):
        self._index -= 1
        if self._index < 0:
            self._index = len(self._c)-1
        return self._c[self._index]

    def current(self): return self._c[self._index]
    def reshuffle(self): random.shuffle(self._c)
    def history(self): self._history

    # Resizes image to fit inside window. If image is smaller, then it will not resize
    # olds are the image, news are the window

    def calculate_resize(self, img_h, img_w, win_h, win_w, readjust=0.9):
        maxval = max(img_h, img_w, win_h, win_w)
        if img_h == maxval:
            ratio = win_h / img_h
        elif img_w == maxval:
            ratio = win_w / img_w
        elif win_h == maxval and img_w > win_w:
            ratio = img_h / win_h
        elif win_w == maxval and img_h > win_h:
            ratio = img_w / win_w
        else:
            ratio = 1
        new_pad = 0
        return (int(img_h*ratio-new_pad), int(img_w*ratio-new_pad))

    def image(self, height, width):
        image = Image.open(self.current())
        old_h, old_w = image.size
        newsize = self.calculate_resize(old_h, old_w, height, width)
        return ImageTk.PhotoImage(image.resize(newsize, Image.ANTIALIAS))


# Timer countdown
class Countdown:
    def __init__(self, time):
        self._maxtime = time
        self._curtime = self._maxtime
        self._update_freq = 1000

    def realtime(self): return self._curtime / 1000
    def time(self): return self._curtime

    def reset(self):
        self._curtime = self._maxtime
        return self._curtime

    def dec(self):
        self._curtime -= self._update_freq

# Gui main class


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        # VARIABLEs

        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")

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

    def paths_initalization(self): pass  # create config folder

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def loadStack(self): pass

    def getTime(self): pass


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Variables
        self.images = ['testData/boris.jpg',
                       'testData/women.jpg', 'testData/anime.jpg']
        controller.update()
        height = controller.winfo_height()
        width = controller.winfo_width()

        self.currentPos = 0
        self.controller = controller
        counter = Countdown(5000)
        photo = ImageIter('testData/*.jpg')

        # Widgets
        self.img = photo.image(height, width)
        panel = tk.Label(self, image=self.img)
        back = tk.Button(self, text="<", command=lambda: goBack(None))
        forward = tk.Button(self, text=">", command=lambda: goForward(None))
        timer = tk.Label(self, text=counter.realtime())

        # Packing
        panel.pack(side="top")
        back.pack(side="left")
        forward.pack(side="right")
        timer.pack()

        def update_countdown_label(): timer['text'] = counter.realtime()

        def countdown_timer():
            if counter.time() > 0:
                update_countdown_label()
                counter.dec()
                controller.after(counter._update_freq, countdown_timer)
            else:
                counter.reset()
                goForward(None)
                controller.after(0, countdown_timer)

        # Functions
        def next_image(event=None):
            photo.next()
            new_image = photo.image(height, width)
            panel.configure(image=new_image)
            panel.image = new_image

        def previous_image(event=None):
            photo.prev()
            new_image = photo.image(height, width)
            panel.configure(image=new_image)
            panel.image = new_image

        # Callbacks
        def goForward(event):
            next_image()
            counter.reset()

        def goBack(event):
            previous_image()
            counter.reset()

        # Bindings and calls
        controller.bind("<Right>", goForward)
        controller.bind("<Left>", goBack)
        countdown_timer()
        # controller.after(counter._maxtime,countdown)

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


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
