Name: openshift-heat-templates
Version: 0.1.1.2
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
* Wed Oct 22 2014 Chris Alfonso <calfonso@redhat.com> 0.1.1.2-1
- new package built with tito

