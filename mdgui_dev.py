import tkinter as tk
from tkinter import scrolledtext, simpledialog, filedialog, messagebox, Toplevel
import markdown
from tkhtmlview import HTMLLabel
import random
import string
import subprocess
import threading
import webbrowser
import os

# ---------------------------- #
# A Graphical User Interface with Markdown Previewer and HTML previewer
# made to make it easier to build Jupyter Books, using Teachbooks.
# Code consists of:
# - Markdown previewer
# - HTML previewer
# - Buttons to add markdown elements
# - Button to build the book
# - Menu with options to open, save, exit, help and about
# - Main menu
# ---------------------------- #


# ---------------------------- #
# update preview of markdown output
# The opened document saves after 5 new elements or every 500 characters

counter = 0
def update_preview(event=None):
    global counter
    try:
        md_text = text_area.get("1.0", tk.END)
        html_text = markdown.markdown(md_text)
        html_label.set_html(html_text)
        counter += 1
        if counter % 5 == 0:
            save_file()
            run_command()
    except Exception as e:
        print(f"Error in update_preview: {e}")

def update_preview_text_area(event=None):
    global counter
    try:
        md_text = text_area.get("1.0", tk.END)
        html_text = markdown.markdown(md_text)
        html_label.set_html(html_text)
        counter += 1
        if counter % 500 == 0:
            save_file()
            run_command()
    except Exception as e:
        print(f"Error in update_preview: {e}")

# ---------------------------- #


# ---------------------------- #
# This is the menu bar with the options to create a new file
# open a file, save a file, save a file as, exit the application
# and show the about and help information

def new_file():
    text_area.delete("1.0", tk.END)
    update_preview()

current_file = None
def open_file():
    global current_file
    filename = tk.filedialog.askopenfilename()
    if filename:
        current_file = filename
        with open(filename, "r") as file:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.INSERT, file.read())
            update_preview()
            run_command()

def save_file():
    global current_file
    if current_file:
        with open(current_file, "w") as file:
            file.write(text_area.get("1.0", tk.END))
    else:
        save_file_as()

def save_file_as():
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


# ---------------------------- #
# Some functions that are used in the applet

# Generate a random label of 4 uppercase letters
def label_maker():
    return ''.join(random.choices(string.ascii_uppercase, k=4))

# Checks whether text is selected. If so, returns the start and end index of the selection
def check_selected():
    global start_idx, end_idx
    try:
        start_idx = text_area.index(tk.SEL_FIRST)
        end_idx = text_area.index(tk.SEL_LAST)
    except tk.TclError:
        start_idx = None
        end_idx = None
    return start_idx, end_idx

# Creates a custom input dialog with a prompt
def custom_input_dialog(prompt):

    # Make a Toplevel window for the input dialog
    input_dialog = Toplevel()
    input_dialog.title("Input Dialog")
    input_dialog.geometry("300x150")
    input_dialog.transient(app) 
    input_dialog.grab_set()      # Block input to the parent window

    # Variabel to store the user input
    user_input = tk.StringVar()

    # Add a label to the Toplevel window
    label = tk.Label(input_dialog, text=prompt)
    label.pack(pady=10)

    # Add an entry field to the Toplevel window
    entry = tk.Entry(input_dialog, textvariable=user_input)
    entry.pack(pady=5)
    entry.focus()  # Zet de focus op het invoerveld

    # Function to confirm the input
    def confirm_input():
        input_dialog.destroy()

    # Add a button to confirm the input
    confirm_button = tk.Button(input_dialog, text="OK", command=confirm_input)
    confirm_button.pack(pady=10)

    # Wait for the input dialog to be closed
    app.wait_window(input_dialog)

    # Return the user input
    return user_input.get()


# ---------------------------- #
# FUNCTIONALITIES

# adding a chapter
def add_chapter():
    text_area.insert(tk.INSERT, f'(ch:{label_maker()})= \n# ')
    update_preview()

# adding a section
def add_section():
    text_area.insert(tk.INSERT, f'(sec:{label_maker()})= \n## ')
    update_preview()

# adding a subsection
def add_subsection():
    text_area.insert(tk.INSERT, f'(sec:{label_maker()})= \n### ')
    update_preview()

# including bold text
def add_bold():
    check_selected()
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
    check_selected()
    if start_idx and end_idx:
        selected_text = text_area.get(start_idx, end_idx)
        text_area.delete(start_idx, end_idx)
        text_area.insert(start_idx, f"*{selected_text}*")
        text_area.tag_remove(tk.SEL, "1.0", tk.END)
    else:
        cursor_idx = text_area.index(tk.INSERT)
        text_area.insert(cursor_idx, "**")
        #text_area.insert(cursor_idx + "+2c", "*")
        text_area.mark_set(tk.INSERT, cursor_idx + "+1c")
    update_preview()

# Add highlight
def add_highlight():
    check_selected()
    if start_idx and end_idx:
        selected_text = text_area.get(start_idx, end_idx)
        text_area.delete(start_idx, end_idx)
        
        # split the selected text into lines and add a > in front of each line
        highlighted_text = "\n".join([f"> {line}" for line in selected_text.splitlines()])
        text_area.insert(start_idx, highlighted_text)
        text_area.tag_remove(tk.SEL, "1.0", tk.END)
    else:
        cursor_idx = text_area.index(tk.INSERT)
        text_area.insert(cursor_idx, "> ")
        text_area.mark_set(tk.INSERT, cursor_idx + "+2c")
    update_preview()

# Including an equation
def add_equation():
    check_selected()
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

# add figure
def add_figure():
    figure_name = custom_input_dialog("Enter the name of the file:")
    if figure_name:
        width = custom_input_dialog("Enter the width percentage:")
        alignment = custom_input_dialog("Enter the alignment (left, center, right):")
        caption = custom_input_dialog("Enter the caption:")
        fig_label = custom_input_dialog("Enter the labelname:")
        
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





# add admonition
def add_admonition():
    admonition_type = custom_input_dialog("Enter the type of admonition (warning, note, tip, info, danger):")
    if admonition_type:
        admonition_text = custom_input_dialog("Enter the text of the admonition:")
        admonition_markdown = f"""
```{{{admonition_type}}}
{admonition_text}
```
"""
    text_area.insert(tk.INSERT, admonition_markdown)
    update_preview()


# add reference
# def add_reference():

# add exercise
def add_exercise():
    exercise = custom_input_dialog("Enter the exercise:")
    label = label_maker()
    if exercise:     
        exercise_markdown = f"""
```{{exercise}} 
:label: ex-{label}
{exercise}
```
"""
    text_area.insert(tk.INSERT, exercise_markdown)
    update_preview()

    solution = custom_input_dialog("Enter the solution:")
    if solution:     
        solution_markdown = f"""
```{{solution}} ex-{label}
:class: dropdown
{solution}
```
"""
    text_area.insert(tk.INSERT, solution_markdown)
    update_preview()        




# ---------------------------- #
# Global variable to control the animation
dots_running = False
dots_text = ""

# Run the jupyter-book build command
def run_command_1():
    """Run the jupyter-book build command and update the output_label with the result."""
    def execute_command():
        try:
            update_dots(popup, dots_label)  # Start the dots animation in the popup
            result = subprocess.run(['jupyter-book', 'build', 'book'], check=True, capture_output=True, text=True)
            message_label.config(text="Commando succesvol uitgevoerd!")
                
            # After successful execution, open the HTML file
            index_path = os.path.abspath(f"book/_build/html/index.html")
            
            if os.path.exists(index_path):
                webbrowser.open(index_path, new=0)                
            else:
                message_label.config(text="Build succesvol, maar index.html niet gevonden.")
        except subprocess.CalledProcessError as e:
            message_label.config(text=f"Fout bij uitvoeren van commando:\n{e.stderr}")
        finally:
            stop_dots()  # Stop the dots animation
            popup.after(2000, popup.destroy)  # Close the popup after 2 seconds

    # Maak een popup venster om de voortgang te tonen
    popup = Toplevel()
    popup.title("Building Book")
    popup.geometry("300x150")

    # Label om de bouwstatus weer te geven
    message_label = tk.Label(popup, text="Boek wordt gebouwd...", wraplength=280)
    message_label.pack(pady=10)

    # Label voor de stippeltjes animatie
    dots_label = tk.Label(popup, text="", wraplength=280, justify="center")
    dots_label.pack(pady=10)

    # Run the command in a separate thread to avoid blocking the GUI
    threading.Thread(target=execute_command).start()

def run_command():
    """Run the jupyter-book build command and update the output_label with the result."""
    def execute_command():
        try:
            result = subprocess.run(['jupyter-book', 'build', 'book'], check=True, capture_output=True, text=True)
                
            # Na succesvolle uitvoering, open het HTML-bestand
            file_base, _ = os.path.splitext(current_file)  # Split de naam en extensie, gebruik _ om de extensie te negeren
            index_path = os.path.abspath(f"book/_build/html/{os.path.basename(file_base)}.html")

            if os.path.exists(index_path):
                webbrowser.open(index_path, new=0)                
            else:
                message_label.config(text="Build successful, but page not found.")
        except subprocess.CalledProcessError as e:
            message_label.config(text=f"Error running the command:\n{e.stderr}")
        
    # Run the command in a separate thread to avoid blocking the GUI
    threading.Thread(target=execute_command).start()

# Animation of dots
dots_running = False

def update_dots(popup, dots_label):
    """Update the dots in the popup label with an increasing number of dots every 3 seconds."""
    global dots_running, dots_text
    dots_running = True
    dots_text = ""

    def animate():
        global dots_text
        if dots_running:
            dots_text += "." if len(dots_text) < 3 else ""
            if len(dots_text) == 3:
                dots_text = ""
            dots_label.config(text=f"Building book{dots_text}")
            dots_label.after(1000, animate)  # Update elke seconde

    animate()

def stop_dots():
    """Stop the dots animation."""
    global dots_running
    dots_running = False

# ---------------------------- #


# ---------------------------- #
# main function
app = tk.Tk()
app.title("Markdown Previewer")

def main():
    global text_area, html_label, output_label
    
    try:

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
        button_font = ('sans', 12)

        # Buttons
        chapter_button = tk.Button(button_frame, text="Chapter", font=('sans', 10), command=add_chapter, width=button_width)
        chapter_button.pack(pady=10)

        section_button = tk.Button(button_frame, text="Section", font=('sans', 10), command=add_section, width=button_width)
        section_button.pack(pady=10)

        subsection_button = tk.Button(button_frame, text="Subsection", font=('sans', 10), command=add_subsection, width=button_width)
        subsection_button.pack(pady=10)

        bold_button = tk.Button(button_frame, text="Bold", font=('sans', 10, 'bold'), command=add_bold, width=button_width)
        bold_button.pack(pady=10)
        
        italic_button = tk.Button(button_frame, text="Italic", font=('sans', 10, 'italic'), command=add_italics, width=button_width)
        italic_button.pack(pady=10)

        highlight_button = tk.Button(button_frame, text="Highlight", font=('sans', 10), command=add_highlight, width=button_width)
        highlight_button.pack(pady=10)

        eq_button = tk.Button(button_frame, text="Equation", font=('sans', 10), command=add_equation, width=button_width)
        eq_button.pack(pady=10)

        figure_button = tk.Button(button_frame, text="Figure", font=('sans', 10), command=add_figure, width=button_width)
        figure_button.pack(pady=10)

        YT_button = tk.Button(button_frame, text="YTvideo", font=('sans', 10), command=add_youtube, width=button_width)
        YT_button.pack(pady=10)

        adm_button = tk.Button(button_frame, text="Admonition", font=('sans', 10), command=add_admonition, width=button_width)
        adm_button.pack(pady=10)

        exc_button = tk.Button(button_frame, text="Exercise", font=('sans', 10), command=add_exercise, width=button_width)
        exc_button.pack(pady=10)

        run_button = tk.Button(button_frame, text="Build TeachBook", font=('sans', 10), command=run_command_1, width=button_width)
        run_button.pack(pady=20)
        
        # Text Area

        text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_area.bind("<KeyRelease>", update_preview_text_area)

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

