#!/bin/sh

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# zsh
brew install zsh
if [ "$(uname -m)" == "arm64" ]; then
    chsh -s /opt/homebrew/bin/zsh
    echo "export PATH=/opt/homebrew/bin:$PATH" > ~/.zshrc
    source ~/.zshrc
else 
    chsh -s /usr/local/bin/zsh
fi

# python
brew install pyenv
