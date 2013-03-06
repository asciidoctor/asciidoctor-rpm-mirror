%global gem_name asciidoctor
%global mandir %{_mandir}/man1

Summary: AsciiDoc implementation in Ruby
Name: rubygem-%{gem_name}
Version: 0.1.1
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/asciidoctor/asciidoctor
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Patch0: disables use of pending statement in the test suite The required gem,
# pending, is not packaged in Fedora and since the statement is merely a task
# note, it's safe to disable it's usage for the purpose of packaging.
Patch0: asciidoctor-disable-use-of-pending.patch
# Patch1: works around nth-child selector bug in Nokogiri
Patch1: asciidoctor-fix-nth-child-selectors.patch
%if 0%{?fedora} <= 18
Requires: ruby(abi) = 1.9.1
BuildRequires: ruby(abi) = 1.9.1
%else
Requires: ruby(release)
BuildRequires: ruby(release)
%endif
Requires: ruby(rubygems)
BuildRequires: rubygems-devel
BuildRequires: ruby(rubygems)
BuildRequires: rubygem(coderay)
BuildRequires: rubygem(erubis)
BuildRequires: rubygem(htmlentities)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(nokogiri)
# using patch to comment lines where pending is used
#BuildRequires: rubygem(pending)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A pure AsciiDoc implementation in Ruby for parsing AsciiDoc source files and
strings and then rendering them as HTML, DocBook or other formats using the
built-in ERB templates or a set of custom Tilt-supported template files.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack -V %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%patch0 -p1
%patch1 -p1

%build
gem build %{gem_name}.gemspec
%gem_install

%check
LANG=en_US.utf8 testrb -Ilib test/*_test.rb

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{mandir}
cp -pa .%{gem_instdir}/man/*.1 \
        %{buildroot}%{mandir}/

%files
%dir %{gem_instdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/%{gem_name}.gemspec
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/test
%exclude %{gem_instdir}/man
%{gem_instdir}/LICENSE
%{gem_instdir}/README.*
%{_bindir}/*
%{gem_instdir}/bin
%{gem_libdir}
%{mandir}/*
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Fri Mar 01 2013 Dan Allen <dan.j.allen@gmail.com> - 0.1.1-1
- Initial package
