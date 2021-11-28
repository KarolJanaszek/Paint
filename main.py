from tkinter import filedialog
from tkinter import *
from tkinter.colorchooser import *
import pyscreenshot as ImageGrab
from PIL import Image


PENCIL, BRUSH, ERASER, LINE, RECTANGLE, OVAL = list(range(6))


class Paint:
    def __init__(self, canvas):
        self.canvas = canvas
        self._tool, self._color, self._width, self._fill, self._obj = \
            None, None, None, None, None
        self.lastX, self.lastY = None, None
        self.canvas.bind('<Button-1>', self.click)
        self.canvas.bind('<B1-Motion>', self.draw)

    def draw(self, event):
        if self._tool is None:
            return
        x, y = self.lastX, self.lastY
        if self._tool in (LINE, RECTANGLE, OVAL):
            self.canvas.coords(self._obj, (x, y, event.x, event.y))
        elif self._tool in (PENCIL, BRUSH, ERASER):
            if self._tool == PENCIL:
                self.canvas.create_line(self.lastX, self.lastY, event.x,
                                        event.y, fill=self._color)
            elif self._tool == BRUSH:
                if self._width is None:
                    x1, y1 = (event.x - 5), (event.y - 5)
                    x2, y2 = (event.x + 5), (event.y + 5)
                else:
                    x1, y1 = (event.x - self._width), (event.y - self._width)
                    x2, y2 = (event.x + self._width), (event.y + self._width)
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=self._color,
                                             outline=self._color)
            elif self._tool == ERASER:
                if self._width is None:
                    x1, y1 = (event.x - 15), (event.y - 15)
                    x2, y2 = (event.x + 15), (event.y + 15)
                else:
                    x1, y1 = (event.x - self._width), (event.y - self._width)
                    x2, y2 = (event.x + self._width), (event.y + self._width)
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill="#ffffff",
                                             outline="#ffffff")
            self.lastX, self.lastY = event.x, event.y


    def click(self, event):
        if self._tool is None:
            return
        if self._color is None:
            self._color = '#000000'
        x, y = event.x, event.y
        if self._tool == LINE:
            self._obj = self.canvas.create_line((x, y, x, y),
                                    fill=self._color, width=self._width)
        elif self._tool == RECTANGLE:
            if self._fill:
                self._obj = self.canvas.create_rectangle((x, y, x, y),
                 outline=self._color, fill=self._color, width=self._width)
            else:
                self._obj = self.canvas.create_rectangle((x, y, x, y),
                                    outline=self._color, width=self._width)
        elif self._tool == OVAL:
            if self._fill:
                self._obj = self.canvas.create_oval((x, y, x, y),
                outline=self._color, fill=self._color, width=self._width)
            else:
                self._obj = self.canvas.create_oval((x, y, x, y),
                                outline=self._color, width=self._width)
        self.lastX, self.lastY = x, y

    def select_tool(self, tool):
        print('Tool', tool)
        self._tool = tool

    def select_color(self, color):
        print('Color', color)
        self._color = color

    def select_width(self, width):
        print('Width', width)
        self._width = width

    def select_fill(self, fill):
        print('Fill', fill)
        self._fill = fill


class Tool:
    def __init__(self, whiteboard, parent=None):
        self.file_to_open = None
        self.custom_color = None
        self._curr_tool = None
        self._curr_color = None
        self._curr_width = None
        self._curr_fill = None

        # TOOL ICONS
        self.pencil = PhotoImage(file="Images/pencil_tool.gif")
        self.brush = PhotoImage(file="Images/brush_tool.gif")
        self.eraser = PhotoImage(file="Images/eraser_tool.gif")
        self.line = PhotoImage(file="Images/line_tool.gif")
        self.rectangle = PhotoImage(file="Images/shape_tool.gif")
        self.oval = PhotoImage(file="Images/oval_tool.gif")

        # COLOR ICONS
        self.black = PhotoImage(file="Images/black.gif")  # 000000
        self.gray = PhotoImage(file="Images/gray.gif")  # 808080
        self.white = PhotoImage(file="Images/white.gif")  # ffffff
        self.red = PhotoImage(file="Images/red.gif")  # ff0000
        self.yellow = PhotoImage(file="Images/yellow.gif")  # ffff00
        self.green = PhotoImage(file="Images/green.gif")  # 00ff00
        self.cyan = PhotoImage(file="Images/cyan.gif")  # 00ffff
        self.blue = PhotoImage(file="Images/blue.gif")  # 0000ff
        self.magenta = PhotoImage(file="Images/magenta.gif")  # ff00ff
        self.brown = PhotoImage(file="Images/brown.gif")  # 883d00
        self.colorwheel = PhotoImage(file="Images/colorwheel.gif")
        self.pick_custom = PhotoImage(file="Images/custom.gif")

        self.one = PhotoImage(file="Images/1.gif")
        self.two = PhotoImage(file="Images/2.gif")
        self.three = PhotoImage(file="Images/3.gif")
        self.four = PhotoImage(file="Images/4.gif")
        self.five = PhotoImage(file="Images/5.gif")
        self.six = PhotoImage(file="Images/6.gif")

        self.stroke = PhotoImage(file="Images/stroke.gif")
        self.fill = PhotoImage(file="Images/fill.gif")

        self.save = PhotoImage(file="Images/save.gif")
        self.clear = PhotoImage(file="Images/clear.gif")
        self.open = PhotoImage(file="Images/open.gif")

        TOOLS = [
            (self.pencil, PENCIL),
            (self.brush, BRUSH),
            (self.eraser, ERASER),
            (self.line, LINE),
            (self.rectangle, RECTANGLE),
            (self.oval, OVAL)
        ]

        COLORS = [
            (self.black, '#000000', 2),
            (self.gray, '#808080', 2),
            (self.white, '#FFFFFF', 2),
            (self.magenta, '#FF00FF', 2),
            (self.brown, '#883d00', 2),
            (self.red, '#FF0000', 1),
            (self.yellow, '#FFFF00', 1),
            (self.green, '#00FF00', 1),
            (self.cyan, '#00FFFF', 1),
            (self.blue, '#0000FF', 1)
        ]

        WIDTH = [
            (self.one, 1),
            (self.two, 3),
            (self.three, 5),
            (self.four, 10),
            (self.five, 20),
            (self.six, 30)
        ]

        FILL = [
            (self.stroke, False),
            (self.fill, True)
        ]

        self.whiteboard = whiteboard
        frame1 = Frame(parent, width=40)
        frame2 = Frame(parent, width=40)
        frame1.pack_propagate(False)
        frame2.pack_propagate(False)

        # ------------------ Ikony ------------------------
        for img, name in TOOLS:
            lbl = Label(frame1, relief='raised', image=img)
            lbl._tool = name
            lbl.bind('<Button-1>', self.update_tool)
            lbl.pack(padx=6, pady=3)

        for img, value in WIDTH:
            lbl = Label(frame2, relief='raised', image=img)
            lbl._width = value
            lbl.bind('<Button-1>', self.update_width)
            lbl.pack(padx=6, pady=3)

        lbl = Label(frame1, relief='raised', image=self.stroke)
        lbl._fill = False
        lbl.bind('<Button-1>', self.update_fill)
        lbl.pack(padx=6, pady=3)
        spacer = Label(frame1)
        spacer.pack(padx=6, pady=3)

        lbl = Label(frame2, relief='raised', image=self.fill)
        lbl._fill = True
        lbl.bind('<Button-1>', self.update_fill)
        lbl.pack(padx=6, pady=3)
        spacer = Label(frame2)
        spacer.pack(padx=6, pady=3)

        lbl = Label(frame1, relief='raised', image=self.colorwheel)
        lbl.bind('<Button-1>', self.pick_color)
        lbl.pack(padx=6, pady=3)

        color_frame = Frame(frame2, height=28, width=37)
        color_frame.pack_propagate(0)
        color_frame.pack(padx=6, pady=3)
        self.custom = Label(color_frame, relief='raised',
                            background=self.custom_color)
        if self.custom_color is None:
            self.custom.configure(image=self.pick_custom)
        self.custom.pack(fill=BOTH, expand=1)

        for img, name, num in COLORS:
            if num == 1:
                lbl = Label(frame1, relief='raised', image=img)
            elif num == 2:
                lbl = Label(frame2, relief='raised', image=img)
            lbl._color = name
            lbl.bind('<Button-1>', self.update_color)
            lbl.pack(padx=6, pady=3)

        spacer = Label(frame1)
        spacer.pack(padx=6, pady=3)

        lbl = Label(frame1, relief='raised', image=self.save)
        lbl.bind('<Button-1>', self.save_file)
        lbl.pack(padx=6, pady=3)

        lbl = Label(frame1, relief='raised', image=self.clear)
        lbl.bind('<Button-1>', self.clear_canvas)
        lbl.pack(padx=6, pady=3)

        spacer = Label(frame2)
        spacer.pack(padx=6, pady=3)

        lbl = Label(frame2, relief='raised', image=self.open)
        lbl.bind('<Button-1>', self.open_file)
        lbl.pack(padx=6, pady=3)

        frame1.pack(side='left', fill='y', expand=True, pady=6)
        frame2.pack(side='left', fill='y', expand=True, pady=6)

    # ----------------------------------------------------------------------

    # Aktualizacja wartosci
    def update_tool(self, event):
        lbl = event.widget
        if self._curr_tool:
            self._curr_tool['relief'] = 'raised'
        lbl['relief'] = 'sunken'
        self._curr_tool = lbl
        self.whiteboard.select_tool(lbl._tool)

    def update_color(self, event):
        lbl = event.widget
        if self._curr_color:
            self._curr_color['relief'] = 'raised'
        lbl['relief'] = 'sunken'
        self._curr_color = lbl
        self.whiteboard.select_color(lbl._color)

    def update_width(self, event):
        lbl = event.widget
        if self._curr_width:
            self._curr_width['relief'] = 'raised'
        lbl['relief'] = 'sunken'
        self._curr_width = lbl
        self.whiteboard.select_width(lbl._width)

    def update_fill(self, event):
        lbl = event.widget
        if self._curr_fill:
            self._curr_fill['relief'] = 'raised'
        lbl['relief'] = 'sunken'
        self._curr_fill = lbl
        self.whiteboard.select_fill(lbl._fill)

    def pick_color(self, event):
        color = askcolor()
        self.whiteboard.select_color(color[1])
        self.custom.configure(background=color[1], relief='sunken', image="")
        self.custom._color = color[1]
        self.custom.bind('<Button-1>', self.update_color)
        self._curr_color = self.custom

    def save_file(self, event):
        filename = filedialog.asksaveasfilename(initialdir="C:/Users/karja/Desktop",
                                                title="Wybierz miejsce zapisu",
                                                filetypes=(("jpeg files", "*.jpeg"), ("png files", "*.png"),
                                                           ("gif files", "*.gif"), ("bmp files", "*.bmp")),
                                                defaultextension="*.jpeg")
        if filename is None:
            return
        x1 = root.winfo_x() + 91
        y1 = root.winfo_y() + 31
        x2 = x1 + root.winfo_width()
        y2 = y1 + root.winfo_height()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save(filename)

    def open_file(self, event):
        pass

    def clear_canvas(self, event):
        canvas.delete("all")


root = Tk()
root.geometry("900x640")
root.resizable(width=False, height=False)
root.title("Paint")

canvas = Canvas(background='white', width=800, height=600)
whiteboard = Paint(canvas)
tool = Tool(whiteboard)
canvas.pack(fill='both', expand=True, padx=6, pady=6)
root.mainloop()
