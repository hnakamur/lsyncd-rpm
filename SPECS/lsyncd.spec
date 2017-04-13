Name:           lsyncd
Version:        2.2.2
Release:        1%{?dist}
Summary:        File change monitoring and synchronization daemon
Group:          Applications/Internet
License:        GPLv2+
URL:            https://github.com/axkibe/lsyncd
Source0:        https://github.com/axkibe/%{name}/archive/release-%{version}.tar.gz#/%{name}-release-%{version}.tar.gz

# https://github.com/axkibe/lsyncd/issues/220
Patch0:         0001-Sanitize-mv-arguments.patch

Source1:        lsyncd.service
Source2:        lsyncd.init
Source3:        lsyncd.sysconfig
Source4:        lsyncd.logrotate
Source5:        lsyncd.conf

# files for el6
Source62:       lsyncd.init.el6
Source63:       lsyncd.sysconfig.el6
Source64:       lsyncd.logrotate.el6

%if 0%{?rhel}  == 7
BuildRequires:  lua-devel >= 5.1.3
BuildRequires:  asciidoc
Requires: lua
Requires: rsync

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

%if 0%{?rhel}  == 6
BuildRequires:  lua-devel >= 5.1.3
BuildRequires:  asciidoc
Requires: lua
Requires: rsync, openssh-clients

Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts
%endif

%description
Lsyncd watches a local directory trees event monitor interface (inotify).
It aggregates and combines events for a few seconds and then spawns one
(or more) process(es) to synchronize the changes. By default this is
rsync.

Lsyncd is thus a light-weight live mirror solution that is comparatively
easy to install not requiring new file systems or block devices and does
not hamper local file system performance.


%prep
%setup -q -n %{name}-release-%{version}
%patch0 -p1


%build
%if 0%{?rhel}  == 6
export CFLAGS="$RPM_OPT_FLAGS -fPIE"
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%endif
%configure
make %{?_smp_mflags}

%install
%if 0%{?rhel}  == 7
make install DESTDIR=%{buildroot}
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/lsyncd.service
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/lsyncd
install -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/lsyncd
install -p -D -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/
%endif

%if 0%{?rhel}  == 6
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -d 0755 %{buildroot}%{_initrddir} 
install -p -m 0755 %{SOURCE62} %{buildroot}%{_initrddir}/lsyncd
install -p -D -m 0644 %{SOURCE63} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -d -m 0755 %{buildroot}%{_localstatedir}/run/%{name}
install -d -m 0755 %{buildroot}%{_localstatedir}/log/%{name}
install -p -D -m 0644 %{SOURCE64} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if 0%{?rhel}  == 7
%systemd_post lsyncd.service
%endif

%if 0%{?rhel}  == 6
/sbin/chkconfig --add %{name}
%endif


%preun
%if 0%{?rhel}  == 7
%systemd_preun lsyncd.service
%endif

%if 0%{?rhel}  == 6
if [ "$1" -eq 0 ]; then
        /sbin/service %{name} stop >/dev/null 2>&1
        /sbin/chkconfig --del %{name}
fi
%endif

%postun
%if 0%{?rhel}  == 7
%systemd_postun_with_restart lsyncd.service
%endif

%if 0%{?rhel}  == 6
if [ "$1" -ge "1" ]; then
  /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi
%endif


%files
%if 0%{?rhel}  == 7
%doc %{_mandir}/man1/lsyncd.1*
%doc COPYING ChangeLog examples
%config(noreplace) %{_sysconfdir}/lsyncd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/lsyncd
%config(noreplace) %{_sysconfdir}/logrotate.d/lsyncd
%{_bindir}/lsyncd
%{_unitdir}/lsyncd.service
%exclude %{_docdir}/lsyncd
%endif

%if 0%{?rhel}  == 6
%defattr(-,root,root,-)
%{_mandir}/man1/lsyncd.1*
%doc COPYING ChangeLog examples
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0755,root,root) %{_initrddir}/%{name}
%dir %{_localstatedir}/run/%{name}
%dir %{_localstatedir}/log/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/lsyncd
%exclude %{_docdir}/lsyncd
%endif


%changelog
* Thu Apr 13 2017 Hiroaki Nakamura <hnakamur@gmail.com> - 2.2.2-1
- Update lsyncd to 2.2.2
- Merge spec files from lsyncd-2.1.5-6.el7.src.rpm and
  lsyncd-2.1.5-0.el6.src.rpm

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
