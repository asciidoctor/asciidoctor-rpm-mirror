%global gem_name asciidoctor
%global mandir %{_mandir}/man1

%define pre %nil

Summary: A fast, open source AsciiDoc implementation in Ruby
Name: rubygem-%{gem_name}
Version: 1.5.2
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/asciidoctor/asciidoctor
Source0: https://rubygems.org/gems/%{gem_name}-%{version}%{pre}.gem
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
BuildRequires: ruby(release)
%endif
%if 0%{?el6}
Requires: ruby(rubygems)
Requires: ruby(abi) = 1.8
BuildRequires: ruby(abi) = 1.8
%endif
BuildRequires: rubygems-devel
BuildRequires: ruby(rubygems)
%if 0%{?el6} || 0%{?el7}
# Dependencies aren't available on EPEL
%else
BuildRequires: rubygem(coderay)
BuildRequires: rubygem(erubis)
BuildRequires: rubygem(haml)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(nokogiri)
BuildRequires: rubygem(slim)
BuildRequires: rubygem(tilt)
%endif
BuildArch: noarch
Provides: asciidoctor = %{version}
%if 0%{?fc19} || 0%{?fc20} || 0%{?el6} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%if %{?pre:1}
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}%{pre}
%global gem_cache   %{gem_dir}/cache/%{gem_name}-%{version}%{pre}.gem
%global gem_spec    %{gem_dir}/specifications/%{gem_name}-%{version}%{pre}.gemspec
%global gem_docdir  %{gem_dir}/doc/%{gem_name}-%{version}%{pre}
%endif

%description
A fast, open source text processor and publishing toolchain, written in Ruby,
for transforming AsciiDoc markup into HTML 5, DocBook 4.5, DocBook 5.0 and
custom output formats. The transformation from AsciiDoc to custom output
formats is performed by running the nodes in the parsed document tree through a
collection of templates written in a template language supported by Tilt.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack -V %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version}%{pre}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Fix shebang (avoid Requires: /usr/bin/env)
sed -i -e 's|#!/usr/bin/env ruby|#!/usr/bin/ruby|' \
  bin/%{gem_name} bin/%{gem_name}-safe

# Clean up development-only file
rm Rakefile
sed -i "s|\"Rakefile\",||g" %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install -n %{gem_name}-%{version}%{pre}.gem

%check
%if 0%{?el6} || 0%{?el7}
# Asciidoctor tests require Minitest 5, so we can't run them on EPEL
%else
LANG=en_US.utf8 ruby -I"lib:test" test/*_test.rb
%endif

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

mkdir -p %{buildroot}%{_sysconfdir}/%{gem_name}
cp -pa .%{gem_instdir}/compat/* \
        %{buildroot}%{_sysconfdir}/%{gem_name}/

%files
%dir %{gem_instdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/benchmark
%exclude %{gem_instdir}/compat
%exclude %{gem_instdir}/man
%exclude %{gem_instdir}/test
%exclude %{gem_instdir}/features
%doc %{gem_instdir}/CHANGELOG.adoc
%doc %{gem_instdir}/LICENSE.adoc
%doc %{gem_instdir}/README.*
%{gem_instdir}/data
%{_bindir}/*
%{gem_instdir}/bin
%{gem_libdir}
%{mandir}/*
%{_sysconfdir}/%{gem_name}/*
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 05 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.2-1
- Update to Asciidoctor 1.5.2

* Fri Sep 19 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.1-1
- Update to Asciidoctor 1.5.1

* Tue Sep 09 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-1
- Update to Asciidoctor 1.5.0 final

* Fri Jun 06 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-0.4.preview.7
- Add %%{version} number to Provides: asciidoctor

* Fri Jun 06 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-0.3.preview.7
- Provide: asciidoctor
  https://github.com/asciidoctor/rubygem-asciidoctor-rpm/issues/5

* Tue May 20 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-0.2.preview.7
- Update to Asciidoctor 0.1.5.preview.7
- Drop unused patch

* Thu May 15 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-0.1.preview.6
- Update to Asciidoctor 0.1.5.preview.6
- Use HTTPS URLs
- Support Minitest 5
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Mark CHANGELOG, LICENSE, READMEs as %%doc
- Remove Rakefile in %%prep
- Remove Requires: /usr/bin/env

* Sun Sep 22 2013 Dan Allen <dan.j.allen@gmail.com> - 0.1.4-1
- Update to Asciidoctor 0.1.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 08 2013 Dan Allen <dan.j.allen@gmail.com> - 0.1.3-1
- Update to Asciidoctor 0.1.3

* Fri Mar 01 2013 Dan Allen <dan.j.allen@gmail.com> - 0.1.1-1
- Initial package
