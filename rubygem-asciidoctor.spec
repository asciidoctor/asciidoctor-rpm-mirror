%global gem_name asciidoctor

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
A pure AsciiDoc implementation in Ruby that can parse AsciiDoc files or strings
and render them as HTML, DocBook and other output formats using Tilt-supported
templates.

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
mkdir -p .%{gem_dir}

gem build %{gem_name}.gemspec

gem install -V \
  --local \
  --install-dir .%{gem_dir} \
  --bindir .%{_bindir} \
  --force \
  --rdoc \
  %{gem_name}-%{version}.gem

%check
LANG=en_US.utf8 testrb -Ilib test/*_test.rb

%install
mkdir -p %{buildroot}%{gem_instdir}
cp -a .%{gem_instdir}/{LICENSE,README.asciidoc} %{buildroot}%{gem_instdir}/

mkdir -p %{buildroot}%{gem_libdir}
cp -a .%{gem_libdir}/* %{buildroot}%{gem_libdir}

mkdir -p %{buildroot}%{gem_docdir}
cp -a .%{gem_docdir}/* %{buildroot}%{gem_docdir}

mkdir -p %{buildroot}%{gem_dir}/specifications
cp -a .%{gem_spec} %{buildroot}%{gem_spec}

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

%files
%dir %{gem_instdir}
%{gem_instdir}/LICENSE
%{gem_instdir}/README.asciidoc
%{gem_libdir}
%{_bindir}/asciidoctor
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Fri Mar 01 2013 Dan Allen <dan.j.allen@gmail.com> - 0.1.1-1
- Initial package
