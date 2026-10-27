
"""
Program: Dynamic Interactive Image/File Viewer with Dialog Prompts
Author: Saurav 241492

Description:
    Opens and displays image or text files using Tkinter.
    Provides file selection, color selection, and message dialogs.
    Supports mouse clicks and the Enter key.

Input:
    File selection and color selection through GUI dialogs.

Output:
    Displays the selected image or text content in the window.
"""

import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from pathlib import Path

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class InteractiveFileViewer:
    """Interactive GUI application for viewing image and text files."""

    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Image/File Viewer")
        self.root.geometry("850x650")
        self.root.minsize(600, 450)

        self.current_image = None
        self.current_file = None

        # Header
        self.title_label = tk.Label(
            root,
            text="Dynamic Image/File Viewer",
            font=("Arial", 20, "bold"),
            pady=12
        )
        self.title_label.pack(fill="x")

        # Toolbar
        toolbar = tk.Frame(root, padx=10, pady=8)
        toolbar.pack(fill="x")

        tk.Button(
            toolbar, text="Open File",
            command=self.open_file
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar, text="Choose Background",
            command=self.choose_color
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar, text="About",
            command=self.show_about
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar, text="Clear",
            command=self.clear_view
        ).pack(side="left", padx=5)

        # File information label
        self.info_label = tk.Label(
            root,
            text="No file selected. Click Open File or press Enter.",
            anchor="w",
            padx=10,
            pady=6
        )
        self.info_label.pack(fill="x")

        # Dynamic viewing area
        self.viewer = tk.Frame(
            root,
            bg="white",
            bd=2,
            relief="sunken"
        )
        self.viewer.pack(
            fill="both", expand=True,
            padx=12, pady=10
        )

        self.image_label = tk.Label(
            self.viewer,
            text="Your image or text file will appear here.",
            bg="white",
            font=("Arial", 12),
            wraplength=700
        )
        self.image_label.pack(
            fill="both", expand=True, padx=10, pady=10
        )

        # Keyboard and mouse event bindings
        self.root.bind("<Return>", self.handle_enter)
        self.image_label.bind("<Button-1>", self.handle_click)

        # Footer
        self.status_label = tk.Label(
            root,
            text="Ready",
            anchor="w",
            relief="groove",
            padx=10,
            pady=5
        )
        self.status_label.pack(fill="x", side="bottom")

    def open_file(self):
        """Open an image or text file using a native file dialog."""
        file_path = filedialog.askopenfilename(
            parent=self.root,
            title="Select an Image or Text File",
            filetypes=[
                ("Supported files", "*.png *.jpg *.jpeg *.gif *.bmp *.webp *.txt *.md *.csv *.py *.log"),
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("Text files", "*.txt *.md *.csv *.py *.log"),
                ("All files", "*.*")
            ]
        )

        if not file_path:
            self.status_label.config(text="File selection cancelled.")
            return

        self.current_file = Path(file_path)
        suffix = self.current_file.suffix.lower()

        try:
            if suffix in {
                ".png", ".jpg", ".jpeg", ".gif",
                ".bmp", ".webp"
            }:
                self.display_image(file_path)
            else:
                self.display_text(file_path)

        except (OSError, ValueError) as error:
            messagebox.showerror(
                "File Error",
                f"Could not open the selected file:\n{error}",
                parent=self.root
            )
            self.status_label.config(text="Unable to open file.")

    def display_image(self, file_path):
        """Display an image, resizing it to fit the viewing area."""
        if not PIL_AVAILABLE:
            messagebox.showerror(
                "Missing Library",
                "Install Pillow to display images:\n\n"
                "python -m pip install Pillow",
                parent=self.root
            )
            return

        with Image.open(file_path) as source:
            image = source.copy()

        image.thumbnail((760, 470))
        self.current_image = ImageTk.PhotoImage(image)

        self.image_label.config(
            image=self.current_image,
            text="",
            bg=self.viewer.cget("bg")
        )

        self.info_label.config(
            text=f"Image: {self.current_file.name}"
        )
        self.status_label.config(
            text=f"Image loaded: {self.current_file.name}"
        )

    def display_text(self, file_path):
        """Display the contents of a text file in a scrollable text area."""
        with open(file_path, "r", encoding="utf-8-sig") as file:
            content = file.read()

        self.image_label.pack_forget()

        # Create the text area only when needed.
        if not hasattr(self, "text_area"):
            self.text_frame = tk.Frame(self.viewer)
            self.text_area = tk.Text(
                self.text_frame,
                wrap="word",
                font=("Consolas", 11),
                undo=False
            )
            scrollbar = tk.Scrollbar(
                self.text_frame,
                command=self.text_area.yview
            )
            self.text_area.configure(
                yscrollcommand=scrollbar.set
            )

            scrollbar.pack(side="right", fill="y")
            self.text_area.pack(
                side="left", fill="both", expand=True
            )

        self.text_frame.pack(
            fill="both", expand=True, padx=5, pady=5
        )
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", content)
        self.text_area.config(state="disabled")

        self.info_label.config(
            text=f"Text file: {self.current_file.name}"
        )
        self.status_label.config(
            text=f"Text loaded: {self.current_file.name}"
        )

    def choose_color(self):
        """Change the background color using a color chooser."""
        result = colorchooser.askcolor(
            parent=self.root,
            title="Choose Viewer Background Color"
        )

        selected_color = result[1]

        if selected_color:
            self.viewer.config(bg=selected_color)

            # Keep the image area background synchronized.
            self.image_label.config(bg=selected_color)

            self.status_label.config(
                text=f"Background changed to {selected_color}"
            )

    def show_about(self):
        """Display information about the application."""
        messagebox.showinfo(
            "About",
            "Dynamic Interactive Image/File Viewer\n\n"
            "Built with Python and Tkinter.\n"
            "Supports image and text files, file dialogs,\n"
            "color selection, and keyboard/mouse events.",
            parent=self.root
        )

    def clear_view(self):
        """Clear the current image or text content."""
        self.current_image = None
        self.current_file = None

        if hasattr(self, "text_frame"):
            self.text_frame.pack_forget()

        self.image_label.pack(
            fill="both", expand=True, padx=10, pady=10
        )
        self.image_label.config(
            image="",
            text="Your image or text file will appear here.",
            bg=self.viewer.cget("bg")
        )

        self.info_label.config(text="No file selected.")
        self.status_label.config(text="Viewer cleared.")

    def handle_enter(self, event=None):
        """Open a file when the Enter key is pressed."""
        self.open_file()

    def handle_click(self, event=None):
        """Respond to a mouse click on the viewing area."""
        self.status_label.config(
            text="Viewing area clicked. Press Enter to open a file."
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = InteractiveFileViewer(root)
    root.mainloop()
