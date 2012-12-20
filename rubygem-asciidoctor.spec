%global gem_name asciidoctor
%global rubyabi 1.9.1

Summary: AsciiDoc implementation in Ruby that uses Tilt-supported templates to generate output
Name: rubygem-%{gem_name}
Version: 0.0.8
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/erebor/asciidoctor
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0: asciidoctor-modify-mocha-import.patch
Patch1: asciidoctor-disable-use-of-pending.patch
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems) 
Requires: ruby 
Requires: rubygem(tilt) 
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: rubygems-devel 
BuildRequires: ruby 
BuildRequires: rubygem(tilt)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(nokogiri)
BuildRequires: rubygem(htmlentities)
# using patch to comment lines where pending is used
#BuildRequires: rubygem(pending)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A pure-Ruby processor for parsing AsciiDoc documents or strings and rendering
them as HTML and other formats using Tilt-based templates.

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
%patch0 -p1
%patch1 -p1

%build
rdoc -o rdoc --charset=UTF-8

%check
LANG=en_US.utf8 testrb2 -Ilib test

%install
mkdir -p %{buildroot}%{gem_instdir}
cp -a lib \
        %{buildroot}%{gem_instdir}/

cp -a {LICENSE,README.asciidoc} \
        %{buildroot}%{gem_instdir}/

# Reenable when binary actually functions
#mkdir -p %{buildroot}%{_bindir}
#cp -a bin/* \
#        %{buildroot}%{_bindir}/
#find %{buildroot}/usr/bin -type f | xargs chmod a+x

#mkdir -p %{buildroot}%{gem_spec}/..
mkdir -p %{buildroot}%{gem_dir}/specifications
cp -a *.gemspec %{buildroot}%{gem_spec}

#mkdir -p %{buildroot}%{gem_cache}/..
mkdir -p %{buildroot}%{gem_dir}/cache
cp -a %{SOURCE0} %{buildroot}%{gem_cache}

mkdir -p %{buildroot}%{gem_docdir}/rdoc
cp -a rdoc/* \
         %{buildroot}%{gem_docdir}/rdoc

%files
%dir %{gem_instdir}
%{gem_instdir}/LICENSE
%{gem_instdir}/README.asciidoc
%{gem_libdir}
%{gem_cache}
%{gem_spec}
# Reenable when binary actually functions
#%{_bindir}/asciidoctor
#%{gem_instdir}/bin

%files doc
%doc %{gem_docdir}

%changelog
* Wed Dec 19 2012 Dan Allen <dan.j.allen@gmail.com> - 0.0.8-1
- Initial package
