#
Summary:	MuseScore - music notation software
Summary(pl.UTF-8):	MuseScore - oprogramowanie do notacji muzycznej
Name:		musescore
Version:	2.0.3
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	https://github.com/musescore/MuseScore/archive/v%{version}/%{name}-%{version}.tar.gz
URL:		https://musescore.org/
BuildRequires:	Qt5Concurrent-devel
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Designer-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Help-devel
BuildRequires:	Qt5Network-devel
BuildRequires:	Qt5OpenGL-devel
BuildRequires:	Qt5PrintSupport-devel
BuildRequires:	Qt5Qml-devel
BuildRequires:	Qt5Quick-devel
BuildRequires:	Qt5Sql-devel
BuildRequires:	Qt5Svg-devel
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5UiTools-devel
BuildRequires:	Qt5WebKit-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	Qt5Xml-devel
BuildRequires:	Qt5XmlPatterns-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	jack-audio-connection-kit-devel >= 0.98
BuildRequires:	lame-libs-devel
BuildRequires:	pkgconfig
BuildRequires:	portaudio-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	qt5-assistant
BuildRequires:	qt5-build
BuildRequires:	qt5-linguist
BuildRequires:	texlive-latex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MuseScore is an open source and free music notation software.

Features:
- WYSIWYG design, notes are entered on a "virtual notepaper"
- TrueType font(s) for printing & display allows for high quality
  scaling to all sizes
- easy & fast note entry
- many editing functions
- MusicXML import/export
- Midi (SMF) import/export
- MuseData import
- Midi input for note entry
- integrated sequencer and software synthesizer to play the score
- print or create pdf files

%prep
%setup -q -n MuseScore-%{version}

%build

# note: 'build' directory is already there, for something else
install -d build.release
cd build.release

# cmake flags taken from the main Makefile
%cmake  \
	-DMSCORE_INSTALL_SUFFIX="" \
	-DMUSESCORE_LABEL="" \
	-DBUILD_LAME="TRUE" \
	-DCMAKE_SKIP_RPATH="FALSE" \
	..

%{__make} lrelease
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd build.release
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT/%{_mandir}/man1/musescore.1.gz
echo ".so mscore.1" > $RPM_BUILD_ROOT/%{_mandir}/man1/musescore.1

%post
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%postun
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md Compatibility
%attr(755,root,root) %{_bindir}/mscore
%attr(755,root,root) %{_bindir}/musescore
%{_datadir}/mscore-2.0
%{_desktopdir}/mscore.desktop
%{_iconsdir}/*/*/apps/*
%{_iconsdir}/*/*/mimetypes/*
%{_mandir}/man1/mscore.1*
%{_mandir}/man1/musescore.1*
%{_datadir}/mime/packages/musescore.xml
