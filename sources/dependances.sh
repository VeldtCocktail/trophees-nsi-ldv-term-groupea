#!/bin/bash

#!/bin/bash

# Detect distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
    DISTRO_LIKE=$ID_LIKE
else
    echo "Distribution non supportée."
    exit 1
fi

# Define packages based on distro
DEBIAN_PKGS="python3-venv python3-pip libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 qtwayland5 python3-pyqt5.qtwebengine libxcb-render-util0 libxcb-shape0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0 libegl1"
FEDORA_PKGS="python3-venv python3-pip libxcb-cursor libxcb-icccm libxcb-image libxcb-keysyms libxcb-randr qt5-qtwayland python3-qt5-webengine libxcb-render-util libxcb-shape libxcb-xinerama libxcb-xkb libxkbcommon-x11 libegl"
ARCH_PKGS="python python-pip libxcb lib32-libxcb-cursor lib32-libxcb-icccm lib32-libxcb-image lib32-libxcb-keysyms lib32-libxcb-randr qt5-wayland python-pyqt5-webengine lib32-libxcb-render-util lib32-libxcb-shape lib32-libxcb-xinerama lib32-libxcb-xkb libxkbcommon-x11 lib32-libegl"

# Install system dependencies
case "$DISTRO" in
    ubuntu|debian|kali|linuxmint)
        echo "Détection de $DISTRO (Debian-like)..."
        sudo apt update
        sudo apt install -y $DEBIAN_PKGS
        ;;
    fedora|rhel|centos)
        echo "Détection de $DISTRO (RedHat-like)..."
        sudo dnf install -y $FEDORA_PKGS
        ;;
    arch|manjaro)
        echo "Détection de $DISTRO (Arch-like)..."
        sudo pacman -S --noconfirm --needed $ARCH_PKGS
        ;;
    *)
        if [[ "$DISTRO_LIKE" == *"debian"* ]]; then
            echo "Détection via ID_LIKE: $DISTRO_LIKE (Debian-like)..."
            sudo apt update
            sudo apt install -y $DEBIAN_PKGS
        else
            echo "Distribution $DISTRO non supportée pour l'installation automatique des paquets système."
            echo "Veuillez installer manuellement les dépendances pour PyQt5 et WebEngine."
        fi
        ;;
esac

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to project root to ensure relative paths work
cd "$PROJECT_ROOT" || exit 1

# Virtual environment setup
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Création de l'environnement virtuel dans $PROJECT_ROOT/$VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

echo "Mise à jour de l'environnement virtuel..."
source "$VENV_DIR/bin/activate"
python3 -m pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    # Handle UTF-16LE requirements.txt if necessary
    if file requirements.txt | grep -q "UTF-16LE"; then
        echo "Conversion de requirements.txt (UTF-16LE -> UTF-8)..."
        iconv -f UTF-16LE -t UTF-8 requirements.txt > requirements_utf8.txt
        python3 -m pip install -r requirements_utf8.txt
        rm requirements_utf8.txt
    else
        python3 -m pip install -r requirements.txt
    fi
else
    echo "Fichier requirements.txt non trouvé dans $PROJECT_ROOT."
fi


echo "Installation terminée !"