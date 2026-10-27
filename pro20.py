
"""
Program: Modular Multi-Frame Graphical Dashboard Application
Author: Saurav 241492

Description:
    Creates a multi-screen dashboard using Tkinter.
    Uses separate classes for application state, dashboard
    views, and event handling. Saves configuration to JSON.

Input:
    User selections, text entries, and dashboard settings.

Output:
    Interactive dashboard with saved configuration data.
"""

import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path


CONFIG_FILE = Path("dashboard_config.json")


# -------------------- MODEL --------------------

class DashboardModel:
    """Stores and manages dashboard configuration."""

    def __init__(self):
        self.config = {
            "username": "User",
            "theme": "Light",
            "notifications": True,
            "last_page": "Dashboard"
        }

    def update(self, key, value):
        """Update one configuration setting."""
        self.config[key] = value

    def save(self, path=CONFIG_FILE):
        """Save configuration to a JSON file."""
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.config, file, indent=4)

    def load(self, path=CONFIG_FILE):
        """Load configuration from a JSON file."""
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Configuration must be a JSON object.")

        defaults = {
            "username": "User",
            "theme": "Light",
            "notifications": True,
            "last_page": "Dashboard"
        }
        defaults.update(data)

        if not isinstance(defaults["username"], str):
            raise ValueError("Username must be text.")
        if defaults["theme"] not in ("Light", "Dark"):
            raise ValueError("Theme must be Light or Dark.")
        if not isinstance(defaults["notifications"], bool):
            raise ValueError("Notifications must be True or False.")
        if defaults["last_page"] not in (
            "Dashboard", "Reports", "Settings"
        ):
            defaults["last_page"] = "Dashboard"

        self.config = defaults


# -------------------- VIEW --------------------

class DashboardApp:
    """Builds the GUI and coordinates application events."""

    def __init__(self, root):
        self.root = root
        self.root.title("Modular Graphical Dashboard")
        self.root.geometry("900x600")
        self.root.minsize(650, 450)

        self.model = DashboardModel()
        self.current_page = "Dashboard"
        self.pages = {}

        self._build_menu()
        self._build_layout()
        self._build_pages()
        self._build_status_bar()

        self.apply_theme()
        self.show_page("Dashboard")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_menu(self):
        """Create the application menu bar."""
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(
            label="Save Configuration",
            command=self.save_config
        )
        file_menu.add_command(
            label="Load Configuration",
            command=self.load_config
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Export Configuration As...",
            command=self.export_config
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit",
            command=self.on_close
        )
        menu_bar.add_cascade(label="File", menu=file_menu)

        view_menu = tk.Menu(menu_bar, tearoff=0)
        for page in ("Dashboard", "Reports", "Settings"):
            view_menu.add_command(
                label=page,
                command=lambda p=page: self.show_page(p)
            )
        menu_bar.add_cascade(label="View", menu=view_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(
            label="About",
            command=self.show_about
        )
        help_menu.add_command(
            label="Help",
            command=self.show_help
        )
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def _build_layout(self):
        """Create the navigation and content frames."""
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill="both", expand=True)

        self.sidebar = ttk.Frame(
            self.main_frame, width=170, padding=10
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ttk.Label(
            self.sidebar,
            text="NAVIGATION",
            font=("Arial", 11, "bold")
        ).pack(fill="x", pady=(5, 15))

        for page in ("Dashboard", "Reports", "Settings"):
            ttk.Button(
                self.sidebar,
                text=page,
                command=lambda p=page: self.show_page(p)
            ).pack(fill="x", pady=5)

        ttk.Separator(
            self.main_frame, orient="vertical"
        ).pack(side="left", fill="y", padx=8)

        self.content = ttk.Frame(self.main_frame, padding=10)
        self.content.pack(side="left", fill="both", expand=True)

    def _build_pages(self):
        """Create each screen as a separate nested frame."""
        self.pages["Dashboard"] = self._dashboard_page()
        self.pages["Reports"] = self._reports_page()
        self.pages["Settings"] = self._settings_page()

    def _dashboard_page(self):
        page = ttk.Frame(self.content)

        ttk.Label(
            page, text="Dashboard Overview",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", pady=(0, 15))

        ttk.Label(
            page,
            text="Welcome to your modular dashboard."
        ).pack(anchor="w", pady=(0, 15))

        cards = ttk.Frame(page)
        cards.pack(fill="x", pady=10)

        stats = [
            ("Total Users", "1,250"),
            ("Active Sessions", "86"),
            ("Reports", "24")
        ]

        for title, value in stats:
            card = ttk.LabelFrame(cards, text=title, padding=15)
            card.pack(side="left", fill="both", expand=True, padx=5)
            ttk.Label(
                card, text=value,
                font=("Arial", 18, "bold")
            ).pack()

        ttk.Label(
            page,
            text="Use the sidebar or View menu to change screens."
        ).pack(anchor="w", pady=20)

        return page

    def _reports_page(self):
        page = ttk.Frame(self.content)

        ttk.Label(
            page, text="Reports",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", pady=(0, 15))

        ttk.Label(
            page,
            text="Select a report category:"
        ).pack(anchor="w", pady=5)

        self.report_choice = tk.StringVar(value="User Activity")

        report_box = ttk.Combobox(
            page,
            textvariable=self.report_choice,
            values=[
                "User Activity",
                "System Performance",
                "Monthly Summary"
            ],
            state="readonly",
            width=30
        )
        report_box.pack(anchor="w", pady=5)

        ttk.Button(
            page,
            text="Generate Report",
            command=self.generate_report
        ).pack(anchor="w", pady=10)

        self.report_result = ttk.Label(
            page, text="No report generated yet."
        )
        self.report_result.pack(anchor="w", pady=10)

        return page

    def _settings_page(self):
        page = ttk.Frame(self.content)

        ttk.Label(
            page, text="Dashboard Settings",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", pady=(0, 15))

        form = ttk.Frame(page)
        form.pack(anchor="w", fill="x")

        ttk.Label(form, text="Username:").grid(
            row=0, column=0, sticky="w", pady=8
        )
        self.username_var = tk.StringVar(
            value=self.model.config["username"]
        )
        ttk.Entry(
            form, textvariable=self.username_var, width=30
        ).grid(row=0, column=1, sticky="w", padx=10)

        ttk.Label(form, text="Theme:").grid(
            row=1, column=0, sticky="w", pady=8
        )
        self.theme_var = tk.StringVar(
            value=self.model.config["theme"]
        )
        ttk.Combobox(
            form,
            textvariable=self.theme_var,
            values=["Light", "Dark"],
            state="readonly",
            width=27
        ).grid(row=1, column=1, sticky="w", padx=10)

        self.notifications_var = tk.BooleanVar(
            value=self.model.config["notifications"]
        )
        ttk.Checkbutton(
            page,
            text="Enable notifications",
            variable=self.notifications_var
        ).pack(anchor="w", pady=12)

        buttons = ttk.Frame(page)
        buttons.pack(anchor="w", pady=10)

        ttk.Button(
            buttons,
            text="Apply Settings",
            command=self.apply_settings
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            buttons,
            text="Reset Settings",
            command=self.reset_settings
        ).pack(side="left")

        return page

    def _build_status_bar(self):
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            padding=5
        ).pack(side="bottom", fill="x")

    # -------------------- CONTROLLER / EVENTS --------------------

    def show_page(self, page_name):
        """Display the selected screen and update application state."""
        if page_name not in self.pages:
            messagebox.showwarning(
                "Invalid Page",
                "The selected page does not exist.",
                parent=self.root
            )
            return

        for page in self.pages.values():
            page.pack_forget()

        self.pages[page_name].pack(fill="both", expand=True)
        self.current_page = page_name
        self.model.update("last_page", page_name)
        self.status_var.set(f"Current screen: {page_name}")

    def generate_report(self):
        """Show a simple report summary based on the selected category."""
        category = self.report_choice.get()

        summaries = {
            "User Activity": "Active users today: 86",
            "System Performance": "System status: Operational",
            "Monthly Summary": "Monthly reports available: 24"
        }

        self.report_result.config(
            text=f"{category}: {summaries.get(category, 'No data available')}"
        )
        self.status_var.set(f"Generated report: {category}")

    def apply_settings(self):
        """Validate and apply settings entered by the user."""
        username = self.username_var.get().strip()
        theme = self.theme_var.get()

        if not username:
            messagebox.showwarning(
                "Missing Username",
                "Please enter a username.",
                parent=self.root
            )
            return

        if theme not in ("Light", "Dark"):
            messagebox.showwarning(
                "Invalid Theme",
                "Please select Light or Dark.",
                parent=self.root
            )
            return

        self.model.update("username", username)
        self.model.update("theme", theme)
        self.model.update(
            "notifications", self.notifications_var.get()
        )

        self.apply_theme()
        self.status_var.set("Settings applied.")

        messagebox.showinfo(
            "Settings",
            "Your settings have been applied.",
            parent=self.root
        )

    def reset_settings(self):
        """Restore default settings after user confirmation."""
        confirm = messagebox.askyesno(
            "Reset Settings",
            "Restore all settings to their defaults?",
            parent=self.root
        )

        if not confirm:
            return

        self.model.config.update({
            "username": "User",
            "theme": "Light",
            "notifications": True
        })

        self.username_var.set("User")
        self.theme_var.set("Light")
        self.notifications_var.set(True)

        self.apply_theme()
        self.status_var.set("Settings reset.")

    def apply_theme(self):
        """Apply a simple light or dark theme to the main frames."""
        dark = self.model.config["theme"] == "Dark"
        background = "#252526" if dark else "#f0f0f0"
        foreground = "#ffffff" if dark else "#202020"

        self.root.configure(bg=background)

        # Update classic Tk widgets and frames.
        self._set_widget_colors(self.root, background, foreground)

    def _set_widget_colors(self, parent, background, foreground):
        """Recursively set colors where supported by each widget."""
        for widget in parent.winfo_children():
            try:
                if isinstance(widget, (tk.Frame, tk.Label, tk.Button)):
                    widget.configure(
                        bg=background,
                        fg=foreground
                    )
            except tk.TclError:
                pass

            self._set_widget_colors(
                widget, background, foreground
            )

    def save_config(self):
        """Save current settings to the default JSON file."""
        try:
            self.model.save()
            self.status_var.set(f"Saved to {CONFIG_FILE}")
            messagebox.showinfo(
                "Saved",
                f"Configuration saved to:\n{CONFIG_FILE.resolve()}",
                parent=self.root
            )
        except (OSError, TypeError, ValueError) as error:
            messagebox.showerror(
                "Save Error",
                f"Could not save configuration:\n{error}",
                parent=self.root
            )

    def load_config(self):
        """Load configuration from the default JSON file."""
        if not CONFIG_FILE.exists():
            messagebox.showwarning(
                "File Not Found",
                "No saved configuration was found yet.",
                parent=self.root
            )
            return

        try:
            self.model.load()
            self._sync_settings()
            self.apply_theme()

            last_page = self.model.config["last_page"]
            self.show_page(last_page)

            self.status_var.set("Configuration loaded.")
            messagebox.showinfo(
                "Loaded",
                "Configuration loaded successfully.",
                parent=self.root
            )
        except (OSError, ValueError, json.JSONDecodeError) as error:
            messagebox.showerror(
                "Load Error",
                f"Could not load configuration:\n{error}",
                parent=self.root
            )

    def export_config(self):
        """Save configuration to a user-selected JSON file."""
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Export Dashboard Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )

        if not path:
            return

        try:
            self.model.save(path)
            messagebox.showinfo(
                "Export Complete",
                f"Configuration exported to:\n{path}",
                parent=self.root
            )
        except (OSError, TypeError, ValueError) as error:
            messagebox.showerror(
                "Export Error",
                str(error),
                parent=self.root
            )

    def _sync_settings(self):
        """Update the settings widgets after loading configuration."""
        self.username_var.set(self.model.config["username"])
        self.theme_var.set(self.model.config["theme"])
        self.notifications_var.set(
            self.model.config["notifications"]
        )

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Modular Multi-Frame Graphical Dashboard\n"
            "Developed with Python and Tkinter.\n"
            "Architecture: MVC-lite",
            parent=self.root
        )

    def show_help(self):
        messagebox.showinfo(
            "Help",
            "1. Use the sidebar or View menu to switch screens.\n"
            "2. Generate a report on the Reports screen.\n"
            "3. Change preferences in Settings.\n"
            "4. Use File > Save Configuration to save settings.\n"
            "5. Use File > Load Configuration to restore settings.",
            parent=self.root
        )

    def on_close(self):
        """Ask before closing the dashboard."""
        if messagebox.askyesno(
            "Exit Dashboard",
            "Are you sure you want to exit?",
            parent=self.root
        ):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
