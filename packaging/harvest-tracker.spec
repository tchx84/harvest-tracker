Name:           harvest-tracker
Version:        0.0.1
Release:        1
Summary:        Adjust activities usage time based on system events

License:        GPLv2+
URL:            https://github.com/tchx84/harvest-tracker
Source0:        %{name}-%{version}.tar.gz

Requires:       python >= 2.7, sugar >= 0.100

BuildArch:      noarch

%description
Service for adjusting Sugar Activities usage time tracking, based on system events.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/sugar/extensions/webservice/
cp -r extensions/webservice/tracker $RPM_BUILD_ROOT/%{_datadir}/sugar/extensions/webservice/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_datadir}/sugar/extensions/webservice/tracker

%changelog
* Thu May 29 2014 Martin Abente Lahaye <tch@sugarlabs.org>
- initial package release
