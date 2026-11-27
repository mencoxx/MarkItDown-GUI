# MarkItDown Converter

<p align="center">
  <strong>Converti PDF, Word, PowerPoint, Excel e altri file in Markdown su Windows.</strong><br>
  Nessun comando da usare. Nessuna installazione di Python.
</p>

<p align="center">
  <a href="https://github.com/mencoxx/MarkItDown-GUI/releases/latest">
    <img src="https://img.shields.io/github/v/release/mencoxx/MarkItDown-GUI?label=Scarica%20per%20Windows&logo=windows&logoColor=white" alt="Scarica per Windows">
  </a>
  <a href="https://github.com/mencoxx/MarkItDown-GUI/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/mencoxx/MarkItDown-GUI" alt="Licenza">
  </a>
  <a href="https://github.com/microsoft/markitdown">
    <img src="https://img.shields.io/badge/basato%20su-Microsoft%20MarkItDown-5c2d91" alt="Basato su Microsoft MarkItDown">
  </a>
</p>

Applicazione desktop gratuita e open source, realizzata da **Leonardo Cozzolino**,
per trasformare documenti e file multimediali in Markdown tramite una semplice
interfaccia grafica.

## Download rapido

[**Scarica MarkItDown Converter per Windows**](https://github.com/mencoxx/MarkItDown-GUI/releases/latest)

1. Scarica il file `MarkItDownConverter-<versione>-Windows-x64.zip`.
2. Estrai il file ZIP in una cartella.
3. Avvia `MarkItDownConverter.exe`.

Non devi installare Python, pip o altre librerie.

> Windows SmartScreen potrebbe mostrare un avviso perché l'eseguibile non è
> firmato digitalmente. Il file ufficiale è pubblicato nella pagina Releases di
> questo repository.

## A cosa serve

MarkItDown Converter è pensato per chi deve usare i contenuti dei propri file
in strumenti di AI, sistemi di ricerca, knowledge base o applicazioni che
lavorano meglio con testo strutturato.

La conversione viene eseguita localmente sul computer: i file selezionati non
vengono caricati su un servizio esterno dalla GUI.

## Formati supportati

- PDF
- Word `.docx`
- PowerPoint `.pptx`
- Excel `.xlsx` e `.xls`
- Immagini `.jpg`, `.jpeg`, `.png`
- Audio `.wav`, `.mp3`
- HTML
- CSV
- JSON
- XML
- ZIP
- EPUB

## Funzionalità

- selezione del file tramite finestra di dialogo;
- scelta della cartella di output;
- conversione locale con l'API restrittiva `convert_local()`;
- interfaccia reattiva durante la conversione;
- log di avanzamento;
- anteprima del Markdown generato;
- apertura rapida della cartella o del file prodotto;
- messaggi chiari in caso di formato non supportato o dipendenze mancanti.

## Utilizzo

Dopo aver avviato il programma:

1. premi **Seleziona file**;
2. scegli il documento da convertire;
3. scegli eventualmente una cartella di output;
4. premi **Converti**;
5. apri il file Markdown generato.

## Versione attuale

- Applicazione: **1.0.2**
- Motore Microsoft MarkItDown: **0.1.9**
- Sistema operativo: **Windows x64**

## Uso in locale per sviluppatori

Richiede Python 3.10 o superiore.

Le versioni sono fissate in `requirements.txt` per rendere riproducibili
installazione e build:

- MarkItDown `0.1.9`
- PyInstaller `6.22.3`

```bat
pip install -r requirements.txt
python main.py
```

## Generazione manuale dell'eseguibile

Lo script `build.bat` crea un ambiente virtuale di build e genera un
eseguibile standalone:

```bat
build.bat
```

L'output viene creato in:

```
dist\\MarkItDownConverter.exe
```

## Pubblicazione automatica

Il workflow GitHub Actions:

- verifica ogni pull request;
- compila l'eseguibile su Windows;
- crea ZIP e checksum SHA-256;
- pubblica automaticamente una nuova Release quando cambia `APP_VERSION`
  in `main.py`.

## Progetto originale

Il motore di conversione è [MarkItDown di Microsoft](https://github.com/microsoft/markitdown).

## Licenza

Il progetto è distribuito con la licenza presente nel file
[LICENSE](https://github.com/mencoxx/MarkItDown-GUI/blob/main/LICENSE).
