@echo off
setlocal enabledelayedexpansion

:: On verifie si au moins 3 arguments sont fournis
if "%~3"=="" (
    echo Usage: %~nx0 [-f|-d] [file_or_directory] [commit_message]
    exit /b 1
)

:: Arguments de la commande
set "   option=%~1"
set "target=%~2"
set "message=%~3"

:: Ajout du fichier/dossier comme option
if "%option%"=="-f" (
    git add "%target%"
) else if "%option%"=="-d" (
    git add "%target%"
) else (
    echo Option invalide. Utiliser -f pour un fichier ou -d pour un dossier.
    exit /b 1
)

:: Commit and push
git commit -m "%message%"
git push -u origin main


:: UTILISATION :
:: .\commit.bat -f nom_du_fichier "message de commit"
:: .\commit.bat -d nom_du_dossier "message de commit"
