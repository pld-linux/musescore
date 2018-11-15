#

# http://ftp.osuosl.org/pub/musescore/soundfont/MuseScore_General/VERSION
%define soundfont_version 0.1.3

%define min_qt_version 5.4.0

Summary:	MuseScore - music notation software
Summary(pl.UTF-8):	MuseScore - oprogramowanie do notacji muzycznej
Name:		musescore
Version:	2.3.2
Release:	1
License:	GPL v2
Group:		Applications
Source0:	https://github.com/musescore/MuseScore/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	db0370d384858653b3ea0670efb8b069
Source1:	http://ftp.osuosl.org/pub/musescore/soundfont/MuseScore_General/MuseScore_General.sf3
# Source1-md5:	3e02cc70ae6df3077d0003bbcb95456c
Source2:	http://ftp.osuosl.org/pub/musescore/soundfont/MuseScore_General/MuseScore_General-License.md
# Source2-md5:	6ab9352030223f909bb36b8f067c7d26
Source3:	http://ftp.osuosl.org/pub/musescore/soundfont/MuseScore_General/MuseScore_General-changelog.txt
# Source3-md5:	765c42a6d1186ae2a68873ade1ff829c
URL:		https://musescore.org/
BuildRequires:	Qt5Concurrent-devel >= %{min_qt_version}
BuildRequires:	Qt5Core-devel >= %{min_qt_version}
BuildRequires:	Qt5Designer-devel >= %{min_qt_version}
BuildRequires:	Qt5Gui-devel >= %{min_qt_version}
BuildRequires:	Qt5Help-devel >= %{min_qt_version}
BuildRequires:	Qt5Network-devel >= %{min_qt_version}
BuildRequires:	Qt5OpenGL-devel >= %{min_qt_version}
BuildRequires:	Qt5PrintSupport-devel >= %{min_qt_version}
BuildRequires:	Qt5Qml-devel >= %{min_qt_version}
BuildRequires:	Qt5Quick-devel >= %{min_qt_version}
BuildRequires:	Qt5Sql-devel >= %{min_qt_version}
BuildRequires:	Qt5Svg-devel >= %{min_qt_version}
BuildRequires:	Qt5Test-devel >= %{min_qt_version}
BuildRequires:	Qt5UiTools-devel >= %{min_qt_version}
BuildRequires:	Qt5WebKit-devel >= %{min_qt_version}
BuildRequires:	Qt5Widgets-devel >= %{min_qt_version}
BuildRequires:	Qt5Xml-devel >= %{min_qt_version}
BuildRequires:	Qt5XmlPatterns-devel >= %{min_qt_version}
BuildRequires:	alsa-lib-devel
BuildRequires:	cmake >= 2.8.7
BuildRequires:	doxygen
BuildRequires:	freetype-devel >= 2.5.2
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

cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} share/sound
echo "%{soundfont_version}" > share/sound/VERSION

%build

# note: 'build' directory is already there, for something else
install -d build.release
cd build.release

# cmake flags taken from the main Makefile
CFLAGS="%{rpmcflags} -DNDEBUG -DQT_NO_DEBUG -fPIC" \
CXXFLAGS="%{rpmcxxflags} -DNDEBUG -DQT_NO_DEBUG -fPIC" \
%cmake  \
	-DMSCORE_INSTALL_SUFFIX="" \
	-DMUSESCORE_LABEL="" \
	-DBUILD_LAME="TRUE" \
	-DCMAKE_SKIP_RPATH="FALSE" \
	-DDOWNLOAD_SOUNDFONT="OFF" \
	-DUSE_SYSTEM_FREETYPE="ON" \
	-DBUILD_PORTMIDI="OFF" \
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
%{_datadir}/mscore-2.3
%{_desktopdir}/mscore.desktop
%{_iconsdir}/*/*/apps/*
%{_iconsdir}/*/*/mimetypes/*
%{_mandir}/man1/mscore.1*
%{_mandir}/man1/musescore.1*
%{_datadir}/mime/packages/musescore.xml
