#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

wget https://ftp.gnu.org/gnu/emacs/emacs-29.1.tar.xz
tar xvf emacs-29.1.tar.xz

cd ${SCRIPT_DIR}/emacs-29.1
./configure
make
make install
