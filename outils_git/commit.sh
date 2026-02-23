#!/bin/bash

# On verifie si au moins 3 arguments sont fournis
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 [-f|-d] <file_or_directory> <commit_message>"
    exit 1
fi

# Arguments de la commande
option=$1
target=$2
message=$3

# Ajouter fichier/dossier comme option
if [ "$option" = "-f" ]; then
    git add "$target"
elif [ "$option" = "-d" ]; then
    git add "$target"
else
    echo "Option invalide. Use -f pour un fichier ou -d pour un dossier."
    exit 1
fi

# Commit and push
git commit -m "$message"
git push -u origin main


# UTILISATION : 
# ./commit.sh -f nom_du_fichier "message de commit"
# ./commit.sh -d nom_du_dossier "message de commit"
