%define Werror_cflags %nil

%define name	efax-gtk
%define version 3.2.4
%define release %mkrel 1

Name: 	 	%{name}
Summary: 	GTK2 frontend for efax
Version: 	%{version}
Release: 	%{release}

Source:		http:/prdownloads.sourceforge.net/efax-gtk/%{name}-%{version}.src.tgz
URL:		http://efax-gtk.sourceforge.net
License:	GPLv2
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	pkgconfig
BuildRequires:  gtk2-devel
BuildRequires:  sigc++2.0-devel
BuildRequires:  desktop-file-utils
BuildRequires:	libtiff-devel

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
perl -p -i -e 's/efax-gtk.png/efax-gtk/g' efax-gtk.desktop
%make

%install
rm -rf %{buildroot}
%makeinstall_std

#menu
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Office-Communications-Fax" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%find_lang %name

%clean
rm -rf %{buildroot}

%post
touch /tmp/faxfile.ps
chmod a+rw /tmp/faxfile.ps

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS README BUGS COPYING
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}rc
%{_datadir}/applications/*
%{_mandir}/man1/*
%{_datadir}/pixmaps/%{name}.png
%{_localstatedir}/spool/fax/*
