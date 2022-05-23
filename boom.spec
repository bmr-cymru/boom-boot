%global summary A set of libraries and tools for managing boot loader entries
%global sphinx_docs 1

Name:		boom-boot
Version:	1.3
Release:	1%{?dist}
Summary:	%{summary}

License:	GPLv2
URL:		https://github.com/snapshotmanager/boom
#Source0:	https://github.com/snapshotmanager/boom/archive/%{version}.tar.gz
Source0:	boom-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:  make
BuildRequires:	python3-setuptools
BuildRequires:	python3-devel
%if 0%{?sphinx_docs}
BuildRequires:  python3-dbus
BuildRequires:	python3-sphinx
%endif

Requires: python3-boom = %{version}-%{release}
Requires: %{name}-conf = %{version}-%{release}

Obsoletes: boom-grub2 <= 1.3

%package -n python3-boom
Summary: %{summary}
%{?python_provide:%python_provide python3-boom}
Requires: python3
Recommends: (lvm2 or brtfs-progs)
Recommends: %{name}-conf = %{version}-%{release}

# There used to be a boom package in fedora, and there is boom packaged in
# copr. How to tell which one is installed? We need python3-boom and no boom
# only.
Conflicts: boom

%package conf
Summary: %{summary}

%description
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the BLS patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

%description -n python3-boom
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the BLS patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

This package provides python3 boom module.

%description conf
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the BLS patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

This package provides configuration files for boom.

%prep
%setup -q -n boom-%{version}
# NOTE: Do not use backup extension - MANIFEST.in is picking them

%build
%if 0%{?sphinx_docs}
make -C doc html
rm doc/_build/html/.buildinfo
mv doc/_build/html doc/html
rm -r doc/_build
%endif

%py3_build

%install
%py3_install

# Make configuration directories
# mode 0700 - in line with /boot/grub2 directory:
install -d -m 700 ${RPM_BUILD_ROOT}/boot/boom/profiles
install -d -m 700 ${RPM_BUILD_ROOT}/boot/boom/hosts
install -d -m 700 ${RPM_BUILD_ROOT}/boot/loader/entries
install -d -m 700 ${RPM_BUILD_ROOT}/boot/boom/cache
install -m 644 examples/boom.conf ${RPM_BUILD_ROOT}/boot/boom

mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man8
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man5
install -m 644 man/man8/boom.8 ${RPM_BUILD_ROOT}/%{_mandir}/man8
install -m 644 man/man5/boom.5 ${RPM_BUILD_ROOT}/%{_mandir}/man5

rm doc/Makefile
rm doc/conf.py

# Test suite currently does not operate in rpmbuild environment
#%%check
#%%{__python3} setup.py test

%files
%license COPYING
%doc README.md
%{_bindir}/boom
%doc %{_mandir}/man*/boom.*

%files -n python3-boom
%license COPYING
%doc README.md
%{python3_sitelib}/*
%doc doc
%doc examples
%doc tests

%files conf
%license COPYING
%doc README.md
%dir /boot/boom
%config(noreplace) /boot/boom/boom.conf
%dir /boot/boom/profiles
%dir /boot/boom/hosts
%dir /boot/boom/cache
%dir /boot/loader/entries


%changelog
* Thu Jan 28 2021 Bryn M. Reeves <bmr@redhat.com> = 1.3
- Check for duplicates consistently in the clone and edit commands
- Apply correct command line precedence to --add-opts and --del-opts
- Correctly merge multiple --add/del-opts when editing or cloning
- Correctly propagate --add/del-opts in boom edit commands
- Enhanced logging of --add/del-opts merge logic
- The default Python interpreter is now /usr/bin/python
- Fixed re-ordering of options modifications when read from disk
- Do not set BootParams attributes for anonymous option words
- Make lvm_root_lv validation checks more strict
- Improve BootParams.from_entry() parameter recovery debug logging
- Include sample OsProfile for Fedora 32
- Re-set sandbox state in test suite to ensure run-to-run consistency
- Improve compatibility with Red Hat BLS implementation
- Allow non-boom managed entries to be listed and displayed
- Handle quirks in Red Hat's use of the BLS machine_id key
- Allow grub2 bootloader variables to be expanded when cloning entries
- Simplify clone_entry logic and make consistent with edit_entry
- Ensure stable ordering of legacy boot entry configuration

* Wed May 13 2020 Bryn M. Reeves <bmr@redhat.com> = 1.1
- Bump release

* Tue May 12 2020 Bryn M. Reeves <bmr@redhat.com> = 1.1-0.1.beta
- Bump release

* Mon May 11 2020 Bryn M. Reeves <bmr@redhat.com> - 1.0-2
- Include boom/cache directory in package

* Wed Nov 27 2019 Bryn M. Reeves <bmr@redhat.com> - 1.0-1
- Bump release for boom-1.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0-0.5.20190329git6ff3e08
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0-0.4.20190329git6ff3e08
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.3.20190329git6ff3e08
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 09 2019 Marian Csontos <mcsontos@redhat.com> 1.0-0.2.20190329git6ff3e08
- Fix packaging issues.

* Thu May 09 2019 Marian Csontos <mcsontos@redhat.com> 1.0-0.1.20190329git6ff3e08
- Pre-release of new version.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 17 2018 Marian Csontos <mcsontos@redhat.com> 0.9-4
- Change dependencies.

* Mon Jul 16 2018 Marian Csontos <mcsontos@redhat.com> 0.9-3
- Split executable, python module and configuration.

* Wed Jun 27 2018 Marian Csontos <mcsontos@redhat.com> 0.9-2
- Spin off grub2 into subpackage

* Wed Jun 27 2018 Marian Csontos <mcsontos@redhat.com> 0.9-1
- Update to new upstream 0.9.
- Fix boot_id caching.

* Fri Jun 08 2018 Marian Csontos <mcsontos@redhat.com> 0.8.5-6.2
- Remove example files from /boot/boom/profiles.

* Fri May 11 2018 Marian Csontos <mcsontos@redhat.com> 0.8.5-6.1
- Files in /boot are treated as configuration files.

* Thu Apr 26 2018 Marian Csontos <mcsontos@redhat.com> 0.8.5-6
- Package upstream version 0.8-5.6

