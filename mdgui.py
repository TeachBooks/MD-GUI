# pip install markdown 
# pip install tkhtmlview


import tkinter as tk
from tkinter import scrolledtext, simpledialog
import markdown
from tkhtmlview import HTMLLabel

def update_preview(event=None):
    try:
        md_text = text_area.get("1.0", tk.END)
        html_text = markdown.markdown(md_text)
        html_label.set_html(html_text)
    except Exception as e:
        print(f"Error in update_preview: {e}")

# buttons left side
def add_chapter():
    text_area.insert(tk.INSERT, '# ')
    update_preview()

def add_section():
    text_area.insert(tk.INSERT, '## ')
    update_preview()

def add_subsection():
    text_area.insert(tk.INSERT, '### ')
    update_preview()

def add_figure():
    figure_name = simpledialog.askstring("Input", "Enter the name of the file:")
    if figure_name:
        width = simpledialog.askstring("Input", "Enter the width percentage:")
        alignment = simpledialog.askstring("Input", "Enter the alignment (left, center, right):")
        caption = simpledialog.askstring("Input", "Enter the caption:")
        fig_name = simpledialog.askstring("Input", "Enter the figure name:")
        
        figure_markdown = f"""
```{{figure}} {figure_name}
---
width: {width}%
alignment: {alignment}
name: {fig_name}
---
{caption}
```"""
    text_area.insert(tk.INSERT, figure_markdown)
    update_preview()

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


def main():
    global text_area, html_label
    
    try:
        app = tk.Tk()
        app.title("Markdown Previewer")

        frame = tk.Frame(app)
        frame.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(frame)
        button_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Buttons
        chapter_button = tk.Button(button_frame, text="Chapter", command=add_chapter)
        chapter_button.pack(pady=10)

        section_button = tk.Button(button_frame, text="Section", command=add_section)
        section_button.pack(pady=10)

        subsection_button = tk.Button(button_frame, text="Subsection", command=add_subsection)
        subsection_button.pack(pady=10)

        figure_button = tk.Button(button_frame, text="Figure", command=add_figure)
        figure_button.pack(pady=10)

        bold_button = tk.Button(button_frame, text="Bold", command=add_bold)
        bold_button.pack(pady=10)

        # Text Area

        text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_area.bind("<KeyRelease>", update_preview)

        # HTML Label

        html_label = HTMLLabel(frame, html="<p>Type Markdown to see preview</p>")
        html_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        app.mainloop()
    except Exception as e:
        print(f"Application Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error in main: {e}")
