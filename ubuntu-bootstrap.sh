#!/bin/bash

DEVEL_DIR=$HOME/devel
SOURCE_DIR=$HOME/source
LOCAL_BIN=$HOME/.local/bin
DOT_REPO_DIR=$SOURCE_DIR/dot
PYTHON_VERION=3.6.0
RUBY_VERSION=2.4.0
GO_VERSION=1.7.4
DOCKER_COMPOSE_VERSION=1.9.0
TERRAFORM_VERSION=0.8.2

mkdir -p $DEVEL_DIR
mkdir -p $SOURCE_DIR
mkdir -p $LOCAL_BIN

sudo apt-get install -y git gnome-tweak-tool vim tmux screen \
    curl tree apt-transport-https ca-certificates  ack-grep \
    make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget python-dev \
    libyaml-dev linux-image-extra-$(uname -r) xclip vagrant virtualbox \
    libpq-dev libxml2-dev libxslt1-dev zlib1g-dev jq silversearcher-ag


echo "Installing docker-compose"
if [ ! -f $LOCAL_BIN/docker-compose ]; then
    curl -L https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-`uname -s`-`uname -m` > $LOCAL_BIN/docker-compose
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
vim +PluginInstall +qall

echo "Installing system powerline"
wget --quiet -O - https://bootstrap.pypa.io/get-pip.py | sudo /urs/bin/python3.5 -
sudo /usr/bin/pip3.5 install git+git://github.com/Lokaltog/powerline

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
wget --quiet -O - https://bootstrap.pypa.io/get-pip.py | sudo python -
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
    wget --quiet -O $HOME/.local/bin/terraform.zip https://releases.hashicorp.com/terraform/$TERRAFORM_VERSION/terraform_$TERRAFORM_VERSION_linux_amd64.zip
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

echo "Installing kubernetes"
curl -sS https://get.k8s.io | bash
export KUBERNETES_PROVIDER=vagrant
export KUBERNETES_MASTER_MEMORY=1536
export KUBERNETES_NODE_MEMORY=4096
cd kubernetes
#./cluster/kube-up.sh

echo "Instaling deis CLI"
if [ ! -f $HOME/.local/bin/deis ]; then
    curl -sSL http://deis.io/deis-cli/install-v2.sh | bash
    sudo mv $PWD/deis $HOME/.local/bin/
fi

echo "Installing helm"
curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash

echo "Installing tmate"
sudo apt-get install software-properties-common && \
    sudo add-apt-repository ppa:tmate.io/archive && \
    sudo apt-get update && \
    sudo apt-get install tmate


echo "Installing ngrok"
if [ ! -f $HOME/.local/bin/ngrok ]; then
    wget --quiet -O $HOME/.local/bin/ngrok.zip https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
    cd $HOME/.local/bin/
    unzip ngrok.zip
    cd -
fi

echo "Installing ok.sh"
if [ ! -f $HOME/.local/bin/ok.sh ]; then
    wget --quiet -O $HOME/.local/bin/ok.sh.zip https://github.com/whiteinge/ok.sh/archive/0.2.2.zip
    cd $HOME/.local/bin/
    unzip ok.sh.zip
    cd -
fi

echo "Installing glide"
curl https://glide.sh/get | sh
