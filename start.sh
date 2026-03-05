#!/bin/bash

# Par défaut, on considérera que l'utilisateur utilise une distribution basée Debian
DISTRO_TYPE="debian"

# On récupère les arguments depuis la console
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --distro-type) DISTRO_TYPE="$2"; shift ;;
        *) echo "Paramètre inconnu : $1"; exit 1 ;;
    esac
    shift
done

# Définition des paquets en fonction de la distro
declare -A PKG_MANAGER=(
    ["debian"]="apt install -y"
    ["fedora"]="dnf install -y"
    ["arch"]="pacman -S --noconfirm"
)

declare -A PKG_LIST=(
    ["debian"]="libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 qtwayland5 python3-pyqt5.qtwebengine libxcb-render-util0 libxcb-shape0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0 libegl1"
    ["fedora"]="libxcb-cursor libxcb-icccm libxcb-image libxcb-keysyms libxcb-randr qt5-qtwayland python3-qt5-webengine libxcb-render-util libxcb-shape libxcb-xinerama libxcb-xkb libxkbcommon-x11 libegl"
    ["arch"]="libxcb lib32-libxcb-cursor lib32-libxcb-icccm lib32-libxcb-image lib32-libxcb-keysyms lib32-libxcb-randr qt5-wayland python-pyqt5-webengine lib32-libxcb-render-util lib32-libxcb-shape lib32-libxcb-xinerama lib32-libxcb-xkb libxkbcommon-x11 lib32-libegl"
)

# Verification du support de la distro
if [[ -z "${PKG_MANAGER[$DISTRO_TYPE]}" ]]; then
    echo "Type de distribution non supporté : $DISTRO_TYPE. Utiliser 'debian', 'fedora', ou 'arch'."
    exit 1
fi

# Installation des paquets
echo "Installation des paquets pour $DISTRO_TYPE..."
sudo ${PKG_MANAGER[$DISTRO_TYPE]} ${PKG_LIST[$DISTRO_TYPE]}

# Lancement du python avec les variables environnement
QT_QPA_PLATFORM=xcb \
QTWEBENGINE_CHROMIUM_FLAGS="--no-sandbox" \
QT_DEBUG_PLUGINS=1 \
python3 sources/main.py 2>&1 | tail -n 15