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

sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'

nvim --headless +PlugInstall +qa
