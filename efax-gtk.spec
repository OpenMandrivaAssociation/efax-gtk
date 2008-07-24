%define name	efax-gtk
%define version 3.0.16
%define release %mkrel 3

Name: 	 	%{name}
Summary: 	GTK2 frontend for efax
Version: 	%{version}
Release: 	%{release}

Source:		http://prdownloads.sourceforge.net/efax-gtk/%{name}-%{version}.src.tar.bz2
URL:		http://efax-gtk.sourceforge.net
License:	GPL
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	pkgconfig
BuildRequires:  gtk2-devel
BuildRequires:  sigc++2.0-devel
BuildRequires:  desktop-file-utils

Requires:	ghostscript
Requires:       cups
Requires:       gv

%description
Efax-gtk provides a GUI frontend for the efax fax program. It interfaces with
efax directly, replacing the scripts supplied with efax, and can be used for
receiving and sending faxes, and for viewing, printing, and managing faxes
which have been received and sent.

%prep
%setup -q
# since users can't write to /var/lock
perl -p -i -e 's|/var/lock|/tmp||g' efax-gtkrc
# /dev/modem is quite common
perl -p -i -e 's|ttyS1|modem||g' efax-gtkrc

%build
%configure2_5x
perl -p -i -e 's/install-data-hook//g' Makefile efax-gtk-faxfilter/Makefile
perl -p -i -e 's/usr\/local/usr/g' Makefile
perl -p -i -e 's/stock_send-fax.png/stock_send-fax/g' efax-gtk.desktop
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

#menu

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Office-Communications-Fax" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*



%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %mdkversion < 200900
%update_menus
%endif
touch /tmp/faxfile.ps
chmod a+rw /tmp/faxfile.ps

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS README BUGS COPYING
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}rc
%{_datadir}/applications/*
%{_mandir}/man1/*
/var/spool/fax/*


