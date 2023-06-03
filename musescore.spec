#

%define min_qt_version 5.15.8

Summary:	MuseScore - music notation software
Summary(pl.UTF-8):	MuseScore - oprogramowanie do notacji muzycznej
Name:		musescore
Version:	4.0.2
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	https://github.com/musescore/MuseScore/archive/v%{version}.tar.gz
# Source0-md5:	e1a5b52bd2cede8f6f332f0f6e315b73
Patch0:		no-crashpad.patch
Patch1:		desktop.patch
Patch2:		use-qtmake-qt5.patch
Patch3:		set_as_stable.patch
Patch4:		%{name}-4.0.2-return.patch
URL:		https://musescore.org/
BuildRequires:	Qt5Concurrent-devel >= %{min_qt_version}
BuildRequires:	Qt5Core-devel >= %{min_qt_version}
BuildRequires:	Qt5Designer-devel >= %{min_qt_version}
BuildRequires:	Qt5Gui-devel >= %{min_qt_version}
BuildRequires:	Qt5Help-devel >= %{min_qt_version}
BuildRequires:	Qt5Network-devel >= %{min_qt_version}
BuildRequires:	Qt5NetworkAuth-devel >= %{min_qt_version}
BuildRequires:	Qt5OpenGL-devel >= %{min_qt_version}
BuildRequires:	Qt5PrintSupport-devel >= %{min_qt_version}
BuildRequires:	Qt5Qml-devel >= %{min_qt_version}
BuildRequires:	Qt5Quick-devel >= %{min_qt_version}
BuildRequires:	Qt5Sql-devel >= %{min_qt_version}
BuildRequires:	Qt5Svg-devel >= %{min_qt_version}
BuildRequires:	Qt5Test-devel >= %{min_qt_version}
BuildRequires:	Qt5UiTools-devel >= %{min_qt_version}
#%ifnarch x32
#BuildRequires:	Qt5WebEngine-devel >= %{min_qt_version}
#%endif
BuildRequires:	Qt5Quick-controls2-devel
BuildRequires:	Qt5Widgets-devel >= %{min_qt_version}
BuildRequires:	Qt5Xml-devel >= %{min_qt_version}
BuildRequires:	Qt5XmlPatterns-devel >= %{min_qt_version}
BuildRequires:	alsa-lib-devel
BuildRequires:	cmake >= 3.3.0
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
BuildRequires:	qt5-qmake
BuildRequires:	texlive-latex
Requires:	Qt5Quick-graphicaleffects
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# broken:
#  extracting debug info from /home/users/jajcus/tmp/musescore-3.0.4-root-jajcus/usr/bin/mscore
#  /usr/lib/rpm/bin/debugedit: canonicalization unexpectedly shrank by one character
#%define	_enable_debug_packages	0

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

%package fonts
Summary:	MuseScore fonts
Summary(pl.UTF-8):	Czcionki MuseScore
License:	GPL-3.0-or-later WITH Font-exception-2.0 AND OFL-1.1
Group:		Fonts
BuildArch:	noarch

%description fonts
Additional fonts for use by the MuseScore music notation program.

%prep
%setup -q -n MuseScore-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build

# note: 'build' directory is already there, for something else
install -d build.release
cd build.release

# cmake flags taken from the main Makefile
#CFLAGS="%{rpmcflags} -DNDEBUG -DQT_NO_DEBUG -fPIC" \
#CXXFLAGS="%{rpmcxxflags} -DNDEBUG -DQT_NO_DEBUG -fPIC" \
%cmake  \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DMUSESCORE_BUILD_CONFIG=release \
	-DMSCORE_INSTALL_SUFFIX="" \
	-DMUSESCORE_LABEL="" \
	-DBUILD_UNIT_TESTS=OFF \
	-DCMAKE_SKIP_RPATH="FALSE" \
	-DDOWNLOAD_SOUNDFONT="OFF" \
	-DUSE_SYSTEM_FREETYPE="ON" \
	-DBUILD_CRASHPAD_CLIENT=OFF \
%ifarch x32
	-DBUILD_WEBENGINE="OFF" \
%endif
	..

%{__make} lrelease
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd build.release
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# don't package kddockwidgets. It should not be installed
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm -r $RPM_BUILD_ROOT%{_includedir}/kddockwidgets
rm -r $RPM_BUILD_ROOT%{_libdir}/cmake/KDDockWidgets

# Remove opus devel files, they are provided by system
rm -r $RPM_BUILD_ROOT%{_includedir}/opus

rm $RPM_BUILD_ROOT%{_mandir}/man1/musescore.1.gz
echo ".so mscore.1" > $RPM_BUILD_ROOT%{_mandir}/man1/musescore.1

# install fonts
install -d $RPM_BUILD_ROOT%{fontdir}
install -p fonts/*.ttf $RPM_BUILD_ROOT%{fontdir}
install -p fonts/*/*.ttf $RPM_BUILD_ROOT%{fontdir}
install -p fonts/bravura/BravuraText.otf $RPM_BUILD_ROOT%{fontdir}
install -p fonts/campania/Campania.otf $RPM_BUILD_ROOT%{fontdir}
install -p fonts/edwin/*.otf $RPM_BUILD_ROOT%{fontdir}
install -p fonts/gootville/GootvilleText.otf $RPM_BUILD_ROOT%{fontdir}
install -p fonts/leland/LelandText.otf $RPM_BUILD_ROOT%{fontdir}
install -p fonts/musejazz/MuseJazzText.otf $RPM_BUILD_ROOT%{fontdir}
install -p fonts/petaluma/PetalumaText.otf $RPM_BUILD_ROOT%{fontdir}

# unique names for font docs
mv fonts/edwin/README.md         fonts/edwin/README.md.edwin
mv fonts/edwin/LICENSE.txt       fonts/edwin/LICENSE.txt.edwin
mv fonts/leland/README.md        fonts/leland/README.md.leland
mv fonts/leland/LICENSE.txt      fonts/leland/LICENSE.txt.leland

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
%{_datadir}/mscore-4.0
%{_desktopdir}/org.musescore.MuseScore.desktop
%{_iconsdir}/*/*/apps/*
%{_iconsdir}/*/*/mimetypes/*
%{_mandir}/man1/mscore.1*
%{_mandir}/man1/musescore.1*
%{_datadir}/mime/packages/musescore.xml
%{_datadir}/metainfo/org.musescore.MuseScore.appdata.xml
