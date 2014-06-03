Name:           timetracker
Version:        0.2.0
Release:        1
Summary:        Track sugar activities usage time

License:        GPLv2+
URL:            https://github.com/tchx84/timetracker
Source0:        %{name}-%{version}.tar.gz

Requires:       python >= 2.7, sugar >= 0.100

BuildArch:      noarch

%description
Service for tracking activities usage time, that also consider management events.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/sugar/extensions/webservice/
cp -r extensions/webservice/timetracker $RPM_BUILD_ROOT/%{_datadir}/sugar/extensions/webservice/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_datadir}/sugar/extensions/webservice/timetracker

%changelog
* Thu May 29 2014 Martin Abente Lahaye <tch@sugarlabs.org>
- initial package release
