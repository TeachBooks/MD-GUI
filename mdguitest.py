# pip install markdown 
# pip install tkhtmlview


import tkinter as tk
from tkinter import scrolledtext, simpledialog, filedialog, messagebox, Toplevel
import functionalities as fn
import markdown
from tkhtmlview import HTMLLabel
import random
import string
import subprocess
import threading
import webbrowser
import os


# Menu functions



# ---------------------------- #


# ---------------------------- #
# main function

def main():
    global text_area, html_label, output_label
    
    try:
        app = tk.Tk()
        app.title("Markdown Previewer")

#        app.bind('<Control-q>', quit_app())

        # Add a menubar
        menubar = tk.Menu(app)
        app.config(menu=menubar)

        # Add a "Menu" dropdownmenu
        menu_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=menu_menu)
        menu_menu.add_command(label="New", command=lambda: fn.new_file())  # new file
        menu_menu.add_command(label="Open", command=lambda: fn.open_file())  # open file
        menu_menu.add_command(label="Save", command=lambda: fn.save_file())  # save file
        menu_menu.add_separator()
        #menu_menu.add_command(label="Exit", command=app.quit)  # Exit 

        # Add a "Help" dropdownmenu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: fn.about())  # about
        help_menu.add_command(label="Help", command=lambda: fn.help())  # help


        # Frame
        frame = tk.Frame(app)
        frame.pack(fill=tk.BOTH, expand=True)

        text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_area.bind("<KeyRelease>", lambda event: fn.update_preview(text_area, html_label))  # Zorg dat de functie wordt aangeroepen

        output_frame = tk.Frame(frame)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        web_view = HTMLLabel(output_frame, html="<iframe src='/book/_build/html/index.html' width='100%' height='100%'></iframe>")
        web_view.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(frame)
        button_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Buttons
        button_width = 20

        chapter_button = tk.Button(button_frame, text="Chapter", command=lambda: fn.add_chapter(text_area,html_label), width=button_width)
        chapter_button.pack(pady=10)

        section_button = tk.Button(button_frame, text="Section", command=lambda: fn.add_section(text_area), width=button_width)
        section_button.pack(pady=10)

        subsection_button = tk.Button(button_frame, text="Subsection", command=lambda: fn.add_subsection(text_area), width=button_width)
        subsection_button.pack(pady=10)

        bold_button = tk.Button(button_frame, text="Bold", command=lambda: fn.add_bold(text_area), width=button_width)
        bold_button.pack(pady=10)
        
        bold_button = tk.Button(button_frame, text="Italics", command=lambda: fn.add_italics(text_area), width=button_width)
        bold_button.pack(pady=10)

        bold_button = tk.Button(button_frame, text="Highlight", command=lambda: fn.add_highlight(text_area), width=button_width)
        bold_button.pack(pady=10)

        bold_button = tk.Button(button_frame, text="Equation", command=lambda: fn.add_equation(text_area), width=button_width)
        bold_button.pack(pady=10)

        figure_button = tk.Button(button_frame, text="Figure", command=lambda: fn.add_figure(text_area), width=button_width)
        figure_button.pack(pady=10)

        bold_button = tk.Button(button_frame, text="YTvideo", command=lambda: fn.add_youtube(text_area), width=button_width)
        bold_button.pack(pady=10)

        bold_button = tk.Button(button_frame, text="Admonition", command=lambda: fn.add_admonition(text_area), width=button_width)
        bold_button.pack(pady=10)

        bold_button = tk.Button(button_frame, text="Exercise", command=lambda: fn.add_exercise(text_area), width=button_width)
        bold_button.pack(pady=10)

        run_button = tk.Button(button_frame, text="Build TeachBook", command=lambda: fn.run_command(text_area), width=button_width)
        run_button.pack(pady=20)
        
        # Text Area

        text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_area.bind("<KeyRelease>", lambda: fn.update_preview)

        # HTML Label
        
        html_label = HTMLLabel(frame, html="<p>This applet is made by <a href='http://teachbooks.tudelft.nl'>teachbooks</a></p>")
        html_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


        # OUTPUT RUN
        output_label = tk.Label(frame, text="", wraplength=400, justify="left")
        output_label.pack(pady=10)



        app.mainloop()
    except Exception as e:
        print(f"Application Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error in main: {e}")

