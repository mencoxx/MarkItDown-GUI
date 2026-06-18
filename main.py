"""
MarkItDown Converter
=====================
Interfaccia grafica desktop per convertire file (PDF, DOCX, PPTX, XLSX, XLS,
immagini, audio, HTML, CSV, JSON, XML, ZIP, EPUB, ...) in Markdown usando la
libreria MarkItDown di Microsoft (https://github.com/microsoft/markitdown).

Realizzato da Leonardo Cozzolino.

Eseguibile sia come script (`python main.py`) sia come .exe generato con
PyInstaller (vedi build.bat).
"""

import os
import sys
import threading
import traceback
import webbrowser
from datetime import datetime
from pathlib import Path

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

APP_TITLE = "MarkItDown Converter"
APP_VERSION = "1.0.0"
REPO_URL = "https://github.com/microsoft/markitdown"

# Lunghezza massima dell'anteprima del markdown mostrata nel log (caratteri)
PREVIEW_MAX_CHARS = 2000

# Estensioni supportate da MarkItDown, usate per il filtro del file dialog
SUPPORTED_FILETYPES = [
    (
        "Tutti i formati supportati",
        "*.pdf *.docx *.pptx *.xlsx *.xls *.jpg *.jpeg *.png "
        "*.wav *.mp3 *.html *.htm *.csv *.json *.xml *.zip *.epub",
    ),
    ("PDF", "*.pdf"),
    ("Word (DOCX)", "*.docx"),
    ("PowerPoint (PPTX)", "*.pptx"),
    ("Excel (XLSX)", "*.xlsx"),
    ("Excel legacy (XLS)", "*.xls"),
    ("Immagini (JPG/PNG)", "*.jpg *.jpeg *.png"),
    ("Audio (WAV/MP3)", "*.wav *.mp3"),
    ("HTML", "*.html *.htm"),
    ("CSV", "*.csv"),
    ("JSON", "*.json"),
    ("XML", "*.xml"),
    ("Archivi ZIP", "*.zip"),
    ("EPUB", "*.epub"),
    ("Tutti i file", "*.*"),
]


def resource_path(relative_path: str) -> str:
    """Risolve il path di una risorsa sia in modalità script che da .exe PyInstaller.

    PyInstaller, quando crea un eseguibile --onefile, estrae le risorse in una
    cartella temporanea indicata da sys._MEIPASS: senza questa funzione l'icona
    non verrebbe trovata una volta compilato.
    """
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


class MarkItDownGUI:
    """Finestra principale dell'applicazione."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.input_path: str | None = None
        self.output_dir: str | None = None
        self.last_output_path: str | None = None
        self.use_same_folder = tk.BooleanVar(value=True)
        self.is_converting = False

        self._configure_window()
        self._build_ui()

    # ------------------------------------------------------------------
    # Costruzione interfaccia
    # ------------------------------------------------------------------
    def _configure_window(self) -> None:
        self.root.title(APP_TITLE)
        self.root.geometry("760x620")
        self.root.minsize(620, 480)
        try:
            self.root.iconbitmap(resource_path("icon.ico"))
        except Exception:
            # Se l'icona non è disponibile (es. ambiente non Windows) si
            # prosegue comunque con l'icona di default del sistema.
            pass

    def _build_ui(self) -> None:
        main_frame = ttk.Frame(self.root, padding=12)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(1, weight=1)

        style = ttk.Style()
        try:
            style.theme_use("vista")
        except tk.TclError:
            pass

        # --- Sezione selezione file -------------------------------------------------
        ttk.Label(main_frame, text="File da convertire:").grid(
            row=0, column=0, sticky="w", pady=(0, 6)
        )
        self.file_entry = ttk.Entry(main_frame, state="readonly")
        self.file_entry.grid(row=0, column=1, sticky="ew", padx=(8, 8), pady=(0, 6))
        ttk.Button(main_frame, text="Seleziona file...", command=self.select_file).grid(
            row=0, column=2, pady=(0, 6)
        )

        # --- Sezione cartella di output ----------------------------------------------
        ttk.Checkbutton(
            main_frame,
            text="Salva nella stessa cartella del file di origine",
            variable=self.use_same_folder,
            command=self._toggle_output_folder_state,
        ).grid(row=1, column=0, columnspan=3, sticky="w")

        ttk.Label(main_frame, text="Cartella output:").grid(
            row=2, column=0, sticky="w", pady=(4, 10)
        )
        self.output_entry = ttk.Entry(main_frame, state="readonly")
        self.output_entry.grid(row=2, column=1, sticky="ew", padx=(8, 8), pady=(4, 10))
        self.output_browse_btn = ttk.Button(
            main_frame, text="Sfoglia...", command=self.select_output_folder, state="disabled"
        )
        self.output_browse_btn.grid(row=2, column=2, pady=(4, 10))

        # --- Pulsante converti + barra di avanzamento --------------------------------
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        action_frame.columnconfigure(1, weight=1)

        self.convert_btn = ttk.Button(
            action_frame, text="Converti", command=self.start_conversion, state="disabled"
        )
        self.convert_btn.grid(row=0, column=0, sticky="w")

        self.progress = ttk.Progressbar(action_frame, mode="indeterminate")
        self.progress.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        # --- Area di log/output -------------------------------------------------------
        ttk.Label(main_frame, text="Log e anteprima:").grid(row=4, column=0, sticky="w")
        self.log_area = scrolledtext.ScrolledText(
            main_frame, height=18, wrap="word", state="disabled", font=("Consolas", 9)
        )
        self.log_area.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=(4, 10))
        main_frame.rowconfigure(5, weight=1)

        # --- Pulsanti post-conversione --------------------------------------------------
        post_frame = ttk.Frame(main_frame)
        post_frame.grid(row=6, column=0, columnspan=3, sticky="w", pady=(0, 10))
        self.open_folder_btn = ttk.Button(
            post_frame, text="Apri cartella output", command=self.open_output_folder, state="disabled"
        )
        self.open_folder_btn.pack(side=tk.LEFT, padx=(0, 8))
        self.open_file_btn = ttk.Button(
            post_frame, text="Apri file .md", command=self.open_md_file, state="disabled"
        )
        self.open_file_btn.pack(side=tk.LEFT)

        # --- Footer / Informazioni ------------------------------------------------------
        footer = ttk.Frame(main_frame)
        footer.grid(row=7, column=0, columnspan=3, sticky="ew", pady=(6, 0))
        footer.columnconfigure(0, weight=1)

        info_label = ttk.Label(
            footer,
            text=(
                "Basato su MarkItDown di Microsoft — https://github.com/microsoft/markitdown\n"
                "Realizzato da Leonardo Cozzolino"
            ),
            font=("Segoe UI", 8),
            foreground="#555555",
            justify="center",
            cursor="hand2",
        )
        info_label.grid(row=0, column=0, sticky="ew")
        info_label.bind("<Button-1>", lambda _e: self._open_repo_link())

        # Menu "Informazioni" come sezione About aggiuntiva
        menubar = tk.Menu(self.root)
        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="Informazioni su MarkItDown Converter", command=self._show_about)
        menubar.add_cascade(label="?", menu=help_menu)
        self.root.config(menu=menubar)

    # ------------------------------------------------------------------
    # Utility di logging
    # ------------------------------------------------------------------
    def _log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.configure(state="normal")
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state="disabled")

    def _clear_log(self) -> None:
        self.log_area.configure(state="normal")
        self.log_area.delete("1.0", tk.END)
        self.log_area.configure(state="disabled")

    def _show_about(self) -> None:
        messagebox.showinfo(
            "Informazioni",
            f"{APP_TITLE} v{APP_VERSION}\n\n"
            "Basato su MarkItDown di Microsoft\n"
            f"{REPO_URL}\n\n"
            "Realizzato da Leonardo Cozzolino",
        )

    def _open_repo_link(self) -> None:
        try:
            webbrowser.open(REPO_URL)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Selezione file e cartelle
    # ------------------------------------------------------------------
    def select_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Seleziona il file da convertire",
            filetypes=SUPPORTED_FILETYPES,
        )
        if not path:
            return

        self.input_path = path
        self._set_readonly_entry(self.file_entry, path)

        # Se l'utente non ha impostato una cartella personalizzata, mostra
        # comunque la cartella del file come anteprima della destinazione.
        if self.use_same_folder.get():
            self._set_readonly_entry(self.output_entry, str(Path(path).parent))

        self.convert_btn.configure(state="normal")
        self._reset_post_conversion_state()
        self._log(f"File selezionato: {path}")

    def select_output_folder(self) -> None:
        folder = filedialog.askdirectory(title="Seleziona la cartella di output")
        if not folder:
            return
        self.output_dir = folder
        self._set_readonly_entry(self.output_entry, folder)
        self._log(f"Cartella di output personalizzata: {folder}")

    def _toggle_output_folder_state(self) -> None:
        if self.use_same_folder.get():
            self.output_browse_btn.configure(state="disabled")
            if self.input_path:
                self._set_readonly_entry(self.output_entry, str(Path(self.input_path).parent))
        else:
            self.output_browse_btn.configure(state="normal")
            self._set_readonly_entry(self.output_entry, self.output_dir or "")

    @staticmethod
    def _set_readonly_entry(entry: ttk.Entry, value: str) -> None:
        entry.configure(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, value)
        entry.configure(state="readonly")

    def _reset_post_conversion_state(self) -> None:
        self.last_output_path = None
        self.open_folder_btn.configure(state="disabled")
        self.open_file_btn.configure(state="disabled")

    # ------------------------------------------------------------------
    # Conversione
    # ------------------------------------------------------------------
    def start_conversion(self) -> None:
        if self.is_converting:
            return
        if not self.input_path or not os.path.isfile(self.input_path):
            messagebox.showerror("Errore", "Seleziona prima un file valido da convertire.")
            return

        if self.use_same_folder.get():
            target_dir = Path(self.input_path).parent
        else:
            if not self.output_dir:
                messagebox.showerror("Errore", "Seleziona una cartella di output personalizzata.")
                return
            target_dir = Path(self.output_dir)

        self._clear_log()
        self._reset_post_conversion_state()
        self.is_converting = True
        self.convert_btn.configure(state="disabled")
        self.progress.start(12)
        self._log("Conversione in corso...")

        thread = threading.Thread(
            target=self._run_conversion, args=(self.input_path, target_dir), daemon=True
        )
        thread.start()

    def _run_conversion(self, input_path: str, target_dir: Path) -> None:
        """Eseguita in un thread separato per non bloccare la GUI."""
        try:
            # Import differito: se la libreria non è installata, l'errore
            # viene mostrato chiaramente solo al momento della conversione
            # e l'app può comunque avviarsi senza markitdown presente.
            from markitdown import (
                MarkItDown,
                FileConversionException,
                MissingDependencyException,
                UnsupportedFormatException,
            )

            md = MarkItDown()
            result = md.convert(input_path)
            content = getattr(result, "markdown", None) or getattr(result, "text_content", "") or ""

            target_dir.mkdir(parents=True, exist_ok=True)
            output_path = target_dir / (Path(input_path).stem + ".md")
            output_path.write_text(content, encoding="utf-8")

            self.root.after(0, self._on_conversion_success, str(output_path), content)

        except ImportError:
            self.root.after(
                0,
                self._on_conversion_error,
                "La libreria 'markitdown' non è installata.\n"
                "Esegui: pip install \"markitdown[all]\"",
            )
        except MissingDependencyException as e:
            self.root.after(
                0,
                self._on_conversion_error,
                "Dipendenza opzionale mancante per questo formato di file.\n"
                "Esegui: pip install \"markitdown[all]\"\n\n"
                f"Dettaglio: {e}",
            )
        except UnsupportedFormatException as e:
            self.root.after(0, self._on_conversion_error, f"Formato file non supportato.\n\nDettaglio: {e}")
        except FileConversionException as e:
            self.root.after(0, self._on_conversion_error, f"Errore durante la conversione del file.\n\nDettaglio: {e}")
        except FileNotFoundError as e:
            self.root.after(0, self._on_conversion_error, f"File non trovato.\n\nDettaglio: {e}")
        except Exception as e:
            self.root.after(
                0,
                self._on_conversion_error,
                f"Errore inatteso durante la conversione: {e}\n\n{traceback.format_exc()}",
            )

    def _on_conversion_success(self, output_path: str, content: str) -> None:
        self._end_conversion_ui()
        self.last_output_path = output_path
        self._log(f"Conversione completata. File salvato in: {output_path}")

        preview = content.strip()
        if len(preview) > PREVIEW_MAX_CHARS:
            preview = preview[:PREVIEW_MAX_CHARS] + "\n... (anteprima troncata, vedi il file .md completo)"
        self._log("--- Anteprima markdown ---")
        self._log(preview if preview else "(il file convertito è vuoto)")

        self.open_folder_btn.configure(state="normal")
        self.open_file_btn.configure(state="normal")

    def _on_conversion_error(self, message: str) -> None:
        self._end_conversion_ui()
        self._log(f"ERRORE: {message}")
        messagebox.showerror("Errore di conversione", message)

    def _end_conversion_ui(self) -> None:
        self.is_converting = False
        self.progress.stop()
        self.convert_btn.configure(state="normal")

    # ------------------------------------------------------------------
    # Apertura file/cartella risultato
    # ------------------------------------------------------------------
    def open_output_folder(self) -> None:
        if not self.last_output_path:
            return
        folder = str(Path(self.last_output_path).parent)
        self._open_with_system(folder)

    def open_md_file(self) -> None:
        if not self.last_output_path:
            return
        self._open_with_system(self.last_output_path)

    @staticmethod
    def _open_with_system(path: str) -> None:
        try:
            os.startfile(path)  # type: ignore[attr-defined]  # disponibile su Windows
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile aprire: {path}\n\n{e}")


def main() -> None:
    root = tk.Tk()
    MarkItDownGUI(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # rete di sicurezza per errori critici all'avvio
        # In modalità --windowed (exe compilato) non esiste una console
        # visibile: mostriamo comunque un messaggio d'errore all'utente.
        try:
            messagebox.showerror(APP_TITLE, f"Errore critico all'avvio:\n\n{exc}")
        except Exception:
            pass
        raise
