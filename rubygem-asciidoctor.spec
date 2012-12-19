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
%setup -q -c -T
mkdir -p .%{gem_dir}
gem install --local --install-dir .%{gem_dir} \
            --bindir .%{_bindir} \
            --force %{SOURCE0}
%patch0 -p1 -d .%{gem_instdir}
%patch1 -p1 -d .%{gem_instdir}

%build
# TODO
#cd .%{gem_instdir}
#rdoc --charset=UTF-8
#cd -

%check
echo %{gem_spec}
LANG=en_US.utf8 testrb2 -b .%{gem_instdir} -Ilib test

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# TODO
#mkdir -p %{buildroot}%{gem_docdir}
#cp -a .%{gem_instdir}/doc/* \
#         %{buildroot}%{gem_docdir}/

%files
%dir %{gem_instdir}
%{_bindir}/asciidoctor
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/test
%exclude %{gem_instdir}/noof.rb
%exclude %{gem_instdir}/%{gem_name}.gemspec
# following exclude is necessary if you have rubygems-bundler installed
%exclude /usr/share/gems/bin/ruby_noexec_wrapper
%{gem_spec}

%files doc
# TODO
#%doc %{gem_docdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.asciidoc

%changelog
* Wed Dec 19 2012 Dan Allen <dan.j.allen@gmail.com> - 0.0.8-1
- Initial package
