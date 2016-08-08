#!/bin/bash

DEVEL_DIR=$HOME/devel
SOURCE_DIR=$HOME/source
LOCAL_BIN=$HOME/.local/bin
DOT_REPO_DIR=$SOURCE_DIR/dot
PYTHON_VERION=3.5.2
RUBY_VERSION=2.3.1
GO_VERSION=1.6.3

mkdir -p $DEVEL_DIR
mkdir -p $SOURCE_DIR
mkdir -p $LOCAL_BIN

sudo apt-get install -y openssh-server git gnome-tweak-tool vim tmux screen \
    curl tree apt-transport-https ca-certificates  ack-grep \
    make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget python-dev ipython \
    libyaml-dev bzr mercurial linux-image-extra-$(uname -r)

echo "Installing docker-compose"
if [ ! -f $LOCAL_BIN/docker-compose ]; then
    curl -L https://github.com/docker/compose/releases/download/1.8.0/docker-compose-`uname -s`-`uname -m` > $LOCAL_BIN/docker-compose
    chmod +x $LOCAL_BIN/docker-compose
fi

echo "Installing docker"
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get purge -y lxc-docker
sudo apt-get install -y docker-engine
sudo systemctl enable docker
sudo usermod --append --groups docker $USER
echo "Your user was added to docker group."
echo "To this change take place you need to login again."

if [ ! -d $DOT_REPO_DIR ]; then
    git clone https://github.com/wiliamsouza/dot.git $DOT_REPO_DIR
    cd $DOT_REPO_DIR
    bash install.sh
    cd -
fi

echo "Installing vim plugins"
mkdir -p $HOME/.vim/bundle
git clone https://github.com/VundleVim/Vundle.vim.git $HOME/.vim/bundle/Vundle.vim

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

echo "Installing powerline"
pip install git+git://github.com/Lokaltog/powerline
mkdir -p $HOME/.fonts
mkdir -p $HOME/.fonts.conf.d
curl -LSso $HOME/.fonts/PowerlineSymbols.otf \
    https://github.com/Lokaltog/powerline/raw/develop/font/PowerlineSymbols.otf
curl -LSso $HOME/.fonts.conf.d/10-powerline-symbols.conf \
    https://github.com/Lokaltog/powerline/raw/develop/font/10-powerline-symbols.conf
fc-cache -vf $HOME/.fonts

echo "Installing terraform"
if [ ! -f $HOME/.local/bin/terraform ]; then
    wget --quiet -O $HOME/.local/bin/terraform.zip https://releases.hashicorp.com/terraform/0.7.0/terraform_0.7.0_linux_amd64.zip
    cd $HOME/.local/bin/
    unzip terraform.zip
    cd -
fi

echo "Installing heroku toolbelt"
wget --quiet -O - https://toolbelt.heroku.com/install-ubuntu.sh | sudo sh

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

echo "Installing terraforming"
gem install terraforming
