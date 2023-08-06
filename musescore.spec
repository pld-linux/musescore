#

%define min_qt_version 5.15.8

Summary:	MuseScore - music notation software
Summary(pl.UTF-8):	MuseScore - oprogramowanie do notacji muzycznej
Name:		musescore
Version:	4.1.1
Release:	1
License:	GPL v2
Group:		Applications
Source0:	https://github.com/musescore/MuseScore/archive/v%{version}.tar.gz
# Source0-md5:	080fd5bf13ef2774af451ae47de09dee
Patch0:		no-crashpad.patch
Patch1:		desktop.patch
Patch2:		use-qtmake-qt5.patch
Patch3:		set_as_stable.patch
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
BuildRequires:	Qt5Quick-controls2-devel
BuildRequires:	Qt5Quick-devel >= %{min_qt_version}
BuildRequires:	Qt5Sql-devel >= %{min_qt_version}
BuildRequires:	Qt5Svg-devel >= %{min_qt_version}
BuildRequires:	Qt5Test-devel >= %{min_qt_version}
BuildRequires:	Qt5UiTools-devel >= %{min_qt_version}
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
Suggests:	%{name}-fonts
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

%description -l pl.UTF-8
MuseScore to otwarte i darmowe oprogramowanie do notacji muzycznej.

Cechy:
- edytor WYSIWYG, nuty są wprowadzane na "wirtualny papier nutowy"
- czcionki TrueType do drukowania i wyświetlania umożliwiają wysokiej
  jakości skalowanie do wszystkich rozmiarów
- łatwe i szybkie wprowadzanie nut
- wiele funkcji edycyjnych
- import/eksport MusicXML
- import/eksport Midi (SMF).
- import MuseData
- wejście Midi do wprowadzania nut
- zintegrowany sekwencer i syntezator programowy do odtwarzania
  partytury
- możliwość tworzenia i drukowania plików pdf

%package fonts
Summary:	MuseScore fonts
Summary(pl.UTF-8):	Czcionki MuseScore
License:	GPL-3.0-or-later WITH Font-exception-2.0 AND OFL-1.1
Group:		Fonts
BuildArch:	noarch

%description fonts
Additional fonts for use by the MuseScore music notation program.

%description fonts -l pl.UTF-8
Dodatkowe czcionki do użytku w oprogramowaniu do notacji muzycznej
MuseScore.

%prep
%setup -q -n MuseScore-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# fix EOL encoding
sed 's/\r$//' fonts/bravura/OFL-FAQ.txt > tmpfile
touch -r fonts/bravura/OFL-FAQ.txt tmpfile
mv -f tmpfile fonts/bravura/OFL-FAQ.txt

sed 's/\r$//' thirdparty/rtf2html/README > tmpfile
touch -r thirdparty/rtf2html/README tmpfile
mv -f tmpfile thirdparty/rtf2html/README

sed 's/\r$//' thirdparty/rtf2html/README.ru > tmpfile
touch -r thirdparty/rtf2html/README.ru tmpfile
mv -f tmpfile thirdparty/rtf2html/README.ru

%build

# note: 'build' directory is already there, for something else
install -d build.release
cd build.release

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

cd ..
# install fonts
install -d $RPM_BUILD_ROOT%{_datadir}/fonts/{OTF,TTF}
install -p fonts/*.ttf $RPM_BUILD_ROOT%{_datadir}/fonts/TTF
install -p fonts/*/*.ttf $RPM_BUILD_ROOT%{_datadir}/fonts/TTF
install -p fonts/bravura/BravuraText.otf $RPM_BUILD_ROOT%{_datadir}/fonts/OTF
install -p fonts/campania/Campania.otf $RPM_BUILD_ROOT%{_datadir}/fonts/OTF
install -p fonts/edwin/*.otf $RPM_BUILD_ROOT%{_datadir}/fonts/OTF
install -p fonts/gootville/GootvilleText.otf $RPM_BUILD_ROOT%{_datadir}/fonts/OTF
install -p fonts/leland/LelandText.otf $RPM_BUILD_ROOT%{_datadir}/fonts/OTF
install -p fonts/musejazz/MuseJazzText.otf $RPM_BUILD_ROOT%{_datadir}/fonts/OTF
install -p fonts/petaluma/PetalumaText.otf $RPM_BUILD_ROOT%{_datadir}/fonts/OTF

# unique names for font docs
mv fonts/edwin/README.md         fonts/edwin/README.md.edwin
mv fonts/edwin/LICENSE.txt       fonts/edwin/LICENSE.txt.edwin
mv fonts/leland/README.md        fonts/leland/README.md.leland
mv fonts/leland/LICENSE.txt      fonts/leland/LICENSE.txt.leland

# collect doc files
mkdir tmp_doc
install -p thirdparty/beatroot/COPYING         tmp_doc/COPYING.beatroot
install -p thirdparty/beatroot/README.txt      tmp_doc/README.txt.beatroot
install -p thirdparty/dtl/COPYING              tmp_doc/COPYING.BSD.dtl
install -p thirdparty/freetype/README          tmp_doc/README.freetype
install -p thirdparty/intervaltree/README      tmp_doc/README.intervaltree
install -p thirdparty/rtf2html/ChangeLog       tmp_doc/ChangeLog.rtf2html
install -p thirdparty/rtf2html/COPYING.LESSER  tmp_doc/COPYING.LESSER.rtf2html
install -p thirdparty/rtf2html/README          tmp_doc/README.rtf2html
install -p thirdparty/rtf2html/README.mscore   tmp_doc/README.mscore.rtf2html
install -p thirdparty/rtf2html/README.ru       tmp_doc/README.ru.rtf2html
install -p tools/bww2mxml/COPYING              tmp_doc/COPYING.bww2mxml
install -p tools/bww2mxml/README               tmp_doc/README.bww2mxml
install -p share/sound/README.md               tmp_doc/README.md.sound
install -p share/instruments/README.md         tmp_doc/README.md.instruments
install -p share/wallpapers/COPYRIGHT          tmp_doc/COPYING.wallpaper

%post
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%postun
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%post fonts
fontpostinst OTF
fontpostinst TTF

%postun fonts
fontpostinst OTF
fontpostinst TTF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md Compatibility LICENSE.GPL tmp_doc/*
%attr(755,root,root) %{_bindir}/mscore
%{_datadir}/mscore-4.1
%{_desktopdir}/org.musescore.MuseScore.desktop
%{_iconsdir}/*/*/apps/*
%{_iconsdir}/*/*/mimetypes/*
%{_mandir}/man1/mscore.1*
%{_mandir}/man1/musescore.1*
%{_datadir}/mime/packages/musescore.xml
%{_datadir}/metainfo/org.musescore.MuseScore.appdata.xml

%files fonts
%defattr(644,root,root,755)
%{_datadir}/fonts/TTF/*.ttf
%{_datadir}/fonts/OTF/*.otf
%doc fonts/README.md
%doc fonts/bravura/bravura-text.md
%doc fonts/bravura/OFL-FAQ.txt
%doc fonts/bravura/OFL.txt
%doc fonts/gootville/readme.txt fonts/campania/LICENSE
# see section 'unique names for font docs' above
%doc fonts/edwin/README.md.edwin fonts/edwin/LICENSE.txt.edwin
%doc fonts/leland/README.md.leland fonts/leland/LICENSE.txt.leland
