import argparse
import glob
import random
import tkinter as tk
from datetime import datetime
from itertools import cycle
from tkinter import font as tkfont

from PIL import Image, ImageTk


def init_argparse():
    # Important
    parser = argparse.ArgumentParser(description="Iterator through images")
    parser.add_argument('-p', '--paths', nargs='+', required=True,
                        default='.', help="path of images")
    parser.add_argument('-r','--recursive',dest='rec', action='store_true')
    parser.add_argument('-t', '--time', type=int,
                        default='30', help="time in seconds")
    parser.add_argument('-q', '--random', dest="random_shuffle", action='store_true', help="Does randomly shuffle images.")
    parser.add_argument('-Q', '--no_random', dest="random_shuffle", action='store_false', help="Does not randomly shuffle images.")
    # Aesethetic Arguements
    parser.add_argument('--bg_color', type=str,
                        default='black', help="background color of app")
    parser.add_argument('--fg_color', type=str,
                        default='white', help="foreground color of app")
    parser.add_argument('--global_font', type=str,
                        default='Arial', help="font family of labels")
    parser.add_argument('--timer_font_size', type=int,
                        default=20, help="size of timer")
    parser.add_argument('--show_timer', type=bool,
                        default=True, help="show timer")
    parser.add_argument('--arrows', dest='show_arrows', action='store_true', help="show forward and back arrows")
    parser.add_argument('--no_arrows', dest='show_arrows', action='store_false', help="show forward and back arrows")
    parser.add_argument('--allow_back', type=bool, default=True,
                        help="disable the ability to view previous images")
    parser.add_argument('--disable_skip', type=bool, default=True,
                        help="disable the ability to skip current image")
    parser.add_argument('--readjust_amount', type=float, default=0.8,
                        help="percent of window size images should be")
    parser.set_defaults(show_arrows=True)
    parser.set_defaults(random_shuffle=True)
    #parser.set_defaults(show_arrows=False)
    return parser

class ImageIter:
    def __init__(self,random_shuffle, paths, recursive=False):
        ext = ['png','jpg']
        self._c = []

        for path in paths:
            results = [glob.glob(path + '/*.' + e,recursive=False) for e in ext]
            for result in results:
                if len(result) > 0:
                    self._c += result
        if(random_shuffle):
            self.reshuffle()
        self._index = -1
        self._history = []

    # Maybe image
    def next(self):
        self._index += 1
        if self._index >= len(self._c):
            self._index = len(self._c) - 1
            return None
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
    
    def nextImage(self): pass
    def current(self): return self._c[self._index]
    def reshuffle(self): random.shuffle(self._c)
    def history(self): self._history

    # Resizes image to fit inside window. If image is smaller, then it will not resize
    # olds are the image, news are the window
    @staticmethod
    def calculate_resize(img_h, img_w, win_h, win_w, readjust_amount):
        new_h = max(win_h*readjust_amount,0)
        new_w = max(win_w*readjust_amount,0)
        ratio = min(new_w/img_w,new_h/img_h)
        return (int(ratio*img_h),int(ratio*img_w))

    """
    def calculate_resize(self, img_h, img_w, win_h, win_w, readjust_amount):
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
        if new_h/win_h > 0.95 or new_w/win_w > 0.95:
            new_h *= readjust_amount
            new_w *= readjust_amount
        return (int(new_h), int(new_w))
        """

    def image(self, height, width, readjust_amount):
        print(self.current())
        image = Image.open(self.current())
        old_h, old_w = image.size
        newsize = self.calculate_resize(
            old_h, old_w, height-200, width, readjust_amount)
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
    def __init__(self, userargs, *args, **kwargs):
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
        frame = StartPage(userargs=userargs, parent=container, controller=self)
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
    def __init__(self, userargs, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg=userargs.bg_color)
        self.controller = controller
        counter = CountdownClock(userargs.time*1000)
        photo = ImageIter(userargs.random_shuffle,userargs.paths)
        self.terminate_clock = False

        # Widgets
        holderFrame = tk.Frame(
            controller, bg=userargs.bg_color, pady=0, padx=0)
        gridFrame = tk.Frame(holderFrame, bg=userargs.bg_color, pady=0, padx=0)
        timer = tk.Label(gridFrame, text=counter.realtime(), font=(
            userargs.global_font, userargs.timer_font_size), fg=userargs.fg_color, bg=userargs.bg_color, padx=30)
        pause = tk.Button(gridFrame, text="End", command=end_session, font=(
            userargs.global_font, 10), fg=userargs.fg_color, bg=userargs.bg_color, padx=10, pady=3)
        end = tk.Button(gridFrame, text="End", command=end_session, font=(
            userargs.global_font, 10), fg=userargs.fg_color, bg=userargs.bg_color, padx=10, pady=3)
        back = tk.Button(gridFrame, text="<", command=goBack, bg=userargs.bg_color, fg=userargs.fg_color)
        forward = tk.Button(gridFrame, text=">", command=goForward, bg=userargs.bg_color, fg=userargs.fg_color)
        # Image widget
        height, width = self.getSize()
        photo.next()
        self.img = photo.image(height, width, userargs.readjust_amount)
        panel = tk.Label(holderFrame, text="", image=self.img,
                         bg=userargs.bg_color, fg=userargs.fg_color)

        # Dispaying Widgets
        holderFrame.pack(side="top", pady=0)
        gridFrame.pack(side='top', pady=10)
        panel.pack(side='bottom')
        timer.grid(row=0, column=1)
        end.grid(row=0, column=3, padx=20)

        if(userargs.show_arrows):
            forward.grid(row=0, column=2)

        def end_session():
            self.terminate_clock = True
            mins, secs = divmod(counter._total_time/1000, 60)
            num_items = len(photo._history)
            results = 'Thank you! \n You have completed {0} images in {1}m{2}s'.format(
                num_items, int(mins), int(secs))
            panel.configure(image='', text=results,
                            font=(userargs.global_font, 20))
            timer['text'] = "   "
            photo._c = photo._history
            photo._index = len(photo._c)
            end.grid_forget()

        def update_countdown_label(): timer['text'] = counter.realtime()

        def countdown_timer():
            if self.terminate_clock:
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
            height, width = self.getSize()
            if photo.next() != None:
                new_image = photo.image(
                    height, width, userargs.readjust_amount)
                panel.configure(image=new_image)
                panel.image = new_image
            else:
                self.terminate_clock = True
                end_session()
                forward.grid_forget()
            if userargs.show_arrows and photo._index > 0:
                back.grid(row=0, column=0)

        def previous_image(event=None):
            height, width = self.getSize()
            photo.prev()
            new_image = photo.image(height, width, userargs.readjust_amount)
            panel.configure(image=new_image)
            panel.image = new_image
            # Display arrows
            if not userargs.show_arrows:
                return
            if photo._index == 0:
                back.grid_forget()
            else:
                forward.grid(row=0, column=2)

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

    def getSize(self):
        self.controller.update()
        height = self.controller.winfo_height()-50
        width = self.controller.winfo_width()
        return height, width


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    app = SampleApp(userargs=args)
    app['bg'] = args.bg_color
    app.mainloop()
