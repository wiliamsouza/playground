#!/bin/bash
set -euo pipefail

DEVEL_DIR=$HOME/Development
SOURCE_DIR=$HOME/Development
LOCAL_BIN=$HOME/.local/bin
DOT_REPO_DIR=$SOURCE_DIR/dot
PYTHON_VERION=3.12.3
PYTHON2_VERION=2.7.18
RUBY_VERSION=3.3.1
GO_VERSION=1.22.2
NODE_VERSION=22.1.0
DOCKER_COMPOSE_VERSION=2.27.0

mkdir -p $DEVEL_DIR
mkdir -p $SOURCE_DIR
mkdir -p $LOCAL_BIN

##sudo add-apt-repository -y ppa:neovim-ppa/stable
sudo apt-get update

sudo apt-get install -y git gnome-tweaks vim tmux screen \
    curl tree apt-transport-https ca-certificates ack \
    make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget python3-dev \
    libyaml-dev xclip libpq-dev libxml2-dev libffi-dev neovim \
    libxslt1-dev zlib1g-dev jq silversearcher-ag fonts-powerline \
    i3 inotify-tools imagemagick feh cpu-checker \
    qemu-system-x86 libvirt-daemon-system libvirt-clients bridge-utils \
    fzy lzma liblzma-dev libbz2-dev flatpak gnome-software-plugin-flatpak

#echo "Configuring quemu"
#sudo adduser `id -un` libvirt
#sudo adduser `id -un` kvm

echo "Installing docker-compose"
if [ ! -f $LOCAL_BIN/docker-compose ]; then
    curl -L https://github.com/docker/compose/releases/download/v$DOCKER_COMPOSE_VERSION/docker-compose-`uname -s`-`uname -m` > $LOCAL_BIN/docker-compose
    chmod +x $LOCAL_BIN/docker-compose
fi

echo "Installing docker"
sudo addgroup --system docker
sudo adduser $USER docker
sudo snap install docker

if [ ! -d $DOT_REPO_DIR ]; then
    git clone https://github.com/wiliamsouza/dot.git $DOT_REPO_DIR
    cd $DOT_REPO_DIR
    bash install.sh
    cd -
fi

echo "Installing pyenv"
git clone https://github.com/pyenv/pyenv.git $HOME/.pyenv
git clone https://github.com/pyenv/pyenv-implicit.git $HOME/.pyenv/plugins/pyenv-implict
export PYENV_ROOT=$HOME/.pyenv
export PATH=$PYENV_ROOT/bin:$PATH
eval "$(pyenv init -)"
pyenv install $PYTHON_VERION
pyenv rehash
pyenv global $PYTHON_VERION
python -m ensurepip --upgrade
python -m pip install tk-tools
pip install virtualenv
pip install virtualenvwrapper
pip install pynvim
pip install pywal
pip install powerline-status

echo "Installing golang"
wget --quiet -O - https://godeb.s3.amazonaws.com/godeb-amd64.tar.gz | tar zxvf - -C $LOCAL_BIN
export PATH=$HOME/.local/bin:$PATH
godeb install $GO_VERSION

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
