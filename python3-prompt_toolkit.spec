#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module	prompt_toolkit
Summary:	Library for building powerful interactive command lines in Python
Summary(pl.UTF-8):	Biblioteka do budowania interaktywnych wierszy poleceń w Pythonie
Name:		python3-%{module}
Version:	3.0.52
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://github.com/prompt-toolkit/python-prompt-toolkit/releases
Source0:	https://github.com/prompt-toolkit/python-prompt-toolkit/archive/%{version}/python-prompt-toolkit-%{version}.tar.gz
# Source0-md5:	f5ea9f7ebf37994a2a17512c5de727af
URL:		https://github.com/prompt-toolkit/python-prompt-toolkit
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools >= 1:68
%if %{with tests}
BuildRequires:	python3-wcwidth
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-pyperclip
BuildRequires:	python3-sphinx_copybutton >= 0.5.2
BuildRequires:	python3-sphinx_nefertiti >= 0.8.6
BuildRequires:	python3-wcwidth
BuildRequires:	sphinx-pdg-3 >= 8
%endif
Requires:	python3-modules >= 1:3.8
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
%py3_build_pyproject

%if %{with tests}
# test_print_tokens expects sequences emitted for xterm
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
TERM=xterm \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|/usr/bin/env python|%{__python3}|'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG LICENSE PROJECTS.rst README.rst
%{py3_sitescriptdir}/prompt_toolkit
%{py3_sitescriptdir}/prompt_toolkit-%{version}.dist-info
%{_examplesdir}/python3-%{module}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,pages,*.html,*.js}
%endif
