import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from texHandler import make_pdf


class CharacterFrame(ttk.Frame):
    def __init__(self, parent, remove_callback):
        super().__init__(parent, padding=5, relief="groove")

        self.remove_callback = remove_callback

        ttk.Label(self, text="Jméno:").grid(row=0, column=0, sticky="w", pady=3)
        self.name = ttk.Entry(self, width=30)
        self.name.grid(row=0, column=1, sticky="ew", pady=3)

        ttk.Label(self, text="Úspěchy (odděl čárkou):").grid(row=1, column=0, sticky="w", pady=3)
        self.achievements = tk.Text(self, width=40, height=3)
        self.achievements.grid(row=1, column=1, sticky="ew", pady=3)

        ttk.Label(self, text="Vlastnosti (odděl čárkou):").grid(row=2, column=0, sticky="w", pady=3)
        self.traits = tk.Text(self, width=40, height=3)
        self.traits.grid(row=2, column=1, sticky="ew", pady=3)

        remove_btn = ttk.Button(self, text="Odstranit postavu", command=self.remove_self)
        remove_btn.grid(row=3, column=0, columnspan=2, pady=5)

    def get_data(self):
        return {
            "Name": self.name.get(),
            "Achievements": [a.strip() for a in self.achievements.get("1.0", "end").split(",") if a.strip()],
            "Traits": [t.strip() for t in self.traits.get("1.0", "end").split(",") if t.strip()]
        }

    def remove_self(self):
        self.remove_callback(self)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lit-gen")
        self.geometry("750x750")

        # mapping GUI labels -> JSON keys
        self.field_map = {
            "Jméno žáka": "UserName",
            "Jméno knihy": "BookName",
            "Autor": "Author",
            "Literání druh": "Kind",
            "Literární styl": "Style",
            "Literární žánr": "Genre",
            "Téma": "Topic",
            "Vypravěč": "NarratorForm",
            "Kompozice": "Composition",
            "Jazyk": "LanguageDescription",
        }

        # Create a canvas with scrollbar
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Fields inside scrollable frame
        self.fields = {}
        for idx, (label, key) in enumerate(self.field_map.items()):
            ttk.Label(self.scroll_frame, text=label + ":").grid(row=idx, column=0, sticky="w", pady=5)
            entry = ttk.Entry(self.scroll_frame, width=50)
            entry.grid(row=idx, column=1, sticky="ew", pady=5)
            self.fields[key] = entry

        ttk.Label(self.scroll_frame, text="Časový kontext (odděl čárkou):").grid(row=10, column=0, sticky="w", pady=5)
        self.context_authors = tk.Text(self.scroll_frame, width=50, height=3)
        self.context_authors.grid(row=10, column=1, sticky="ew", pady=5)

        ttk.Label(self.scroll_frame, text="Motivy (odděl čárkou):").grid(row=11, column=0, sticky="w", pady=5)
        self.motives = tk.Text(self.scroll_frame, width=50, height=3)
        self.motives.grid(row=11, column=1, sticky="ew", pady=5)

        # Characters
        self.char_frame = ttk.LabelFrame(self.scroll_frame, text="Postavy", padding=10)
        self.char_frame.grid(row=12, column=0, columnspan=2, sticky="ew", pady=10)

        self.characters = []

        # Output folder path
        ttk.Label(self.scroll_frame, text="Výstupní složka:").grid(row=14, column=0, sticky="w", pady=5)
        self.output_entry = ttk.Entry(self.scroll_frame, width=50)
        self.output_entry.grid(row=14, column=1, sticky="ew", pady=5)
        ttk.Button(self.scroll_frame, text="Procházet...", command=self.browse_folder).grid(row=14, column=2, padx=5)

        ttk.Button(self.scroll_frame, text="Přidat Postavu", command=self.add_character).grid(row=15, column=0, pady=10)
        ttk.Button(self.scroll_frame, text="Vytvořit PDF", command=self.save_data).grid(row=15, column=1, pady=10)

        # Mousewheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def add_character(self):
        char = CharacterFrame(self.char_frame, self.remove_character)
        char.pack(fill="x", pady=8)
        self.characters.append(char)

    def remove_character(self, char):
        char.destroy()
        self.characters.remove(char)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)

    def save_data(self):
        # Collect base fields
        data = {key: widget.get() for key, widget in self.fields.items()}
        data["ContextAuthors"] = [a.strip() for a in self.context_authors.get("1.0", "end").split(",") if a.strip()]
        data["Motives"] = [m.strip() for m in self.motives.get("1.0", "end").split(",") if m.strip()]
        data["Characters"] = [c.get_data() for c in self.characters]

        if len(data["ContextAuthors"]) < 1: 
            messagebox.showerror("Chyba", "Pole 'Časový kontext' musí mít alespoň 1 hodnotu")
            return
        
        if len(data["Motives"]) < 3: 
            messagebox.showerror("Chyba", "Pole 'Motivy' musí mít alespoň 3 hodnoty")
            return
        
        folder = self.output_entry.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Chyba", "Prosím vyberte existující výstupní složku.")
            return

        path = os.path.join(folder, f"{data['BookName']}-Rozbor.json")
        
        with open(path, "w+", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        make_pdf(data, folder, f"{data['BookName']}-Rozbor")

        messagebox.showinfo("Success", f"Data saved to {path}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
