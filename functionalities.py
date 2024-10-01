# functionalities.py
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import markdown
import random
import string

def new_file(text_area, html_label):
    text_area.delete("1.0", tk.END)
    update_preview(text_area, html_label)

def open_file(text_area, html_label):
    filename = filedialog.askopenfilename()
    if filename:
        with open(filename, "r") as file:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.INSERT, file.read())
            update_preview(text_area, html_label)

def save_file(text_area):
    filename = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])
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
    messagebox.showinfo("About", about_text)

def help():
    help_text = """
    See this, yet non-existing, YouTube video for a quick tutorial on how to use this applet.
    """
    messagebox.showinfo("Help", help_text)

def label_maker():
    return ''.join(random.choices(string.ascii_uppercase, k=4))

def update_preview(text_area, html_label):
    try:
        md_text = text_area.get("1.0", tk.END)
        html_text = markdown.markdown(md_text)
        html_label.set_html(html_text)  # Correct gebruik van html_label.set_html met de juiste HTML tekst
    except Exception as e:
        print(f"Error in update_preview: {e}")

def add_chapter(text_area, html_label):
    text_area.insert(tk.INSERT, f'(ch:{label_maker()})= \n# ')
    update_preview(text_area, html_label)

def add_section(text_area, html_label):
    text_area.insert(tk.INSERT, f'(sec:{label_maker()})= \n## ')
    update_preview(text_area, html_label)

# Voeg soortgelijke functies toe voor andere functionaliteiten als dat nodig is
