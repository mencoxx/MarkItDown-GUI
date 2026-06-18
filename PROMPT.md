# PROMPT PER CLAUDE CODE — MarkItDown Desktop Converter

## Obiettivo
Crea un'applicazione desktop Windows standalone (eseguibile .exe) che fornisca un'interfaccia grafica semplice per convertire file in Markdown usando la libreria Python `markitdown` di Microsoft (https://github.com/microsoft/markitdown).

## Requisiti funzionali

1. **Interfaccia grafica** (usa `tkinter`, incluso di default in Python, per evitare dipendenze pesanti):
   - Pulsante "Seleziona file" che apre una finestra di dialogo per scegliere il file da convertire.
   - Filtro file dialog limitato ai formati supportati da MarkItDown: PDF, DOCX, PPTX, XLSX, XLS, immagini (JPG/PNG), audio (WAV/MP3), HTML, CSV, JSON, XML, ZIP, EPUB.
   - Campo/etichetta che mostra il percorso del file selezionato.
   - Pulsante "Converti" che esegue la conversione tramite la libreria `markitdown` e salva il risultato come `.md` (stesso nome del file originale, stessa cartella o cartella scelta dall'utente).
   - Area di log/output che mostra lo stato (in corso, completato, errore) e in caso di successo un'anteprima del markdown generato.
   - Pulsante "Apri cartella output" / "Apri file .md" al termine della conversione.
   - Gestione errori chiara a video (es. dipendenza mancante per un formato, file non valido).

2. **Branding nell'interfaccia**:
   - Titolo finestra: "MarkItDown Converter"
   - Nel footer o in una sezione "Informazioni"/About della GUI, includere testo visibile:
     - "Basato su MarkItDown di Microsoft — https://github.com/microsoft/markitdown"
     - "Realizzato da Leonardo Cozzolino"

3. **Logica di conversione**:
   - Usa la libreria `markitdown` come dipendenza Python (`pip install 'markitdown[all]'`), import `from markitdown import MarkItDown`, istanzia `MarkItDown()` e chiama `.convert(percorso_file)`, poi scrivi `result.text_content` (o `result.markdown`) su file `.md`.
   - Esegui la conversione in un thread separato per non bloccare la GUI.

4. **Packaging come eseguibile**:
   - Usa `PyInstaller` per generare un singolo `.exe` standalone (`--onefile --windowed`).
   - Includi un'icona se disponibile, altrimenti icona di default.
   - Verifica che le dipendenze opzionali necessarie di MarkItDown (pdf, docx, pptx, xlsx, xls) siano incluse nel bundle/nell'ambiente virtuale usato per il build.
   - Fornisci uno script di build (`build.bat` o comando PyInstaller) pronto all'uso.

## Struttura progetto richiesta

```
markitdown-gui/
├── main.py              # GUI + logica applicazione
├── requirements.txt     # markitdown[all], pyinstaller
├── build.bat            # script per generare l'exe con PyInstaller
├── icon.ico             # icona (opzionale, placeholder se non fornita)
└── README.md            # istruzioni per uso e build
```

## Vincoli tecnici
- Python 3.10+ compatibile.
- Nessuna chiamata di rete necessaria per la conversione (tutto locale), tranne dipendenze opzionali di markitdown stesse se richiedono modelli (es. OCR) — in caso, gestiscilo via try/except con messaggio chiaro.
- Codice pulito, commentato in italiano dove utile, gestione eccezioni robusta.
- Il file `main.py` deve essere eseguibile sia in modalità script (`python main.py`) che una volta compilato in `.exe`.

## Output atteso da Claude Code
1. Crea tutti i file della struttura sopra elencata nella working directory corrente.
2. Implementa `main.py` completo e funzionante.
3. Mostra il comando per testare in locale (`python main.py`) e quello per generare l'eseguibile (`build.bat`).
4. Non non chiedere conferma, ma generare tutta i file richiesta

L'gpp deve essere a app deve esserea runtime portabile, deve includere l'gp Python e embedded, deve includere lo runtime Python embedded e per le sue dipendenze in modo che l'untente non debba installar nulla.
