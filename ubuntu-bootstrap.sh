#!/bin/bash

DEVEL_DIR=$HOME/Development
SOURCE_DIR=$HOME/Development
LOCAL_BIN=$HOME/.local/bin
DOT_REPO_DIR=$SOURCE_DIR/dot
PYTHON_VERION=3.7.3
RUBY_VERSION=2.6.3
GO_VERSION=1.12.4
DOCKER_COMPOSE_VERSION=1.24.0
TERRAFORM_VERSION=0.8.2

mkdir -p $DEVEL_DIR
mkdir -p $SOURCE_DIR
mkdir -p $LOCAL_BIN

sudo apt-get install -y git gnome-tweak-tool vim tmux screen \
    curl tree apt-transport-https ca-certificates  ack-grep \
    make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget python-dev \
    libyaml-dev xclip libpq-dev libxml2-dev libffi-dev neovim \
    libxslt1-dev zlib1g-dev jq silversearcher-ag fonts-powerline


echo "Installing docker-compose"
if [ ! -f $LOCAL_BIN/docker-compose ]; then
    curl -L https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-`uname -s`-`uname -m` > $LOCAL_BIN/docker-compose
    chmod +x $LOCAL_BIN/docker-compose
fi


if [ ! -d $DOT_REPO_DIR ]; then
    git clone https://github.com/wiliamsouza/dot.git $DOT_REPO_DIR
    cd $DOT_REPO_DIR
    bash install.sh
    cd -
fi

echo "Installing pyenv"
git clone git://github.com/yyuu/pyenv.git $HOME/.pyenv
git clone git://github.com/concordusapps/pyenv-implict.git $HOME/.pyenv/plugins/pyenv-implict
export PYENV_ROOT=$HOME/.pyenv
export PATH=$PYENV_ROOT/bin:$PATH
eval "$(pyenv init -)"
pyenv install $PYTHON_VERION
pyenv rehash
pyenv global $PYTHON_VERION
wget --quiet -O - https://bootstrap.pypa.io/get-pip.py | python -
pip install virtualenv
pip install virtualenvwrapper

echo "Installing golang"
wget --quiet -O - https://godeb.s3.amazonaws.com/godeb-amd64.tar.gz | tar zxvf - -C $HOME/.local/bin/
godeb install $GO_VERSION

echo "Intalling rbenv"
git clone https://github.com/sstephenson/rbenv.git $HOME/.rbenv
git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build
export RBENV_ROOT=$HOME/.rbenv
export PATH=$RBENV_ROOT/bin:$PATH
eval "$(rbenv init -)"
export PATH=$HOME/.rbenv/versions/$RUBY_VERSION/bin/:$PATH
rbenv install $RUBY_VERSION
rbenv rehash
rbenv global $RUBY_VERSION
