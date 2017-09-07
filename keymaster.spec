Name:           keymaster
Version:        0.4.3
Release:        1%{?dist}
Summary:        Short term access certificate generator and client

#Group:
License:        ASL 2.0
URL:            https://github.com/cviecco/simple-cloud-encrypt/
Source0:        keymaster-%{version}.tar.gz

#BuildRequires: golang
#Requires:
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel

#no debug package as this is go
%define debug_package %{nil}

%description
Simple utilites for checking state of ldap infrastructure


%prep
%setup -n %{name}-%{version}


%build
make


%install
#%make_install
%{__install} -Dp -m0755 ~/go/bin/keymasterd %{buildroot}%{_sbindir}/keymasterd
%{__install} -Dp -m0755 ~/go/bin/keymaster %{buildroot}%{_bindir}/keymaster
%{__install} -Dp -m0755 ~/go/bin/keymaster-unlocker %{buildroot}%{_bindir}/keymaster-unlocker
install -d %{buildroot}/usr/lib/systemd/system
install -p -m 0644 misc/startup/keymaster.service %{buildroot}/usr/lib/systemd/system/keymaster.service
install -d %{buildroot}/%{_datarootdir}/keymasterd/static_files/
install -p -m 0644 cmd/keymasterd/static_files/u2f-api.js  %{buildroot}/%{_datarootdir}/keymasterd/static_files/u2f-api.js
install -p -m 0644 cmd/keymasterd/static_files/keymaster-u2f.js  %{buildroot}/%{_datarootdir}/keymasterd/static_files/keymaster-u2f.js
install -p -m 0644 cmd/keymasterd/static_files/webui-2fa-u2f.js  %{buildroot}/%{_datarootdir}/keymasterd/static_files/webui-2fa-u2f.js
%pre
/usr/bin/getent passwd keymaster || useradd -d /var/lib/keymaster -s /bin/false -U -r  keymaster

%post
mkdir -p /etc/keymaster/
mkdir -p /var/lib/keymaster
chown keymaster /var/lib/keymaster
systemctl daemon-reload

%postun
/usr/sbin/userdel keymaster
systemctl daemon-reload

%files
#%doc
%{_sbindir}/keymasterd
%{_bindir}/keymaster
%{_bindir}/keymaster-unlocker
/usr/lib/systemd/system/keymaster.service
%{_datarootdir}/keymasterd/static_files/*

%changelog


