# MarkItDown Converter

Applicazione desktop Windows con interfaccia grafica per convertire file in
Markdown, basata su [MarkItDown di Microsoft](https://github.com/microsoft/markitdown).

Realizzato da **Leonardo Cozzolino**.

## Formati supportati

PDF, DOCX, PPTX, XLSX, XLS, immagini (JPG/PNG), audio (WAV/MP3), HTML, CSV,
JSON, XML, ZIP, EPUB.

## Funzionalità

- Selezione del file da convertire tramite finestra di dialogo.
- Scelta della cartella di output (di default la stessa del file originale).
- Conversione eseguita in un thread separato: la finestra resta reattiva.
- Log di avanzamento e anteprima del Markdown generato.
- Pulsanti rapidi per aprire la cartella di output o il file `.md` prodotto.
- Messaggi di errore chiari per file non validi o dipendenze opzionali
  mancanti.

## Uso in locale (modalità script)

Richiede Python 3.10+.

```bat
pip install -r requirements.txt
python main.py
```

## Generazione dell'eseguibile standalone (.exe)

Lo script `build.bat` crea automaticamente un ambiente virtuale di build,
installa le dipendenze e genera un eseguibile **portabile e standalone**
con PyInstaller:

```bat
build.bat
```

Al termine, l'eseguibile si trova in:

```
dist\MarkItDownConverter.exe
```

Questo file include l'interprete Python (embedded) e tutte le librerie
necessarie (markitdown, magika, onnxruntime, ecc.): può essere copiato e
lanciato su un altro PC Windows **senza installare Python, pip o alcuna
dipendenza**.

> Nota: la prima esecuzione di `build.bat` può richiedere alcuni minuti,
> perché `markitdown[all]` installa diverse librerie opzionali (motore di
> rilevamento formato, parsing PDF/Office, ecc.).

## Note su dipendenze opzionali

- La conversione di file audio può richiedere `ffmpeg` installato nel
  sistema per l'estrazione/transcodifica; in sua assenza l'app mostra un
  errore chiaro invece di bloccarsi.
- Se per un determinato formato manca una libreria opzionale di MarkItDown,
  l'app mostra un messaggio con l'indicazione del comando
  `pip install "markitdown[all]"` da eseguire (utile solo in modalità
  script: l'eseguibile compilato con `build.bat` le include già tutte).

## Struttura del progetto

```
markitdown-gui/
├── main.py              # GUI + logica applicazione
├── requirements.txt     # markitdown[all], pyinstaller
├── build.bat            # script per generare l'exe con PyInstaller
├── icon.ico             # icona dell'applicazione
└── README.md            # questo file
```
