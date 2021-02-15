#!/bin/bash

if hash brew 2>/dev/null; then
  echo Brew installed
else
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
fi

if hash nvim 2>/dev/null; then
  echo nvim installed
else
  brew install neovim
fi

mkdir -p ~/.config/nvim/

cp ./init.vim ~/.config/nvim/
cp ./coc-settings.json ~/.config/nvim/

FILE=~/.local/share/nvim/site/autoload/plug.vim

if test -f $FILE; then
  echo "Plug installed"
else
  sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
fi

nvim --headless +PlugInstall +qa
