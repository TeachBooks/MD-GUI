# pip install markdown 
# pip install tkhtmlview


import tkinter as tk
from tkinter import scrolledtext, simpledialog, filedialog
import markdown
from tkhtmlview import HTMLLabel
import random
import string

# ---------------------------- #
# quit the app
#def quit_app(event=None):
#    app.quit()

# labelmaker
def label_maker():
    return ''.join(random.choices(string.ascii_uppercase, k=4))

# update preview of markdown output
def update_preview(event=None):
    try:
        md_text = text_area.get("1.0", tk.END)
        html_text = markdown.markdown(md_text)
        html_label.set_html(html_text)
    except Exception as e:
        print(f"Error in update_preview: {e}")

# ---------------------------- #
# added functionalities

# adding a chapter
def add_chapter():
    #text_area.insert(tk.INSERT, '(', label_maker(), ')=' '# ')
    #label = label_maker()
    text_area.insert(tk.INSERT, f'({label_maker()})= \n# ')
    update_preview()


# adding a section
def add_section():
    text_area.insert(tk.INSERT, '## ')
    update_preview()


# adding a subsection
def add_subsection():
    text_area.insert(tk.INSERT, '### ')
    update_preview()


# adding a figure
def add_figure():
    figure_name = simpledialog.askstring("Input", "Enter the name of the file:")
    if figure_name:
        width = simpledialog.askstring("Input", "Enter the width percentage:")
        alignment = simpledialog.askstring("Input", "Enter the alignment (left, center, right):")
        caption = simpledialog.askstring("Input", "Enter the caption:")
        fig_label = simpledialog.askstring("Input", "Enter the labelname:")
        
        figure_markdown = f"""
```{{figure}} {figure_name}
---
width: {width}%
alignment: {alignment}
name: {fig_label}
---
{caption}
```"""
    text_area.insert(tk.INSERT, figure_markdown)
    update_preview()


# including bold text
def add_bold():
    try:
        start_idx = text_area.index(tk.SEL_FIRST)
        end_idx = text_area.index(tk.SEL_LAST)
    except tk.TclError:
        start_idx = None
        end_idx = None

    if start_idx and end_idx:
        selected_text = text_area.get(start_idx, end_idx)
        text_area.delete(start_idx, end_idx)
        text_area.insert(start_idx, f"**{selected_text}**")
        text_area.tag_remove(tk.SEL, "1.0", tk.END)
    else:
        cursor_idx = text_area.index(tk.INSERT)
        text_area.insert(cursor_idx, "**")
        text_area.insert(cursor_idx + "+2c", "**")
        text_area.mark_set(tk.INSERT, cursor_idx + "+2c")

    update_preview()


# including italics
def add_italics():
    try:
        start_idx = text_area.index(tk.SEL_FIRST)
        end_idx = text_area.index(tk.SEL_LAST)
    except tk.TclError:
        start_idx = None
        end_idx = None

    if start_idx and end_idx:
        selected_text = text_area.get(start_idx, end_idx)
        text_area.delete(start_idx, end_idx)
        text_area.insert(start_idx, f"*{selected_text}*")
        text_area.tag_remove(tk.SEL, "1.0", tk.END)
    else:
        cursor_idx = text_area.index(tk.INSERT)
        text_area.insert(cursor_idx, "*")
        text_area.insert(cursor_idx + "+2c", "*")
        text_area.mark_set(tk.INSERT, cursor_idx + "+2c")

    update_preview()


# Including an equation
def add_equation():
    try:
        start_idx = text_area.index(tk.SEL_FIRST)
        end_idx = text_area.index(tk.SEL_LAST)
    except tk.TclError:
        start_idx = None
        end_idx = None

    if start_idx and end_idx:
        selected_text = text_area.get(start_idx, end_idx)
        text_area.delete(start_idx, end_idx)
        label = f"(eq:{label_maker()})\n"
        text_area.insert(start_idx, f"\n$$ {selected_text} $$ {label}")
        text_area.tag_remove(tk.SEL, "1.0", tk.END)
    else:
        cursor_idx = text_area.index(tk.INSERT)
        text_area.insert(cursor_idx, "\n$$")
        label = f"$$ (eq:{label_maker()})\n"
        text_area.insert(cursor_idx + "+3c", label)
        text_area.mark_set(tk.INSERT, cursor_idx + "+3c")

    update_preview()


# add youtube video
def add_youtube():
    YTurl = simpledialog.askstring("Input", "Enter the EMBED YouTube URL:")
    if YTurl:
        YT_markdown = f"""
\n
<div style="display: flex; justify-content: center;">
    <div style="position: relative; width: 70%; height: 0; padding-bottom: 56.25%;">
        <iframe
            src="{YTurl}"  
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
        ></iframe>
    </div>
</div>
\n
"""
    text_area.insert(tk.INSERT, YT_markdown)
    update_preview()


# add admonition
def add_admonition():
    admonition_type = simpledialog.askstring("Input", "Enter the type of admonition (warning, note, tip, info, danger):")
    if admonition_type:
        admonition_text = simpledialog.askstring("Input", "Enter the text of the admonition:")
        admonition_markdown = f"""
```{{{admonition_type}}}
{admonition_text}
```
"""
    text_area.insert(tk.INSERT, admonition_markdown)
    update_preview()


# add highlight
def add_highlight():
    try:
        start_idx = text_area.index(tk.SEL_FIRST)
        end_idx = text_area.index(tk.SEL_LAST)
    except tk.TclError:
        start_idx = None
        end_idx = None

    if start_idx and end_idx:
        selected_text = text_area.get(start_idx, end_idx)
        text_area.delete(start_idx, end_idx)
        
        # Splits de geselecteerde tekst op nieuwe regels en voeg > toe aan elke regel
        highlighted_text = "\n".join([f"> {line}" for line in selected_text.splitlines()])
        text_area.insert(start_idx, highlighted_text)
        
        text_area.tag_remove(tk.SEL, "1.0", tk.END)
    else:
        cursor_idx = text_area.index(tk.INSERT)
        text_area.insert(cursor_idx, "> ")
        text_area.mark_set(tk.INSERT, cursor_idx + "+2c")

    update_preview()

# add reference
# def add_reference():


# ---------------------------- #
# Menu functions
def new_file():
    text_area.delete("1.0", tk.END)
    update_preview()

def open_file():
    filename = tk.filedialog.askopenfilename()
    if filename:
        with open(filename, "r") as file:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.INSERT, file.read())
            update_preview()

def save_file():
    filename = tk.filedialog.asksaveasfilename()
    if filename:
        with open(filename, "w") as file:
            file.write(text_area.get("1.0", tk.END))

def about():
    about_text = """
This is a simple markdown previewer applet, allowing you to write markdown text and preview it in real-time. Not all markdown features are supported (like showing the figure), but the most common ones are.

Made by Freek Pols, Teachbooks
https://github.com/TeachBooks/MD-GUI
Version 1.0
CC-BY-NC
    """
    tk.messagebox.showinfo("About", about_text)

def help():
    help_text = """
    See this, yet non-existing, youtube video for a quick tutorial on how to use this applet.
    """
    tk.messagebox.showinfo("Help", help_text)

# ---------------------------- #
# main function

def main():
    global text_area, html_label
    
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
        menu_menu.add_command(label="New", command=new_file)  # new file
        menu_menu.add_command(label="Open", command=open_file)  # open file
        menu_menu.add_command(label="Save", command=save_file)  # save file
        menu_menu.add_separator()
        menu_menu.add_command(label="Exit", command=app.quit)  # Exit 

        # Add a "Help" dropdownmenu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=about)  # about
        help_menu.add_command(label="Help", command=help)  # help


        # Frame
        frame = tk.Frame(app)
        frame.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(frame)
        button_frame.pack(side=tk.LEFT, fill=tk.Y)

        button_width = 20

        # Buttons
        chapter_button = tk.Button(button_frame, text="Chapter", command=add_chapter, width=button_width)
        chapter_button.pack(pady=10)

        section_button = tk.Button(button_frame, text="Section", command=add_section, width=button_width)
        section_button.pack(pady=10)

        subsection_button = tk.Button(button_frame, text="Subsection", command=add_subsection, width=button_width)
        subsection_button.pack(pady=10)

        bold_button = tk.Button(button_frame, text="Bold", command=add_bold, width=button_width)
        bold_button.pack(pady=10)
        
        bold_button = tk.Button(button_frame, text="Italics", command=add_italics, width=button_width)
        bold_button.pack(pady=10)

        bold_button = tk.Button(button_frame, text="Highlight", command=add_highlight, width=button_width)
        bold_button.pack(pady=10)

        bold_button = tk.Button(button_frame, text="Equation", command=add_equation, width=button_width)
        bold_button.pack(pady=10)

        figure_button = tk.Button(button_frame, text="Figure", command=add_figure, width=button_width)
        figure_button.pack(pady=10)

        bold_button = tk.Button(button_frame, text="YTvideo", command=add_youtube, width=button_width)
        bold_button.pack(pady=10)

        bold_button = tk.Button(button_frame, text="Admonition", command=add_admonition, width=button_width)
        bold_button.pack(pady=10)


        # Text Area

        text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_area.bind("<KeyRelease>", update_preview)

        # HTML Label
        
        html_label = HTMLLabel(frame, html="<p>This applet is made by <a href='http://teachbooks.tudelft.nl'>teachbooks</a></p>")
        html_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        app.mainloop()
    except Exception as e:
        print(f"Application Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error in main: {e}")
