Summary:	A Curl-like tool for humans
Name:		httpie
Version:	0.7.2
Release:	1
License:	BSD
Group:		Applications/Networking
Source0:	http://pypi.python.org/packages/source/h/httpie/%{name}-%{version}.tar.gz
# Source0-md5:	09218336048596da757c4f0cf19642fd
URL:		http://httpie.org/
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
# Needed so we can build the manpage with help2man without fataling.
BuildRequires:	help2man
BuildRequires:	python-pygments
BuildRequires:	python-requests
Requires:	python-pygments
Requires:	python-requests
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HTTPie is a CLI HTTP utility built out of frustration with existing
tools. The goal is to make CLI interaction with HTTP-based services as
human-friendly as possible.

HTTPie does so by providing an http command that allows for issuing
arbitrary HTTP requests using a simple and natural syntax and
displaying colorized responses.

%prep
%setup -q

sed -i '/#!\%{_prefix}\/bin\/env/d' %{name}/__main__.py

# Fedora currently only ships with Pygments 1.4 but httpie wants 1.5.
# Also, RHEL currently only ships with Pygments 1.1.
# However, it seems to work just fine with lower versions.
sed -i 's/Pygments>=1.5/Pygments>=1.1/' setup.py
sed -i 's/requests>=2.0.0/requests>=1.1.0/' setup.py

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

export PYTHONPATH=$RPM_BUILD_ROOT%{py_sitescriptdir}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
help2man --no-discard-stderr $RPM_BUILD_ROOT%{_bindir}/http > $RPM_BUILD_ROOT%{_mandir}/man1/http.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%attr(755,root,root) %{_bindir}/http
%{_mandir}/man1/http.1*
%{py_sitescriptdir}/httpie
%{py_sitescriptdir}/httpie-%{version}-py*.egg-info
