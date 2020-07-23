#!/bin/bash
set -euo pipefail

DEVEL_DIR=$HOME/Development
SOURCE_DIR=$HOME/Development
LOCAL_BIN=$HOME/.local/bin
DOT_REPO_DIR=$SOURCE_DIR/dot
PYTHON_VERSION=3.8.5
PYTHON2_VERSION=2.7.18
RUBY_VERSION=2.7.1
NODE_VERSION=14.5.0

mkdir -p $DEVEL_DIR
mkdir -p $SOURCE_DIR
mkdir -p $LOCAL_BIN

if [ ! -d $DOT_REPO_DIR ]; then
    git clone https://github.com/wiliamsouza/dot.git $DOT_REPO_DIR
    ##cd $DOT_REPO_DIR
    ##bash install.sh
    ##cd -
fi

echo "Install brew"
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

brew install wget neovim tree

echo "Installing pyenv"
git clone git://github.com/yyuu/pyenv.git $HOME/.pyenv
git clone git://github.com/concordusapps/pyenv-implict.git $HOME/.pyenv/plugins/pyenv-implict
export PYENV_ROOT=$HOME/.pyenv
export PATH=$PYENV_ROOT/bin:$PATH
eval "$(pyenv init -)"
pyenv install $PYTHON_VERSION
pyenv rehash
pyenv global $PYTHON_VERSION
wget --quiet -O - https://bootstrap.pypa.io/get-pip.py | python -
pip install virtualenv
pip install virtualenvwrapper
pip install pynvim
pip install pywal
pip install powerline-status

echo "Installing rbenv"
git clone https://github.com/sstephenson/rbenv.git $HOME/.rbenv
git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build
export RBENV_ROOT=$HOME/.rbenv
export PATH=$RBENV_ROOT/bin:$PATH
eval "$(rbenv init -)"
export PATH=$HOME/.rbenv/versions/$RUBY_VERSION/bin/:$PATH
rbenv install $RUBY_VERSION
rbenv rehash
rbenv global $RUBY_VERSION
gem install neovim
gem environment

echo "Installing nodenv"
git clone https://github.com/nodenv/nodenv.git ~/.nodenv
git clone https://github.com/nodenv/node-build.git ~/.nodenv/plugins/node-build
export PATH=$HOME/.nodenv/bin:$PATH
eval "$(nodenv init -)"
nodenv install $NODE_VERSION
nodenv rehash
nodenv global $NODE_VERSION
npm install --global  diff-so-fancy
npm install --global lerna
npm install -g neovim
