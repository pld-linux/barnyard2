
# Conditional build:
%bcond_without  mysql		# don't build support for MySQL
%bcond_without	postgresql	# don't build support for PostgreSQL

Summary:	Snort Log Backend
Name:		barnyard2
Version:	1.10beta2
Release:	1
License:	GPL
Group:		Networking
Source0:	https://github.com/firnsy/barnyard2/tarball/v2-1.10-beta2
# Source0-md5:	af417a3491c5a4e5605c8fbd529f2255
Source2:	%{name}.config
Source3:	%{name}
URL:		https://github.com/firnsy/barnyard2
%{?with_mysql:BuildRequires:		mysql-devel}
%{?with_postgresql:BuildRequires:	postgresql-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Barnyard has 3 modes of operation:
One-shot, continual, continual w/ checkpoint.  In one-shot mode,
barnyard will process the specified file and exit.  In continual mode,
barnyard will start with the specified file and continue to process
new data (and new spool files) as it appears.  Continual mode w/
checkpointing will also use a checkpoint file (or waldo file in the
snort world) to track where it is.  In the event the barnyard process
ends while a waldo file is in use, barnyard will resume processing at
the last entry as listed in the waldo file.
%{?with_mysql:barnyard2 binary compiled with mysql support.}
%{?with_postgresql:barnyard2 binary compiled with postgresql support.}

%prep
%setup -q -n firnsy-barnyard2-5832a85


%build
./autogen.sh
%configure --sysconfdir=%{_sysconfdir}/snort  \
	%{?with_postgresql:--with-postgresql} \
	%{?with_mysql:--with-mysql-libraries=/usr/%{_lib}} \

%{__make}


%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__install} -d -p $RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,rc.d/init.d,snort} 
%{__install} -d -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/contrib
%{__install} -d -p $RPM_BUILD_ROOT%{_mandir}/man8
%{__install} -d -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/doc
%{__install} -m 644 etc/barnyard2.conf $RPM_BUILD_ROOT%{_sysconfdir}/snort/
%{__install} -m 644 $RPM_SOURCE_DIR/barnyard2.config $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/barnyard2
%{__install} -m 755 $RPM_SOURCE_DIR/barnyard2 $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/barnyard2
%{__install} -m 644 doc/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/doc/

%clean
if [ -d $RPM_BUILD_ROOT ] && [ "$RPM_BUILD_ROOT" != "/"  ] ; then
	rm -rf $RPM_BUILD_ROOT
fi

%files
%defattr(644,root,root,755)
%doc LICENSE doc/
%attr(755,root,root) %{_bindir}/barnyard2
%attr(640,root,root) %config %{_sysconfdir}/snort/barnyard2.conf
%attr(755,root,root) %config %{_sysconfdir}/rc.d/init.d/barnyard2
%attr(644,root,root) %config %{_sysconfdir}/sysconfig/barnyard2
