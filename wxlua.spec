%define oname wxLua

Summary:	wxWidgets bindings for Lua
Name:		wxlua
Version:	2.8.12.3
Release:	2
License:	wxWidgets License
Group:		Development/Other
Url:		http://wxlua.sourceforge.net/
Source0:	http://downloads.sourceforge.net/wxlua/%{oname}-%{version}-src.tar.gz
BuildRequires:	librsvg
BuildRequires:	pkgconfig(lua)
BuildRequires:	wxgtku2.8-devel

%description
wxLua is a set of bindings to the C++ wxWidgets cross-platform GUI library for
the Lua programming language. Nearly all of the functionality of wxWidgets is
exposed to Lua, meaning that your programs can have windows, dialogs, menus,
toolbars, controls, image loading and saving, drawing, sockets, streams,
printing, clipboard access... and much more.

Additionally, wxLua can be used in your C++ programs to embed a Lua interpreter
with the wxWidgets API.

%files
%{_libdir}/lua/5.1/wx.so

#----------------------------------------------------------------------------

%package ide
Summary:	Lua IDE with a GUI debugger
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Requires:	lua

%description ide
This package contains Integrated Development Environments (IDE, written in
wxLua) with a GUI debugger, a binding generator and wxWidgets bindings usable
as a module.

%files ide
%{_bindir}/%{oname}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}.*
%{_datadir}/wxlua

#----------------------------------------------------------------------------

%prep
%setup -q -n %{oname}-%{version}-src

%build
%cmake \
	-DwxWidgets_CONFIG_EXECUTABLE=/usr/bin/wx-config-unicode \
	-DwxLua_LUA_LIBRARY_BUILD_SHARED=FALSE \
	-DwxLua_LUA_LIBRARY_USE_BUILTIN=FALSE \
	-DwxLua_LUA_LIBRARY_VERSION=5.1 \
	-DBUILD_SHARED_LIBS=FALSE
%make

%install
%makeinstall_std -C build

rm -rf %{buildroot}%{_prefix}/doc
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_datadir}/wxstedit
rm -rf %{buildroot}%{_datadir}/wxlua/*.cmake
rm -rf %{buildroot}%{_libdir}/*.a

mkdir -p %{buildroot}%{_libdir}/lua/5.1/
mv %{buildroot}%{_libdir}/libwx.so %{buildroot}%{_libdir}/lua/5.1/wx.so

# Install icons of various sizes
for s in 256 128 96 48 32 22 16 ; do
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps
rsvg-convert -w ${s} -h ${s} \
    art/wxlualogo.svg -o \
    %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/%{name}.png
done

# menu-entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=wxLua
Comment=Lua IDE with a GUI debugger
Exec=%{oname}
Icon=%{name}
Terminal=false
Type=Application
Categories=Development;IDE;
EOF
