Summary:	Image gallery system created in PHP
Summary(pl):	System galeriowy oparty na PHP
Name:		phpAutoGallery
Version:	0.9.6
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/phpautogallery/%{name}-%{version}.tar.gz
# Source0-md5:	8fc1407037f54b9d2b9d5f3d9f47939f
Source1:	%{name}.conf
URL:		http://phpautogallery.sourceforge.net/
Requires:	ImageMagick
Requires:	php
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gallerydir	%{_datadir}/%{name}
%define		_sysconfdir	/etc/%{name}

%description
phpAutoGallery is a auto indexing picture gallery written in php and
with the help of mod_rewrite.

Current Features:

- Application fully transparent to gallery-enduser
- On-the-fly creation and caching of thumbnails, resized fullsize
  images, directory listings
- Configurable view sizes for fullsize-image display
- Overlaying of Copyright/Logo images on-the-fly.
- Displays information about imagefiles and directories.
- Folder- and picture-descriptions
- Admin-interface
- Easy to setup.
- Fully customizable through the use of Smarty templates.
- Generates valid XHTML 1.0 Strict and CSS 2.0 code


%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_gallerydir} \
	$RPM_BUILD_ROOT{%{_sysconfdir},/etc/httpd,%{_gallerydir}/config}

cp -af css htaccess-dist img include loader javascript php *.php templates $RPM_BUILD_ROOT%{_gallerydir}

install config/config.inc.php $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf %{_sysconfdir}/config.inc.php $RPM_BUILD_ROOT%{_gallerydir}/config/config.inc.php

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/usr/sbin/apachectl restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc BUGS CHANGELOG README docs/*
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%config(noreplace) %verify(not md5 mtime size) /etc/httpd/%{name}.conf
%dir %{_gallerydir}
%{_gallerydir}/*
#%{_gallerydir}/*.php
#%{_gallerydir}/*.css
