# MarkItDown Converter

Applicazione desktop Windows con interfaccia grafica per convertire file in
Markdown, basata su [MarkItDown di Microsoft](https://github.com/microsoft/markitdown).

Realizzato da **Leonardo Cozzolino**.

Versione applicazione: **1.0.1** — motore Microsoft MarkItDown **0.1.7**.

## Download per utenti Windows

Scarica l'ultima versione dalla pagina
[Releases](https://github.com/mencoxx/MarkItDown-GUI/releases/latest).

1. Scarica il file `MarkItDownConverter-<versione>-Windows-x64.zip`.
2. Estrai lo ZIP in una cartella.
3. Avvia `MarkItDownConverter.exe`.

Non è necessario installare Python o altre dipendenze. Scarica l'eseguibile
soltanto dalla pagina Releases ufficiale di questo repository.

> L'eseguibile non è firmato digitalmente. Windows SmartScreen potrebbe quindi
> mostrare un avviso anche se il file proviene dal repository ufficiale.

## Formati supportati

PDF, DOCX, PPTX, XLSX, XLS, immagini (JPG/PNG), audio (WAV/MP3), HTML, CSV,
JSON, XML, ZIP, EPUB.

## Funzionalità

- Selezione del file da convertire tramite finestra di dialogo.
- Scelta della cartella di output (di default la stessa del file originale).
- Conversione locale tramite `convert_local()`, l'API più restrittiva indicata per file selezionati dal computer.
- Conversione eseguita in un thread separato: la finestra resta reattiva.
- Log di avanzamento e anteprima del Markdown generato.
- Pulsanti rapidi per aprire la cartella di output o il file `.md` prodotto.
- Messaggi di errore chiari per file non validi o dipendenze opzionali
  mancanti.

## Uso in locale (modalità script)

Richiede Python 3.10+. La versione di MarkItDown è fissata a `0.1.7` nel file `requirements.txt`, così installazioni e build utilizzano lo stesso motore verificato.

```bat
pip install -r requirements.txt
python main.py
```

## Generazione manuale dell'eseguibile

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

> La prima esecuzione di `build.bat` può richiedere alcuni minuti, perché
> `markitdown[all]` installa diverse librerie opzionali.

## Pubblicazione automatica di una versione

Il workflow GitHub Actions `windows-release.yml` legge `APP_VERSION` da
`main.py`. Dopo un aggiornamento del ramo `main`:

1. compila e verifica l'eseguibile su Windows;
2. crea automaticamente il tag `v<APP_VERSION>`, se non esiste;
3. pubblica la relativa GitHub Release;
4. allega `MarkItDownConverter-<versione>-Windows-x64.zip` e
   `SHA256SUMS.txt`.

Se la Release della versione indicata esiste già, non viene pubblicata
nuovamente. Per creare una nuova versione è quindi necessario aggiornare
`APP_VERSION` in `main.py` prima di integrare le modifiche in `main`.

Le pull request eseguono soltanto la build di controllo con permessi di lettura.
Il permesso di scrittura è riservato al job di pubblicazione sul ramo `main`.
Il workflow può anche essere avviato manualmente dalla scheda **Actions** per
produrre un artefatto di test senza pubblicare una nuova Release.

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
├── .github/workflows/   # build e pubblicazione automatica
├── main.py              # GUI + logica applicazione
├── requirements.txt     # markitdown[all], pyinstaller
├── build.bat            # script per generare l'exe con PyInstaller
├── icon.ico             # icona dell'applicazione
└── README.md            # questo file
```
