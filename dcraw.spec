%define withgimp2 1

Name:		dcraw
Version:	9.16
Release:	2
Summary:	Reads the raw image formats of 279 digital cameras
Group:		Graphics
URL:		http://www.cybercom.net/~dcoffin/dcraw/
# do not use source code, but the archive tarball
# it contains all additional localizations
Source0:	http://www.cybercom.net/~dcoffin/dcraw/archive/%name-%version.tar.gz
Source2:	http://www.cybercom.net/~dcoffin/dcraw/rawphoto.c
Source3:	http://www.cybercom.net/~dcoffin/dcraw/.badpixels
Source4:	http://www.cybercom.net/~dcoffin/dcraw/dcraw.1.html
Source5:	dcwrap
Source6:	http://www.cybercom.net/~dcoffin/dcraw/parse.c
Source240:	http://www.cybercom.net/~dcoffin/dcraw/clean_crw.c
Source7:	fixdates.c
Source8:	http://www.cybercom.net/~dcoffin/dcraw/decompress.c
Source9:	pgm.c
Source210:	http://www.cybercom.net/~dcoffin/dcraw/sony_clear.c
Source10:	http://neuemuenze.heim1.tu-clausthal.de/~sven/crwinfo/CRWInfo-0.2.tar.bz2
Source11:	http://www.cybercom.net/~dcoffin/dcraw/fujiturn.c
Source250:	http://www.cybercom.net/~dcoffin/dcraw/fuji_green.c
Source220:	renum
Source230:	lcfile
# This is a copy of the dcraw home page with camera list, usage info, FAQ,
# ...
Source100:	http://www.cybercom.net/~dcoffin/dcraw/dcraw.html.bz2
Source110:	secrets.html
# program to read Nikon Dust Off images (NDF files)
Source260:	read_ndf.c
# Remove multiple-line string constant from crwinfo.c, gcc cannot handle it
Patch0:		crwinfo-help.patch
# gcc 4.x does not allow cast on left hand side of assignment
Patch1:		dcraw-7.42-sony-clear-gcc-4.patch
License:	Freely redistributable without restriction
%if %withgimp2
BuildRequires:	gimp-devel >= 2.0
%endif
BuildRequires:	jpeg-devel
BuildRequires:	lcms-devel
BuildRequires:	jasper-devel

%description
Reads and processes raw images from more than 279 digital cameras.

Raw images are the data directly read from the CCD of the camera,
without in-camera processing, without lossy JPEG compression, and in
36 or 48 bits color depth (TIFF has 24 bits). Problem of the raw
images is that they are in proprietary, camera-specific formats as
once, there seems not to be a standard format for high-color-depth
images, and second, the raw images contain headers with information
about camera settings.

This is a collection of command line tools to read and convert the raw
image files and also to get camera setting information out of them.

This program does not download the files from the camera, it only
processes the already downloaded files. Depending on your camera
model, mount your camera as a USB mass-storage device, use GPhoto2
("gtkam", "digikam", "flphoto", "gphoto2"), or a flash card reader for
downloading the files.


%if %withgimp2
%package gimp2.0
Summary:	A GIMP plug-in to load raw files of digicams (GIMP 2.x)
Group:		Graphics
Requires:	gimp dcraw
Conflicts:	rawphoto ufraw
 
%description gimp2.0
GIMP 2.x plug-in to load all raw image files of digital cameras
supported by the dcraw package. This allows direct editing of the
original images of the camera, without any conversion or compression
loss.
%endif

%prep
%setup -qc -a10
%if %withgimp2
mkdir gimp2.0
install -m644 %{SOURCE2} gimp2.0/rawphoto.c
%endif
install -m644 %{SOURCE3} .badpixels
install -m644 %{SOURCE4} dcraw.1
install -m644 %{SOURCE5} dcwrap
install -m644 %{SOURCE6} parse.c
install -m644 %{SOURCE240} clean_crw.c
install -m644 %{SOURCE7} fixdates.c
install -m644 %{SOURCE8} decompress.c
install -m644 %{SOURCE9} pgm.c
install -m644 %{SOURCE210} sony_clear.c
install -m644 %{SOURCE11} fujiturn.c
install -m644 %{SOURCE250} fuji_green.c
install -m644 %{SOURCE220} renum
install -m644 %{SOURCE230} lcfile
bzcat %{SOURCE100} > dcraw.html
install -m644 %{SOURCE110} secrets.html
install -m644 %{SOURCE260} read_ndf.c
#cd ljpeg_decode
#ln -s ../dcraw.c .
#cd ..
cd CRWInfo*
%patch0 -p0 -b .help
cd ..
%patch1 -p0 -b .gcc4

%build
%setup_compile_flags

cd dcraw
cc ${CFLAGS:-%optflags} %{ldflags} -DLOCALEDIR='"%{_datadir}/locale/"' \
   dcraw.c -o dcraw -lm -ljpeg -llcms -ljasper
cd ..

# Build simple C programs
# fixed overlinking issues by appending -Wl,--as-needed -lm
for file in *.c; do
  if [ "$file" != "dcraw.c" ]; then
	cc ${CFLAGS:-%optflags} -o ${file%.c} $file %{ldflags} -lm
  fi
done

# Build GIMP plug-in
%if %withgimp2
gimptool-2.0 --build gimp2.0/rawphoto.c
mv rawphoto gimp2.0
%endif

# Build programs provided in tarballs
cd CRWInfo*
%make
cd ..

#cd ljpeg_decode
#make
#cd ..

%install
# Directories
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1
%if %withgimp2
install -d %{buildroot}%{_libdir}/gimp/2.0/plug-ins
%endif

# Program files
#install -m 755 ljpeg_decode/dcraw %{buildroot}%{_bindir}
install -m 755 dcraw/dcraw %{buildroot}%{_bindir}
install -m 755 decompress %{buildroot}%{_bindir}
install -m 755 fixdates %{buildroot}%{_bindir}
install -m 755 fujiturn %{buildroot}%{_bindir}
install -m 755 fuji_green %{buildroot}%{_bindir}
install -m 755 parse %{buildroot}%{_bindir}
install -m 755 clean_crw %{buildroot}%{_bindir}
install -m 755 pgm %{buildroot}%{_bindir}
%if %withgimp2
install -m 755 gimp2.0/rawphoto %{buildroot}%{_libdir}/gimp/2.0/plug-ins
%endif
install -m 755 CRWInfo*/crwinfo %{buildroot}%{_bindir}
install -m 755 sony_clear %{buildroot}%{_bindir}
install -m 755 renum %{buildroot}%{_bindir}
install -m 755 lcfile %{buildroot}%{_bindir}

# Documentation
install -m 644 .badpixels badpixels
install -m 644 CRWInfo*/README README.crwinfo
install -m 644 CRWInfo*/spec spec.crwinfo

install -D -m 644 dcraw/dcraw.1 %{buildroot}%{_datadir}/man/man1

pushd dcraw
for lang in fr it de pt es nl sv ca cs hu pl eo ru zh_TW zh_CN da
do
  if [ -f dcraw_$lang.po ]; then
    mkdir -p -m 755 %{buildroot}/%{_datadir}/locale/$lang/LC_MESSAGES
    msgfmt -o %{buildroot}/%{_datadir}/locale/$lang/LC_MESSAGES/dcraw.mo \
      dcraw_$lang.po
    echo "%lang($lang) %{_datadir}/locale/$lang/LC_MESSAGES/dcraw.mo" >> ../%{name}.lang
  fi
  if [ -f dcraw_$lang.1 ]; then
    install -m 644 -D dcraw_$lang.1 %{buildroot}/%{_datadir}/man/$lang/man1/dcraw_$lang.1
    echo "%lang($lang) %{_datadir}/man/$lang/man1/dcraw_$lang.1*" >> ../%{name}.lang
  fi
done
popd

#find_lang %{name} --with-man

%files -f %{name}.lang
%doc dcraw.html secrets.html badpixels README.crwinfo spec.crwinfo
%{_bindir}/*
%{_mandir}/man1/dcraw.1*

%if %withgimp2
%files gimp2.0
%{_libdir}/gimp/2.0/plug-ins/*
%endif



%changelog
* Tue Jul 31 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 9.16-1
+ Revision: 811503
- update to 9.16
- dont package non-utf8 man pages

* Thu Dec 29 2011 Götz Waschk <waschk@mandriva.org> 9.12-1
+ Revision: 748188
- new version
- update build deps

* Fri Nov 25 2011 Götz Waschk <waschk@mandriva.org> 9.11-1
+ Revision: 733345
- new version
- build fix

* Wed Aug 03 2011 Götz Waschk <waschk@mandriva.org> 9.10-1
+ Revision: 692969
- new version
- build with jasper support
- uncompress html doc

* Thu Jun 16 2011 Götz Waschk <waschk@mandriva.org> 9.08-1
+ Revision: 685484
- new version

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 9.06-2
+ Revision: 663760
- mass rebuild

* Mon Mar 07 2011 Götz Waschk <waschk@mandriva.org> 9.06-1
+ Revision: 642409
- update to new version 9.06

* Tue Dec 21 2010 Götz Waschk <waschk@mandriva.org> 9.05-1mdv2011.0
+ Revision: 623628
- update to new version 9.05

* Mon Aug 09 2010 Funda Wang <fwang@mandriva.org> 9.04-1mdv2011.0
+ Revision: 568053
- new version 9.04

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 8.96-2mdv2010.1
+ Revision: 488744
- rebuilt against libjpeg v8

* Sun Aug 23 2009 Frederik Himpe <fhimpe@mandriva.org> 8.96-1mdv2010.0
+ Revision: 419909
- update to new version 8.96
- update to new version 8.95

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 8.93-3mdv2010.0
+ Revision: 416649
- rebuilt against libjpeg v7

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 8.93-2mdv2010.0
+ Revision: 413343
- rebuild

* Sun Mar 22 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 8.93-1mdv2009.1
+ Revision: 360202
- Updated to version 8.93
- Make sure we enable internationalization defining LOCALEDIR in dcraw
  build.
- Provide main dcraw man page.

* Thu Nov 13 2008 Frederic Crozat <fcrozat@mandriva.com> 8.88-1mdv2009.1
+ Revision: 302685
- Release 8.88
- a lot of specfile cleanup and improvement from Florian Hubold

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 8.80-2mdv2009.0
+ Revision: 220577
- rebuild
- fix spacing at top of description
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sun Nov 18 2007 Giuseppe Ghibò <ghibo@mandriva.com> 8.80-1mdv2008.1
+ Revision: 109824
- Release 8.80.

* Sat Sep 15 2007 Adam Williamson <awilliamson@mandriva.org> 8.61-2mdv2008.0
+ Revision: 85822
- oops, correct fix for doc install failure
- fix installation of .badpixels
- correct buildrequires
- rebuild for 2008
- new doc policy (don't use a versioned directory)
- Fedora license policy


* Sun Feb 25 2007 Emmanuel Andry <eandry@mandriva.org> 8.61-1mdv2007.0
+ Revision: 125628
- New version 8.61
- uncompress patches
- change number of supported cameras to 254
- Import dcraw

* Fri Aug 25 2006 Till Kamppeter <till@mandriva.com> 8.31-2mdv2007.0
- Shortened the package description.

* Wed Aug 23 2006 Till Kamppeter <till@mandriva.com> 8.31-1mdv2007.0
- Updated to version 8.31 (Many new cameras supported).
- Also updated: rawphoto.c, dcraw.1, parse.c, dcraw.html

* Sat May 13 2006 Till Kamppeter <till@mandriva.com> 8.15-2mdk
- Rebuild.

* Sat May 13 2006 Till Kamppeter <till@mandriva.com> 8.15-1mdk
- Updated to version 8.15 (New cameras supported, including Canon EOS 30D).
- Also updated: parse.c dcraw.html, dcraw.1

* Sat May 13 2006 Till Kamppeter <till@mandriva.com> 8.03-3mdk
- Rebuild to make Cooker consistent again.

* Sat May 13 2006 Stefan van der Eijk <stefan@eijk.nu> 8.03-2mdk
- rebuild for sparc

* Fri Feb 03 2006 Till Kamppeter <till@mandriva.com> 8.03-1mdk
- Updated to version 7.49 (New cameras supported, including Sony DSC R1,
  Pentax *istDL, Olympus E-500, Canon EOS 5D; Color management based on
  LittleCMS).
- Also updated: rawphoto.c, parse.c dcraw.html, dcraw.1
- Re-introduced GIMP plug-in, it builds again.
- Introduced %%mkrel.

* Sat Sep 03 2005 Till Kamppeter <till@mandriva.com> 7.49-2mdk
- Removed unneeded "Requires: ".
- Removed GIMP plug-in. Does not build any more and there are several
  better ones around (ex.: ufraw).

* Mon Aug 15 2005 Till Kamppeter <till@mandriva.com> 7.49-1mdk
- Updated to version 7.49 (New cameras supported, including Minolta
  Alpha/Dynax/Maxxum 5D and Olympus C770UZ).
- Updated also: rawphoto, parse.

* Mon Jul 18 2005 Till Kamppeter <till@mandriva.com> 7.42-1mdk
- Updated to version 7.42 (New cameras supported, including Nikon D50).
- Updated also: parse.
- Removed restriction on using gcc 3.x, it works with gcc 4.x now.
- Patch1 to make sony_clear working with gcc 4.x.

* Sun May 15 2005 Till Kamppeter <till@mandriva.com> 7.21-1mdk
- Updated to version 7.21 (New cameras supported, including Canon EOS 350D).
- Updated also: .badpixels, parse, fujiturn.
- Still some compatibility issues with GCC 4.x, using 3.x for now.

* Fri Apr 22 2005 Till Kamppeter <till@mandriva.com> 7.14-1mdk
- Updated to version 7.14 (Many new cameras, support for the Adobe
  Digital Negative format, DNG).
- Updated also: rawphoto, parse.

* Mon Mar 07 2005 Till Kamppeter <till@mandrakesoft.com> 6.35-2mdk
- Added "Conflicts: ufraw" to the GIMP 2 plugin package.

* Mon Mar 07 2005 Till Kamppeter <till@mandrakesoft.com> 6.35-1mdk
- Updated to version 6.35.
- Updated also: parse.
- Updated to "Requires: jpeg-progs".
- Updated to "Requires: gimp" (it is every day changing).

* Fri Feb 11 2005 Till Kamppeter <till@mandrakesoft.com> 6.34-1mdk
- Updated to version 6.34.
- Updated also: dcwrap, parse, rawphoto.

* Sat Jan 15 2005 Couriousous <couriousous@mandrake.org> 6.18-2mdk
- Fix gimp requires

* Fri Dec 17 2004 Till Kamppeter <till@mandrakesoft.com> 6.18-1mdk
- Updated to version 6.18 (New cameras supported, especially all recent
  DSLRs).

* Wed Sep 08 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.20040813-2mdk
- add BuildRequires: libjpeg-devel

* Sat Aug 14 2004 Till Kamppeter <till@mandrakesoft.com> 0.20040813-1mdk
- Updated to the state of 13/08/2004 (More camera models supported).
- Removed support for GIMP 1.x as dcraw is in main and GIMP 1.x in contrib.

* Wed May 12 2004 Till Kamppeter <till@mandrakesoft.com> 0.20040511-1mdk
- Updated to the state of 11/05/2004 (Many new camera models supported).

* Thu Mar 25 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.20040317-2mdk
- rebuild for gimp2

* Wed Mar 17 2004 Till Kamppeter <till@mandrakesoft.com> 0.20040317-1mdk
- Updated to the state of 15/12/2003 (Many new camera models supported,
  GIMP 2.0 support, some new tools added).

