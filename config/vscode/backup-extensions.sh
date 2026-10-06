#!/bin/sh

echo "Saving VSCode extensions..."
code --list-extensions > "$HOME"/dotfilesrc/vscode/extensions.txt
