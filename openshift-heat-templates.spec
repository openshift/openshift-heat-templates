Name: openshift-heat-templates
Version: 0.1.1.6
Release:       1%{?dist}
Summary: OpenShift Enterprise heat templates and DIB elements
Group: System Environment/Base
License: ASL 2.0
URL: https://github.com/openshift/enterprise-heat-templates
Source0: openshift-heat-templates-%{version}.tar.gz
BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch: noarch

%description
OpenShift Enterprise heat templates and image building elements

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -aR openshift-enterprise %{buildroot}%{_datadir}/%{name}/openshift-enterprise


%files
%doc README.md
%{_datadir}/%{name}

%changelog
* Tue Dec 16 2014 Chris Alfonso <calfonso@redhat.com> 0.1.1.6-1
- Resolves: rhbz#1161774 (calfonso@redhat.com)

* Wed Dec 10 2014 Chris Alfonso <calfonso@redhat.com> 0.1.1.5-1
- Resolves: rhbz#1172513, rhbz#1172563, rhbz#1172704 , rhbz#1172717
  (calfonso@redhat.com)

* Tue Dec 09 2014 Chris Alfonso <calfonso@redhat.com> 0.1.1.4-1
- Resolves: rhbz#1172064 (calfonso@redhat.com)
- Resolves: rhbz#1172060 (calfonso@redhat.com)

* Mon Dec 08 2014 Chris Alfonso <calfonso@redhat.com> 0.1.1.3-1
- BZ1167792 - rh_reg_pool should be a property of node1..3
  (calfonso@redhat.com)
- Fixed typo in allowed values (calfonso@redhat.com)
- Update README references to installed diskimage-builder package
  (calfonso@redhat.com)
- Use diskimage-builder package. Removed --skip-broken (calfonso@redhat.com)
- Updating hard coded OSE version to read environment variable.
  (calfonso@redhat.com)
- BZ1161777 - OpenShift Heat Templates don't demonstrate how to...
  (calfonso@redhat.com)
- BZ1164190 - networks/port should not be defined in yaml file
  (calfonso@redhat.com)

* Wed Oct 22 2014 Chris Alfonso <calfonso@redhat.com> 0.1.1.2-1
- new package built with tito

