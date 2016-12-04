%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           leftokill
Version:        0.1.1
Release:        4%{?dist}.srce
Summary:        Unix daemon that cleans processes/threads left by the job scheduler
Group:          System Environment/Daemons
License:        GPL
URL:            https://github.com/vrdel/leftokill 
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch 
BuildRequires:  python2-devel
Requires:       python-psutil >= 4.3
Requires:       python-daemon
Requires:       python-argparse

%description
Unix daemon that cleans the processes/threads left by the job scheduler

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT --record=INSTALLED_FILES
install --directory --mode 755 $RPM_BUILD_ROOT/%{_localstatedir}/log/%{name}/
install --directory --mode 755 $RPM_BUILD_ROOT/%{_localstatedir}/run/%{name}/

%post
/sbin/chkconfig --add leftokill

%preun
if [ "$1" = 0 ]; then
  /sbin/service leftokill stop > /dev/null 2>&1
  /sbin/chkconfig --del leftokill
fi
exit 0

%postun
rm -rf %{_localstatedir}/run/%{name}/

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/%{name}/%{name}.conf
%dir %{python_sitelib}/%{name}/
%dir %{_localstatedir}/log/%{name}/
%dir %{_localstatedir}/run/%{name}/
%{python_sitelib}/%{name}/*.py[co]

%changelog
* Sun Dec 4 2016 Daniel Vrcic <dvrcic@srce.hr> - 0.1.1-4%{?dist}
- created time + pid as key in report structure
* Sat Nov 26 2016 Daniel Vrcic <dvrcic@srce.hr> - 0.1.1-3%{?dist}
- removed SMTP SSL
- only root execute
* Sat Nov 19 2016 Daniel Vrcic <dvrcic@srce.hr> - 0.1.1-2%{?dist}
- cleanup stale pidfile lock
- fix handling of empty exclude options
- init script returns proper exit codes
- remove pidfile dir on pkg uninstall
- complain if no logger defined
* Fri Nov 18 2016 Daniel Vrcic <dvrcic@srce.hr> - 0.1.1-1%{?dist}
- num of leftovers in subject
- use created time as key in leftovers structure
* Fri Nov 4 2016 Daniel Vrcic <dvrcic@srce.hr> - 0.1.0-1%{?dist}
- initial version
