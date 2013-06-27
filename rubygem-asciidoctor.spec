%global gemname asciidoctor

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global mandir %{_mandir}/man1
%global rubyabi 1.8

Summary: AsciiDoc implementation in Ruby
Name: rubygem-%{gemname}
Version: 0.1.3
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/asciidoctor/asciidoctor
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
# Patch0: disables use of pending statement in the test suite The required gem,
# pending, is not packaged in Fedora and since the statement is merely a task
# note, it's safe to disable it's usage for the purpose of packaging.
Patch0: asciidoctor-disable-use-of-pending.patch
# Patch1: disables CodeRay tests since the library is not available in el6
Patch1: asciidoctor-disable-coderay-tests.patch
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems)
BuildRequires: ruby 
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems)
BuildRequires: rubygem(erubis)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(nokogiri)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
An open source text processor and publishing toolchain written in Ruby for
converting AsciiDoc markup into HTML 5, DocBook 4.5 and custom formats. Export
to custom formats is performed by running the nodes of the parsed tree through
a collection of Tilt-supported templates.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack -V %{SOURCE0}
%setup -q -D -T -n %{gemname}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gemname}.gemspec
%patch0 -p1
%patch1 -p1
gem build %{gemname}.gemspec
mkdir -p .%{gemdir}
gem install --local --install-dir .%{gemdir} \
            --bindir .%{_bindir} \
            --force %{SOURCE0}

%build

%check
LANG=en_US.utf8 testrb -Ilib test/*_test.rb

%install
mkdir -p %{buildroot}%{gemdir}
cp -pa .%{gemdir}/* \
        %{buildroot}%{gemdir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{mandir}
cp -pa .%{geminstdir}/man/*.1 \
        %{buildroot}%{mandir}/

mkdir -p %{buildroot}%{_sysconfdir}/%{gemname}
cp -pa .%{geminstdir}/compat/* \
        %{buildroot}%{_sysconfdir}/%{gemname}/

%files
%dir %{geminstdir}
%exclude %{gemdir}/cache/%{gemname}-%{version}.gem
%exclude %{geminstdir}/%{gemname}.gemspec
%exclude %{geminstdir}/Gemfile
%exclude %{geminstdir}/Guardfile
%exclude %{geminstdir}/Rakefile
%exclude %{geminstdir}/compat
%exclude %{geminstdir}/man
%exclude %{geminstdir}/test
%{geminstdir}/LICENSE
%{geminstdir}/README.*
%{_bindir}/*
%{geminstdir}/bin
%{geminstdir}/lib
%{mandir}/*
%{_sysconfdir}/%{gemname}/*
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/LICENSE

%changelog
* Thu Jun 27 2013 Jimmi Dyson <jimmidyson@gmail.com> - 0.1.3-1
- Fix packaging for EL6
* Sat Jun 08 2013 Dan Allen <dan.j.allen@gmail.com> - 0.1.3-1
- Update to Asciidoctor 0.1.3
* Fri Mar 01 2013 Dan Allen <dan.j.allen@gmail.com> - 0.1.1-1
- Initial package
