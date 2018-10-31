#!/bin/sh

SUDO="sudo -u btcbuild"
BITCOIN_VERSION=0.17.0
BUILD_USER=btcbuild
BUILD_GROUP=btcbuild

yum install -y shadow-utils sudo rpmdevtools wget

groupadd ${BUILD_GROUP}
useradd -g ${BUILD_GROUP} ${BUILD_GROUP}

yum groupinstall -y "Development Tools"
yum install -y $(grep BuildRequires bitcoin.spec | sed -e 's/BuildRequires://')

$SUDO rpmdev-setuptree
$SUDO wget -P ~btcbuild/rpmbuild/SOURCES https://bitcoincore.org/bin/bitcoin-core-${BITCOIN_VERSION}/bitcoin-${BITCOIN_VERSION}.tar.gz
$SUDO rpmbuild -ba /btcbuild/bitcoin.spec
