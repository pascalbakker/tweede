import tkinter as tk
from tkinter import font as tkfont
from PIL import ImageTk, Image
from itertools import cycle
import random
import glob
from datetime import datetime
import argparse


def init_argparse():
    parser = argparse.ArgumentParser(description="Iterator through images")
    parser.add_argument('-p','--paths', type=str, default='.', help="path of images")
    # Aesethetic Arguements
    parser.add_argument('--bg_color', type=str, default='black', help="background color of app")
    parser.add_argument('--fg_color', type=str, default='white', help="foreground color of app")
    parser.add_argument('--global_font', type=str, default='Arial', help="font family of labels")
    parser.add_argument('--timer_font_size', type=int, default=20, help="size of timer")
    parser.add_argument('--show_timer', type=bool, default=True, help="show timer")
    parser.add_argument('--show_arrows', type=bool, default=True, help="show forward and back arrows")
    parser.add_argument('--allow_back', type=bool, default=True, help="disable the ability to view previous images")
    parser.add_argument('--disable_skip', type=bool, default=True, help="disable the ability to skip current image")
    parser.add_argument('--readjust_amount', type=float, default=0.7, help="percent of window size images should be")
    return parser


# GLOBALS
# preset = dict{
#    "scalar": [5,30,60,120,240] # in seconds
#    "class": [[(30,5),(60,3),(1,120)]] # (time in seconds, number of images)
# }
"""
bg_color = "black"
fg_color = "white"
global_font = 'Arial'
timer_font_size = 20
show_timer = True
show_arrows = True
disable_skip = False
disable_skip = False
readjust_amount=0.7 # How much to shrink large photos
"""
# Main clas for project. Run as gui or command line


class DesktopReference:
    def __init__(self, args): pass

    def runApp(self): pass
    def runCommand(self): pass


class ImageIter:
    def __init__(self, path, recursive=False):
        images = path+"/*.jpg"
        self._c = glob.glob(images, recursive=recursive)
        random.shuffle(self._c)
        self._index = -1
        self._history = []

    # Maybe image
    def next(self):
        self._index += 1
        if self._index >= len(self._c):
            self._index = len(self._c) - 1
            return None
            #self._index = 0
        item = self._c[self._index]
        if item not in self._history:
            self._history.append(item)
        return item

    def prev(self):
        self._index -= 1
        if self._index < 0:
            self._index = 0
            #self._index = len(self._c)-1
        return self._c[self._index]

    def current(self): return self._c[self._index]
    def reshuffle(self): random.shuffle(self._c)
    def history(self): self._history

    # Resizes image to fit inside window. If image is smaller, then it will not resize
    # olds are the image, news are the window

    def calculate_resize(self, img_h, img_w, win_h, win_w,readjust_amount):
        maxval = max(img_h, img_w, win_h, win_w)
        if img_h == maxval:
            ratio = (win_h / img_h)
        elif img_w == maxval:
            ratio = win_w / img_w
        elif win_h == maxval and img_w > win_w:
            ratio = img_h / win_h
        elif win_w == maxval and img_h > win_h:
            ratio = img_w / win_w
        else:
            ratio = 1
        new_h = img_h*ratio
        new_w = img_w*ratio
        # if image is still too large
        if new_h/win_h > 0.9 or new_w/win_w > 0.9:
            new_h *= readjust_amount
            new_w *= readjust_amount
        return (int(new_h), int(new_w))

    def image(self, height, width,readjust_amount):
        image = Image.open(self.current())
        old_h, old_w = image.size
        newsize = self.calculate_resize(old_h, old_w, height-200, width,readjust_amount)
        return ImageTk.PhotoImage(image.resize(newsize, Image.ANTIALIAS))


# Timer countdown
class CountdownClock:
    def __init__(self, time):
        self._maxtime = time
        self._curtime = self._maxtime
        self._update_freq = 1000
        self._total_time = 0

    def realtime(self):
        mins, secs = divmod(self._curtime/1000, 60)
        if(mins == 0):
            return '{:01d}:{:02d}'.format(int(mins), int(secs))
        return '{:02d}:{:02d}'.format(int(mins), int(secs))

    def time(self): return self._curtime

    def reset(self):
        self._curtime = self._maxtime
        return self._curtime

    def dec(self):
        self._total_time += self._update_freq
        self._curtime -= self._update_freq

# Gui main class


class SampleApp(tk.Tk):
    def __init__(self,userargs, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        self.title("Reference Desktop")
        self.geometry("1000x1000")
        container.pack(side="bottom", fill="both", expand=True, padx=0, pady=0)


        start_button = tk.Button()
        page_name = StartPage.__name__
        frame = StartPage(userargs=userargs,parent=container, controller=self)
        frame.pack(side="top", fill="both", expand="true")
        """
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.pack()
            #frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        """

    def paths_initalization(self): pass  # create config folder

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def loadStack(self): pass

    def getTime(self): pass


class StartPage(tk.Frame):
    def __init__(self, userargs,parent, controller):
        tk.Frame.__init__(self, parent)
        # Variables
        #self.images = ['testData/boris.jpg', 'testData/women.jpg', 'testData/anime.jpg']

        def getSize():
            controller.update()
            height = controller.winfo_height()-50
            width = controller.winfo_width()
            return height, width

        self.configure(bg=userargs.bg_color)
        self.controller = controller
        counter = CountdownClock(5000)
        photo = ImageIter(userargs.paths)
        self.end_session_bool = False

        # Widgets
        height, width = getSize()
        photo.next()
        self.img = photo.image(height, width,userargs.readjust_amount)

        holderFrame = tk.Frame(controller, bg=userargs.bg_color, pady=0, padx=0)
        gridFrame = tk.Frame(holderFrame, bg=userargs.bg_color, pady=0, padx=0)
        panel = tk.Label(holderFrame, text="", image=self.img,
                         bg=userargs.bg_color, fg=userargs.fg_color)
        timer = tk.Label(gridFrame, text=counter.realtime(), font=(
            userargs.global_font, userargs.timer_font_size), fg=userargs.fg_color, bg=userargs.bg_color, padx=30)
        end = tk.Button(gridFrame, text="End", command=lambda: end_session(), font=(
            userargs.global_font, 10), fg=userargs.fg_color, bg=userargs.bg_color, padx=10, pady=3)

        # Packing
        holderFrame.pack(side="top", pady=0)
        gridFrame.pack(side='top', pady=10)
        panel.pack(side='bottom')
        timer.grid(row=0, column=1)
        end.grid(row=0, column=3, padx=20)
        if(userargs.show_arrows):
            back = tk.Button(gridFrame, text="<", command=lambda: goBack(
                None), bg=userargs.bg_color, fg=userargs.fg_color)
            forward = tk.Button(gridFrame, text=">", command=lambda: goForward(
                None), bg=userargs.bg_color, fg=userargs.fg_color)
            back.grid(row=0, column=0)
            forward.grid(row=0, column=2)

        def showGallery(): pass

        def end_session():
            self.end_session_bool = True
            mins, secs = divmod(counter._total_time/1000, 60)
            num_items = len(photo._history)
            results = 'Thank you! \n You have completed {0} images in {1}m{2}s'.format(
                num_items, int(mins), int(secs))
            panel.configure(image='', text=results,
                            font=(userargs.font, 20))
            panel.update_idletasks()
            timer['text'] = "   "
            photo._c = photo._history
            photo._index = len(photo._c)
            end.grid_forget()

        def update_countdown_label(): timer['text'] = counter.realtime()

        def countdown_timer():
            if self.end_session_bool:
                return
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
            height, width = getSize()
            if photo.next() != None:
                new_image = photo.image(height, width,userargs.readjust_amount)
                panel.configure(image=new_image)
                panel.image = new_image
            else:
                self.end_session_bool = True
                end_session()

        def previous_image(event=None):
            height, width = getSize()
            photo.prev()
            new_image = photo.image(height, width,userargs.readjust_amount)
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

if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()

    app = SampleApp(userargs=args)
    app['bg'] = args.bg_color
    app.mainloop()
