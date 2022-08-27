%define withgimp2 1

Summary:	Reads the raw image formats of 279 digital cameras
Name:		dcraw
Version:	9.28.0
Release:	4
Group:		Graphics
License:	Freely redistributable without restriction
Url:		http://www.cybercom.net/~dcoffin/dcraw/
# do not use source code, but the archive tarball
# it contains all additional localizations
Source0:	http://www.cybercom.net/~dcoffin/dcraw/archive/%{name}-%{version}.tar.gz
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

%if %{withgimp2}
BuildRequires:	pkgconfig(gimp-2.0)
%endif
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(lcms2)

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

%files -f %{name}.lang
%doc dcraw.html secrets.html badpixels README.crwinfo spec.crwinfo
%{_bindir}/*
%{_mandir}/man1/dcraw.1*

#----------------------------------------------------------------------------

%if %{withgimp2}
%package gimp2.0
Summary:	A GIMP plug-in to load raw files of digicams (GIMP 2.x)
Group:		Graphics
Requires:	gimp
Requires:	%{name}

%description gimp2.0
GIMP 2.x plug-in to load all raw image files of digital cameras
supported by the dcraw package. This allows direct editing of the
original images of the camera, without any conversion or compression
loss.

%files gimp2.0
%{_libdir}/gimp/2.0/plug-ins/*
%endif

#----------------------------------------------------------------------------

%prep
%setup -qc -a10
%if %{withgimp2}
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
cc ${CFLAGS:-%{optflags}} %{ldflags} -DLOCALEDIR='"%{_datadir}/locale/"' \
   dcraw.c -o dcraw -lm -ljpeg -llcms2 -ljasper
cd ..

# Build simple C programs
# fixed overlinking issues by appending -Wl,--as-needed -lm
for file in *.c; do
  if [ "$file" != "dcraw.c" ]; then
	cc ${CFLAGS:-%{optflags}} -o ${file%.c} $file %{ldflags} -lm
  fi
done

# Build GIMP plug-in
%if %{withgimp2}
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
%if %{withgimp2}
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
%if %{withgimp2}
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

