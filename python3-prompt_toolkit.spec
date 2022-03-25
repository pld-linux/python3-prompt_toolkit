#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module	prompt_toolkit
Summary:	Library for building powerful interactive command lines in Python
Summary(pl.UTF-8):	Biblioteka do budowania interaktywnych wierszy poleceń w Pythonie
Name:		python3-%{module}
Version:	3.0.5
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://github.com/prompt-toolkit/python-prompt-toolkit/releases
Source0:	https://github.com/jonathanslenders/python-prompt-toolkit/archive/%{version}/python-prompt-toolkit-%{version}.tar.gz
# Source0-md5:	b1a2403b503177ddb5873630123fd533
URL:		https://github.com/jonathanslenders/python-prompt-toolkit
BuildRequires:	python3-modules >= 1:3.6.1
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-wcwidth
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python3-modules >= 1:3.6.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
prompt_toolkit is a library for building powerful interactive command
lines and terminal applications in Python.

%description -l pl.UTF-8
prompt_toolkit to biblioteka do tworzenia interaktywnych wierwszy
poleceń i aplikacji terminalowych w Pythonie.

%package apidocs
Summary:	API documentation for prompt_toolkit module
Summary(pl.UTF-8):	Dokumentacja API modułu prompt_toolkit
Group:		Documentation

%description apidocs
API documentation for prompt_toolkit module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu prompt_toolkit.

%prep
%setup -q -n python-prompt-toolkit-%{version}

%build
%py3_build

%if %{with tests}
# test_print_tokens expects sequences emitted for xterm
TERM=xterm \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|/usr/bin/env python|%{__python3}|'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG LICENSE README.rst
%{py3_sitescriptdir}/prompt_toolkit
%{py3_sitescriptdir}/prompt_toolkit-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,pages,*.html,*.js}
%endif
