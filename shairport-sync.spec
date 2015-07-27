Name:		shairport-sync
Version:	2.3.7
Release:	1%{?dist}
Summary:	AirTunes emulator. Shairport Sync adds multi-room capability with Audio Synchronisation

Group:		Applications/Multimedia
License:	GPL
URL:		https://github.com/mikebrady/shairport-sync
Source0:	https://github.com/mikebrady/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:		shairport-sync-systemd.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libconfig-devel
BuildRequires:	popt-devel
BuildRequires:	openssl-devel
BuildRequires:	libdaemon-devel
BuildRequires:	avahi-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	systemd-units
BuildRequires:	soxr-devel
Requires:	popt
Requires:	openssl
Requires:	avahi
Requires:	libdaemon
Requires:	alsa-lib
Requires:	soxr

%description
Shairport Sync emulates an AirPort Express for the purpose of streaming audio from iTunes, iPods, iPhones, iPads and AppleTVs. Audio played by a Shairport Sync-powered device stays synchronised with the source and hence with similar devices playing the same source. Thus, for example, synchronised multi-room audio is possible without difficulty. (Hence the name Shairport Sync, BTW.)

Shairport Sync does not support AirPlay video or photo streaming.

%prep
%setup -q
%patch0 -p1

%build
autoreconf -i -f
%configure --with-avahi --with-alsa --with-ssl=openssl --with-soxr --without-initscript
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
rm %{buildroot}/etc/shairport-sync.conf.sample

%pre
getent group %{name} &>/dev/null || groupadd --system %{name} >/dev/null
getent passwd %{name} &> /dev/null || useradd --system -c "%{name} User" \
	-d %{_localstatedir}/%{name} -m -g %{name} -s /sbin/nologin \
	-G audio %{name} >/dev/null

%files
%config /etc/shairport-sync.conf
/usr/bin/shairport-sync
/usr/share/man/man7/shairport-sync.7.gz
%{_unitdir}/%{name}.service
%doc AUTHORS LICENSES README.md

%changelog
* Fri Jul 24 2015 Bill Peck <bill@pecknet.com> 2.3.7-1
- Initial spec file
