#!/bin/bash

DEVEL_DIR=$HOME/devel
SOURCE_DIR=$HOME/source
LOCAL_BIN=$HOME/.local/bin
DOT_REPO_DIR=$SOURCE_DIR/dot

mkdir -p $DEVEL_DIR
mkdir -p $SOURCE_DIR
mkdir -p $LOCAL_BIN

sudo yum -y install screen gnome-tweak-tool vim python-flake8 \
    curl tree python-pip python-virtualenvwrapper python-virtualenv-clone\
    python-tox python-virtualenv make automake gcc gcc-c++ openssl-devel \
    zlib-devel bzip2-devel readline-devel libsqlite3x-devel wget llvm \
    python-jedi python-devel python-ipdb ipython libyaml-devel

echo "Installing fig"
pip install --user fig

echo "Installing docker"
#sudo yum install docker-io -y
#sudo usermod --append --groups docker $USER
#exec sudo su -l $USER
echo "Your user was added to docker group."
echo "To this change take place you need to login again."


git clone https://github.com/wiliamsouza/dot.git $DOT_REPO_DIR
pushd $DOT_REPO_DIR
bash install.sh
popd
source $HOME/.bashrc

echo "Installing vim plugins"
mkdir -p $HOME/.vim/autoload
mkdir -p $HOME/.vim/bundle

curl -LSso $HOME/.vim/autoload/pathogen.vim \
    https://raw.github.com/tpope/vim-pathogen/master/autoload/pathogen.vim

git clone https://github.com/honza/dockerfile.vim.git \
    $HOME/.vim/bundle/dockerfile.vim

git clone https://github.com/nvie/vim-flake8 \
     $HOME/.vim/bundle/vim-flake8

git clone https://github.com/plasticboy/vim-markdown.git \
    $HOME/.vim/bundle/vim-markdown

git clone git://github.com/tpope/vim-fugitive.git \
    $HOME/.vim/bundle/vim-fugitive

git clone https://github.com/scrooloose/nerdtree.git \
    $HOME/.vim/bundle/nerdtree

echo "Intalling rbenv"
git clone https://github.com/sstephenson/rbenv.git $HOME/.rbenv

echo "Installing pyenv"
git clone git://github.com/yyuu/pyenv.git $HOME/.pyenv
git clone git://github.com/concordusapps/pyenv-implict.git $HOME/.pyenv/plugins/pyenv-implict
pyenv install 2.7.6
pyenv install 3.4.1
pyenv install pypy-2.3
pyenv rehash

echo "Installing powerline"
pip install --user git+git://github.com/Lokaltog/powerline
mkdir -p $HOME/.fonts
mkdir -p $HOME/.fonts.conf.d
curl -LSso $HOME/.fonts/PowerlineSymbols.otf \
    https://github.com/Lokaltog/powerline/raw/develop/font/PowerlineSymbols.otf
curl -LSso $HOME/.fonts.conf.d/10-powerline-symbols.conf \
    https://github.com/Lokaltog/powerline/raw/develop/font/10-powerline-symbols.conf
fc-cache -vf $HOME/.fonts

echo "Installing git-flow-completion"
mkdir -p $HOME/.bash_completion.d
curl -LSso $HOME/.bash_completion.d/git-flow-completion.bash \
    https://raw.githubusercontent.com/bobthecow/git-flow-completion/master/git-flow-completion.bash
source $HOME/.bash_completion.d/git-flow-completion.bash
