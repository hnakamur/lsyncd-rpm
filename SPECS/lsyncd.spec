Name:           lsyncd
Version:        2.1.5
Release:        6%{?dist}
Summary:        File change monitoring and synchronization daemon
Group:          Applications/Internet
License:        GPLv2+
URL:            http://code.google.com/p/lsyncd/
Source0:        http://%{name}.googlecode.com/files/%{name}-%{version}.tar.gz

# https://github.com/axkibe/lsyncd/issues/220
Patch0:         0001-Sanitize-mv-arguments.patch

Source1:        lsyncd.service
Source2:        lsyncd.init
Source3:        lsyncd.sysconfig
Source4:        lsyncd.logrotate
Source5:        lsyncd.conf

BuildRequires:  lua-devel >= 5.1.3
BuildRequires:  asciidoc
Requires: lua
Requires: rsync

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Lsyncd watches a local directory trees event monitor interface (inotify).
It aggregates and combines events for a few seconds and then spawns one
(or more) process(es) to synchronize the changes. By default this is
rsync.

Lsyncd is thus a light-weight live mirror solution that is comparatively
easy to install not requiring new file systems or block devices and does
not hamper local file system performance.


%prep
%setup -q
%patch0 -p1


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/lsyncd.service
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/lsyncd
install -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/lsyncd
install -p -D -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/


%post
%systemd_post lsyncd.service


%preun
%systemd_preun lsyncd.service


%postun
%systemd_postun_with_restart lsyncd.service


%files
%doc %{_mandir}/man1/lsyncd.1*
%doc COPYING ChangeLog examples
%config(noreplace) %{_sysconfdir}/lsyncd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/lsyncd
%config(noreplace) %{_sysconfdir}/logrotate.d/lsyncd
%{_bindir}/lsyncd
%{_unitdir}/lsyncd.service
%exclude %{_docdir}/lsyncd


%changelog
* Tue Nov 18 2014 Lubomir Rintel <lkundrak@v3.sk> - 2.1.5-6
- Fix bad shell argument escaping

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 18 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.1.5-4
- No prelink on aarch64/ppc64le

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 24 2013 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 2.1.5-2
- Bulk sad and useless attempt at consistent SPEC file formatting

* Wed Oct  9 2013 Martin Langhoff <martin@laptop.org> - 2.1.5-1
- New upstream version
- adds rsync options: bwlimit, timeout
- several upstream fixes

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Paul Wouters <pwouters@redhat.com> - 2.1.4-3
- Comment out the LSYNCD_OPTIONS options per default, it accidentally
  caused the options from the initscript/systemd service to ignored

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 19 2012 Paul Wouters <pwouters@redhat.com> - 2.1.4-1
- Merged in changes of rhbz#805849
- Fixed URL/Source
- Upgraded systemd macros

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Apr 29 2011 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 2.0.4-1
- Initial packaging
