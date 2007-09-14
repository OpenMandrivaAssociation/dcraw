%define	name	dcraw
%define	version	8.61
%define	release	%mkrel 2

%define withgimp1 0
%define withgimp2 1
#define gcc	gcc-3.3.4
%define gcc	gcc

Name:		%name
Version:	%version
Release:	%release
Summary:	Reads the raw image formats of 226 digital cameras
Group:		Graphics
URL:		http://www.cybercom.net/~dcoffin/dcraw/
Source0:	http://www.cybercom.net/~dcoffin/dcraw/dcraw.c.bz2
Source2:	http://www.cybercom.net/~dcoffin/dcraw/rawphoto.c.bz2
Source3:	http://www.cybercom.net/~dcoffin/dcraw/.badpixels.bz2
Source4:	http://www.cybercom.net/~dcoffin/dcraw/dcraw.1.bz2
Source5:	dcwrap.bz2
Source6:	http://www.cybercom.net/~dcoffin/dcraw/parse.c.bz2
Source240:	http://www.cybercom.net/~dcoffin/dcraw/clean_crw.c.bz2
Source7:	fixdates.c.bz2
Source8:	http://www.cybercom.net/~dcoffin/dcraw/decompress.c.bz2
Source9:	pgm.c.bz2
Source210:	http://www.cybercom.net/~dcoffin/dcraw/sony_clear.c.bz2
Source10:	http://neuemuenze.heim1.tu-clausthal.de/~sven/crwinfo/CRWInfo-0.2.tar.bz2
Source11:	http://www.cybercom.net/~dcoffin/dcraw/fujiturn.c.bz2
Source250:	http://www.cybercom.net/~dcoffin/dcraw/fuji_green.c.bz2
Source220:	renum.bz2
Source230:	lcfile.bz2
# This is a copy of the dcraw home page with camera list, usage info, FAQ,
# ...
Source100:	http://www.cybercom.net/~dcoffin/dcraw/dcraw.html.bz2
Source110:	secrets.html.bz2
# Remove multiple-line string constant from crwinfo.c, gcc cannot handle it
Patch0:		crwinfo-help.patch
# gcc 4.x does not allow cast on left hand side of assignment
Patch1:		dcraw-7.42-sony-clear-gcc-4.patch
License:	Freely redistributable without restriction
%if %withgimp1
BuildRequires:	gimp-devel
%endif 
%if %withgimp2
BuildRequires:	libgimp-devel >= 2.0
%endif
BuildRequires:	libjpeg-devel, lcms-devel
Buildroot:	%_tmppath/%name-%version-%release-root

%description
Reads and processes raw images from more than 245 digital cameras.

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


%if %withgimp1
%package gimp
Summary: 	A GIMP plug-in to load raw image files of digital cameras
Group: 		Graphics
Requires: 	gimp dcraw
 
%description gimp

GIMP 1.2.x plug-in to load all raw image files of digital cameras
supported by the dcraw package. This allows direct editing of the
original images of the camera, without any conversion or compression
loss.

%endif
%if %withgimp2
%package gimp2.0
Summary: 	A GIMP plug-in to load raw files of digicams (GIMP 2.2.x)
Group: 		Graphics
Requires: 	gimp dcraw
Conflicts:	rawphoto ufraw
 
%description gimp2.0

GIMP 2.2.x plug-in to load all raw image files of digital cameras
supported by the dcraw package. This allows direct editing of the
original images of the camera, without any conversion or compression
loss.
%endif

%prep
rm -rf $RPM_BUILD_DIR/%{name}-%{version}
mkdir $RPM_BUILD_DIR/%{name}-%{version}
%if %withgimp1
mkdir $RPM_BUILD_DIR/%{name}-%{version}/gimp
%endif
%if %withgimp2
mkdir $RPM_BUILD_DIR/%{name}-%{version}/gimp2.0
%endif
cd $RPM_BUILD_DIR/%{name}-%{version}

bzcat %{SOURCE0} > dcraw.c
%if %withgimp1
bzcat %{SOURCE2} > gimp/rawphoto.c
%endif
%if %withgimp2
bzcat %{SOURCE2} > gimp2.0/rawphoto.c
%endif
bzcat %{SOURCE3} > .badpixels
bzcat %{SOURCE4} > dcraw.1
bzcat %{SOURCE5} > dcwrap
bzcat %{SOURCE6} > parse.c
bzcat %{SOURCE240} > clean_crw.c
bzcat %{SOURCE7} > fixdates.c
bzcat %{SOURCE8} > decompress.c
bzcat %{SOURCE9} > pgm.c
bzcat %{SOURCE210} > sony_clear.c
bzcat %{SOURCE11} > fujiturn.c
bzcat %{SOURCE250} > fuji_green.c
bzcat %{SOURCE220} > renum
bzcat %{SOURCE230} > lcfile
bzcat %{SOURCE100} > dcraw.html
bzcat %{SOURCE110} > secrets.html
#setup -q -T -D -a 1 -n %{name}-%{version}
#cd ljpeg_decode
#ln -s ../dcraw.c .
#cd ..
%setup -q -T -D -a 10 -n %{name}-%{version}
cd CRWInfo*
%patch0 -p0
cd ..
%patch1 -p0

%build
cd $RPM_BUILD_DIR/%{name}-%{version}

%{gcc} ${CFLAGS:-%optflags} -lm -ljpeg -llcms -o dcraw dcraw.c

# Build simple C programs
for file in *.c; do
   if [ "$file" != "dcraw.c" ]; then
      %{gcc} ${CFLAGS:-%optflags} -lm -o ${file%.c} $file
   fi
done

# Build GIMP plug-in
%if %withgimp1
gimptool-1.2 --build gimp/rawphoto.c
mv rawphoto gimp
%endif
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
cd $RPM_BUILD_DIR/%{name}-%{version}

rm -rf %buildroot

# Directories
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_docdir}/%{name}
%if %withgimp1
install -d %{buildroot}%{_libdir}/gimp/1.2/plug-ins
%endif
%if %withgimp2
install -d %{buildroot}%{_libdir}/gimp/2.0/plug-ins
%endif

# Program files
#install -m 755 ljpeg_decode/dcraw %{buildroot}%{_bindir}
install -m 755 dcraw %{buildroot}%{_bindir}
install -m 755 decompress %{buildroot}%{_bindir}
install -m 755 fixdates %{buildroot}%{_bindir}
install -m 755 fujiturn %{buildroot}%{_bindir}
install -m 755 fuji_green %{buildroot}%{_bindir}
install -m 755 parse %{buildroot}%{_bindir}
install -m 755 clean_crw %{buildroot}%{_bindir}
install -m 755 pgm %{buildroot}%{_bindir}
%if %withgimp1
install -m 755 gimp/rawphoto %{buildroot}%{_libdir}/gimp/1.2/plug-ins
%endif
%if %withgimp2
install -m 755 gimp2.0/rawphoto %{buildroot}%{_libdir}/gimp/2.0/plug-ins
%endif
install -m 755 CRWInfo*/crwinfo %{buildroot}%{_bindir}
install -m 755 sony_clear %{buildroot}%{_bindir}
install -m 755 renum %{buildroot}%{_bindir}
install -m 755 lcfile %{buildroot}%{_bindir}

# Documentation
install -m 644 dcraw.1 %{buildroot}%{_mandir}/man1
install -m 644 dcraw.html %{buildroot}%{_docdir}/%{name}
install -m 644 secrets.html %{buildroot}%{_docdir}/%{name}
install -m 644 .badpixels %{buildroot}%{_docdir}/%{name}/badpixels
install -m 644 CRWInfo*/README %{buildroot}%{_docdir}/%{name}/README.crwinfo
install -m 644 CRWInfo*/spec %{buildroot}%{_docdir}/%{name}/spec.crwinfo

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%docdir %{_docdir}/%{name}
%_bindir/*
%_mandir/man1/*
%_docdir/*

%if %withgimp1
%files gimp
%defattr(-,root,root)
%{_libdir}/gimp/1.2/plug-ins/*
%endif

%if %withgimp2
%files gimp2.0
%defattr(-,root,root)
%{_libdir}/gimp/2.0/plug-ins/*
%endif


