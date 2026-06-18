@echo off
setlocal

:: ================================================================
:: build.bat - MarkItDown Converter
:: Crea un eseguibile .exe standalone e portabile con PyInstaller.
:: L'exe generato include l'interprete Python (embedded) e tutte
:: le dipendenze necessarie: sul PC di destinazione non serve
:: installare Python, pip o alcuna libreria.
:: ================================================================

set VENV_DIR=.venv_build
set APP_NAME=MarkItDownConverter

echo [1/5] Verifica Python...
where python >nul 2>nul
if errorlevel 1 (
    echo ERRORE: Python non trovato nel PATH. Installa Python 3.10+ e riprova.
    exit /b 1
)

echo [2/5] Creazione ambiente virtuale di build "%VENV_DIR%"...
if not exist "%VENV_DIR%" (
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ERRORE: creazione ambiente virtuale fallita.
        exit /b 1
    )
)

call "%VENV_DIR%\Scripts\activate.bat"

echo [3/5] Installazione dipendenze (markitdown[all], pyinstaller)...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRORE: installazione dipendenze fallita.
    call "%VENV_DIR%\Scripts\deactivate.bat"
    exit /b 1
)

echo [4/5] Pulizia build precedenti...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "%APP_NAME%.spec" del /q "%APP_NAME%.spec"

echo [5/5] Generazione eseguibile standalone con PyInstaller...
pyinstaller --onefile --windowed --noconfirm --clean ^
    --name "%APP_NAME%" ^
    --icon "icon.ico" ^
    --add-data "icon.ico;." ^
    --collect-all markitdown ^
    --collect-all magika ^
    --collect-all onnxruntime ^
    main.py

if errorlevel 1 (
    echo ERRORE: build PyInstaller fallita.
    call "%VENV_DIR%\Scripts\deactivate.bat"
    exit /b 1
)

call "%VENV_DIR%\Scripts\deactivate.bat"

echo.
echo ================================================================
echo  Build completata con successo!
echo  Eseguibile portabile generato in: dist\%APP_NAME%.exe
echo  Copialo dove vuoi: non richiede Python installato sul PC di
echo  destinazione (interprete e dipendenze sono incluse nell'exe).
echo ================================================================

endlocal
