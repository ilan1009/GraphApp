import matplotlib.pyplot as plt
import sympy
from kivy.core.window import Window
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from numpy import arange as arange
from numpy import linspace as linspace

i = 1
c = 1


def plot(m, b):  # Plot graph using y=mx+b
    # Define new figure
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # match style of other elements
    fig.patch.set_facecolor((0.1289, 0.1289, 0.1289))
    ax.set_facecolor((0.21, 0.21, 0.21))

    # set ticks color
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    x = linspace(-20, 20, 100)  # adjust lin
    y = m * x + b  # ????

    # plot mx + b
    plt.plot(x, y, '-r', '', label='graph')

    # Toggling box aspect
    if c == 1:  # If button is enabled - box aspect on
        ax.set_box_aspect(1)
    else:  # Off
        ax.set_aspect('auto')

    # Labels
    plt.ylabel('y', color='white')
    plt.xlabel('x', color='white')

    # adjust middle line
    ax.axhline(linewidth=1.7, color="white")
    ax.axvline(linewidth=1.7, color="white")

    # Ticks every 1 "?"
    ax.set_xticks(arange(-50, 50, 1))
    ax.set_yticks(arange(-50, 50, 1))

    # size of plot determined by menu
    plt.xlim(lim * -1, lim)
    plt.ylim(lim * -1, lim)

    plt.grid()  # grid

    # Bind ID to graph and add to layout
    graph = FigureCanvasKivyAgg(plt.gcf(), size_hint=(1, 2))
    layout.ids['graph'] = graph
    layout.add_widget(graph)


def formatted(f):  # Function to remove redundant 0's from floats using rstrip
    return float(format(f, '.2f').rstrip('0').rstrip('.'))


class MenuWindow(Screen):  # Manage the main menu screen
    def change_lim(self):  # Change "lim" when exiting the menu
        global lim
        lim = self.ids.slider.value

    def graph_toggle(self):  # ON/OFF function for menu graph button
        global i  # To be used by other classes
        if i == 1:  # When ON turn OFF when pressed
            i = 0
            self.ids.graphbutton.text = 'Graph OFF'
            self.ids.graphbutton.background_color = 1, 0, 0, 1
        else:
            i = 1
            self.ids.graphbutton.text = 'Graph ON'
            self.ids.graphbutton.background_color = 0, 1, 0, 1

    def box_toggle(self):  # ON/OFF function for box aspect button
        global c
        if c == 1:  # When ON turn OFF when pressed
            c = 0
            self.ids.boxbutton.text = 'Keep Box Aspect OFF'
            self.ids.boxbutton.background_color = 1, 0, 0, 1
        else:  # Inverse
            c = 1
            self.ids.boxbutton.text = 'Keep Box Aspect ON'
            self.ids.boxbutton.background_color = 0, 1, 0, 1


class TwoWindow(Screen):  # 2P screen;
    def find2p(self):
        # set global parameters
        global m
        global b
        global bs

        try:

            # set points to text from textinput defined in graph.kv
            point1 = self.ids.pone.text
            point2 = self.ids.ptwo.text

            # Split numbers from input with space
            x1, y1 = point1.split(' ')  # Point 1
            x2, y2 = point2.split(' ')  # ..... 2

            x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)  # Parity

            # Find M from y1, y2, x1, x2
            m1 = y2 - y1
            m2 = x2 - x1

            if m1 and m2 != 0:
                m = m1 / m2
            else:
                m = 0

            # Find B
            b = sympy.symbols('b')

            b_out = (sympy.solve(y1 - x1 * m + b))  # Solve equation

            b_out[0] *= -1

            b = float(b_out[0])  # Init B

            # Print to console ; not visible!
            print(f"m = {m}, b = {b}")

            if b >= 0:
                bs = f'+{b}'
            else:
                bs = b

            # Over to the next screen
            ResultWindow().displayresult()

            # If graphing is on, plot mx + b
            if i == 1:
                plot(m, b)

        except ValueError:
            print('VALUE ERROR')
            ErrorWindow().display('VALUE ERROR\n'
                                  'You have inputted the two integers incorrectly')


class OneWindow(Screen):
    def find1p(self):
        """
        I don't want to comment this
        this is the exact same thing except that M is already known
        fuck off now
        """

        global m
        global b
        global bs

        try:
            point1 = self.ids.pone.text

            m = float(self.ids.mvalue.text)

            x1, y1 = point1.split(' ')

            x1, y1 = float(x1), float(y1)

            b = sympy.symbols('b')

            b_out = (sympy.solve(y1 - x1 * m + b))

            b_out[0] *= -1

            b = float(b_out[0])

            print(f"m = {m}, b = {b}")  # Debug to console

            if b >= 0:
                bs = f'+{b}'
            else:
                bs = b

            ResultWindow().displayresult()  # Send data
            if i == 1:
                plot(m, b)
        except:
            print('VALUE ERROR')
            ErrorWindow().display('VALUE ERROR\n'
                                  'You have inputted the two integers incorrectly')


class GraphWindow(Screen):  # Graph with m and b known;
    def graph(self):
        # set global parameters
        global m
        global b
        global bs

        try:

            # Init M and B through textinput;
            m = int(self.ids.mvalue.text)
            b = int(self.ids.bvalue.text)
            # init b sign
            if b >= 0:
                bs = f'+{b}'
            else:
                bs = b

            ResultWindow().displayresult()  # On to the next screen

            # Plot if graphing on
            if i == 1:
                plot(m, b)

        except:
            print('VALUE ERROR')
            ErrorWindow().display('VALUE ERROR\n'
                                  'You have inputted the two integers incorrectly')


class ResultWindow(Screen):
    def displayresult(self):  # result window
        global layout
        global table

        out = f"out: \n y = {m}x{bs}"  # Out string

        app = MDApp.get_running_app()  # init

        screen = app.root.get_screen("result")  # Move over to the screen

        # Show equation function
        displayname = screen.ids.out_func
        displayname.text = out

        # Make layout
        layout = screen.ids.lay

        # Init our table - this was done manually ; can be more efficient
        table = MDDataTable(column_data=[
            ("Y", dp(25)),
            ("-2", dp(25)),
            ("-1", dp(25)),
            ("0", dp(25)),
            ("1", dp(25)),
            ("2", dp(25)),
            ("3", dp(25)),
            ("4", dp(25)),
            ("5", dp(25)),
        ],
            row_data=[
                ("X", (m * -2) + b, (m * -1) + b, (m * 0) + b, (m * 1) + b, (m * 2) + b, (m * 3) + b, (m * 4) + b,
                 (m * 5) + b)
            ]
        )

        # add widget
        layout.ids['table'] = table
        layout.add_widget(table)

    def back(self):  # Back button
        # Remove old widget
        try:
            layout.remove_widget(layout.ids.graph)
            layout.remove_widget(layout.ids.table)

        except NameError:
            print("nameerror")


class ErrorWindow(Screen):
    def display(self, etext):
        # screen = app.root.get_screen("error")  # Move over to the screen

        errorlabel = self.ids.errorvalue
        errorlabel.text = "Error"


class WindowManager(ScreenManager):  # Screen manager
    pass


kv = Builder.load_file('graph.kv')


class graphApp(MDApp):  # App settings
    def build(self):
        self.theme_cls.theme_style = "Dark"
        Window.size = (300, 600)
        return kv


graphApp().run()  # :D
