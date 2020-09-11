#!/bin/bash

if hash brew 2>/dev/null; then
  echo Brew installed
else
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
fi

brew install neovim

mkdir -p ~/.config/nvim/

mv ./init.vim ~/.config/nvim/
mv ./coc-settings.json ~/.config/nvim/


nvim --headless +PlugInstall +qa
