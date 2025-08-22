# Lit-gen

Program, který slouží k jenoduché tvorbě literárních rozborů knih. 

## Build info

1. Naklonujte repozitář pomocí `git clone https://github.com/j0hner/Lit-gen`
2. Poté lze Lit-gen lze spustit 2 způsoby:
    1. jako přiložený .exe soubor
    2. přímo v pythonu:
         - Je třeba mít instalovaný python ([microsoft store](https://apps.microsoft.com/detail/9pnrbtzxmb4z) nebo [python.org](https://www.python.org/downloads/))
         - Je třeba instalovat jinja2 (`pip install Jinja2`)
         - Poté pomocí Run.lnk nebé `Python main.py`

Pokud si chcete .exe soubor sestavit sami; použijte pyinstaller: `pyinstaller --onefile --add-data "template.tex;." --add-data "icon.ico;." --icon=icon.ico --name "Lit-gen" --windowed main.py`

## Jak to funguje

<img width="681" height="554" alt="Formulář" src="https://github.com/user-attachments/assets/68805e18-d51e-429e-a507-d0a5e85fcc8c" />

Vyplňte pole formuláře údaji o knize a stiskněte 'Vytvořit PDF'

.pdf soubor obsahující rozbor a další soubory využité při jeho tvorbě najdete ve vybrané výstupní složce