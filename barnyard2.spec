
# Conditional build:
%bcond_without  mysql		# don't build support for MySQL
%bcond_without	postgresql	# don't build support for PostgreSQL

%define		subver	beta2
%define		rel		1
Summary:	Snort Log Backend
Name:		barnyard2
Version:	1.10
Release:	0.%{subver}.%{rel}
License:	GPL
Group:		Networking
Source0:	https://github.com/firnsy/barnyard2/tarball/v2-%{version}-%{subver}/%{name}-%{version}.tar.gz
# Source0-md5:	af417a3491c5a4e5605c8fbd529f2255
Source2:	%{name}.config
Source3:	%{name}
URL:		https://github.com/firnsy/barnyard2
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%{?with_mysql:BuildRequires:		mysql-devel}
%{?with_postgresql:BuildRequires:	postgresql-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Barnyard has 3 modes of operation: One-shot, continual, continual w/
checkpoint. In one-shot mode, barnyard will process the specified file
and exit. In continual mode, barnyard will start with the specified
file and continue to process new data (and new spool files) as it
appears. Continual mode w/ checkpointing will also use a checkpoint
file (or waldo file in the snort world) to track where it is. In the
event the barnyard process ends while a waldo file is in use, barnyard
will resume processing at the last entry as listed in the waldo file.

%{?with_mysql:barnyard2 binary compiled with mysql support.}
%{?with_postgresql:barnyard2 binary compiled with postgresql support.}

%prep
%setup -qc
mv firnsy-%{name}-*/* .

%build
%{__aclocal} -I m4
%{__libtoolize}
%{__autoconf}
%{__autoheader}
%{__automake} --force-missing
%configure \
	--sysconfdir=%{_sysconfdir}/snort \
	%{?with_postgresql:--with-postgresql} \
	%{?with_mysql:--with-mysql-libraries=%{_libdir}} \

%{__make}


%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_sysconfdir}/snort}
cp -p etc/barnyard2.conf $RPM_BUILD_ROOT%{_sysconfdir}/snort
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/barnyard2
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/barnyard2

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE doc
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/snort/barnyard2.conf
%attr(754,root,root) /etc/rc.d/init.d/barnyard2
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/barnyard2
%attr(755,root,root) %{_bindir}/barnyard2
