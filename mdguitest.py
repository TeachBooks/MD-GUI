# mdguitest.py
import tkinter as tk
from tkinter import scrolledtext
import functionalities as fn
from tkhtmlview import HTMLLabel

def main():
    root = tk.Tk()
    root.title("Markdown GUI")

    # Frame Setup
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Text Area
    text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50)
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # HTML Label
    html_label = HTMLLabel(frame, html="<p>This applet is made by <a href='http://teachbooks.tudelft.nl'>teachbooks</a></p>")
    html_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Bind KeyRelease to update preview
    text_area.bind("<KeyRelease>", lambda event: fn.update_preview(text_area, html_label))

    # Button Frame
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, fill=tk.X)

    # Example Button
    chapter_button = tk.Button(button_frame, text="Chapter", command=lambda: fn.add_chapter(text_area, html_label))
    chapter_button.pack(pady=5)

    section_button = tk.Button(button_frame, text="Section", command=lambda: fn.add_section(text_area, html_label))
    section_button.pack(pady=5)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
