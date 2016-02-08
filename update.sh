#!/bin/bash

cd /var/www/bearicc.com

echo "Checking Bootstrap ..."
if [ -n "$(ls static|grep bootstrap-)" ]; then
    BOOTSTRAP_OLD_VERSION=$(ls -d ./static/bootstrap-*|grep -v zip|awk -F'/' '{print $NF}'|grep -Eo '[0-9.]+')
else
    BOOTSTRAP_OLD_VERSION=''
fi
BOOTSTRAP_NEW_VERSION=$(python3 -c 'from util import getBootstrapVesrion; print(getBootstrapVesrion())')
echo Current: $BOOTSTRAP_OLD_VERSION
if [[ $BOOTSTRAP_OLD_VERSION == $BOOTSTRAP_NEW_VERSION ]]; then
    echo Latest: $BOOTSTRAP_NEW_VERSION
    echo "Alreay latest"
else
    echo "Found new version: $BOOTSTRAP_NEW_VERSION"
    cd static
    rm -rf ./bootstrap*
    wget -q https://github.com/twbs/bootstrap/releases/download/v${BOOTSTRAP_NEW_VERSION}/bootstrap-${BOOTSTRAP_NEW_VERSION}-dist.zip
    7z x bootstrap-${BOOTSTRAP_NEW_VERSION}-dist.zip
    ln -s bootstrap-${BOOTSTRAP_NEW_VERSION}-dist bootstrap
    echo "Updated"
    cd ..
fi
