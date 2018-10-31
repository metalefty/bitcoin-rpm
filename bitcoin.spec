%define		daemon_user	bitcoin
%define		daemon_group	bitcoin

Summary:	bitcoin
Name:		bitcoin
Version:	0.17.0
License:	MIT
Release:	1%{?dist}
URL:		https://bitcoincore.org
Source0:	https://bitcoin.org/bin/bitcoin-core-%{version}/bitcoin-%{version}.tar.gz

BuildRequires:	openssl-devel
BuildRequires:	boost-devel
BuildRequires:	libevent-devel
BuildRequires:	libdb-cxx-devel
BuildRequires:	qt5-qttools-devel
BuildRequires:	qt5-qtbase-devel
BuildRequires:	protobuf-devel

BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
bitcoin

%package cli
Summary:	Bitcoin cli
%description cli
bitcoin cli

%package daemon
Summary:	Bitcoin daemon
Requires:	systemd
%description daemon
bitcoin daemon

%package qt
Summary:	Bitcoin GUI
%description qt
bitcoin qt

%prep
%setup -q

%build
%configure \
	--with-incompatible-bdb \
	--without-libs \
	--with-gui=qt5
%{__make} %{?_smp_mflags}

%install
%{make_install}

mkdir -p %{buildroot}/%{_sysconfdir}/bitcoin
mkdir -p %{buildroot}/%{_sharedstatedir}/bitcoind
mkdir -p %{buildroot}/%{_unitdir}
cp -v %{_builddir}/bitcoin-%{version}/contrib/init/bitcoind.service %{buildroot}/%{_unitdir}/bitcoind.service

%{__install} -Dm644 %{_builddir}/bitcoin-%{version}/contrib/bitcoind.bash-completion \
	%{buildroot}%{_datarootdir}/bash-completion/completions/bitcoind
%{__install} -Dm644 %{_builddir}/bitcoin-%{version}/contrib/bitcoin-cli.bash-completion \
	%{buildroot}%{_datarootdir}/bash-completion/completions/bitcoin-cli
%{__install} -Dm644 %{_builddir}/bitcoin-%{version}/contrib/bitcoin-tx.bash-completion \
	%{buildroot}%{_datarootdir}/bash-completion/completions/bitcoin-tx


%post daemon
groupadd %{daemon_group}
useradd -r -g %{daemon_group} -s /sbin/nologin -d %{_sharedstatedir}/bitcoind %{daemon_group}
%systemd_post bitcoind.service

%postun daemon
%systemd_postun bitcoind.service

%files qt
%license COPYING
%{_bindir}/bitcoin-qt
%{_bindir}/test_bitcoin-qt
%{_mandir}/man1/bitcoin-qt.1.gz

%files cli
%license COPYING
%{_bindir}/bench_bitcoin
%{_bindir}/bitcoin-cli
%{_bindir}/bitcoin-tx
%{_bindir}/test_bitcoin
%{_mandir}/man1/bitcoin-cli.1.gz
%{_mandir}/man1/bitcoin-tx.1.gz
%{_datarootdir}/bash-completion/completions/bitcoin-cli
%{_datarootdir}/bash-completion/completions/bitcoin-tx

%files daemon
%{_bindir}/bitcoind
%{_unitdir}/bitcoind.service
%{_mandir}/man1/bitcoind.1.gz
%{_datarootdir}/bash-completion/completions/bitcoind
