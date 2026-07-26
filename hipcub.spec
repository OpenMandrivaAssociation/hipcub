# CUB-like HIP wrappers on rocPRIM (header-only) (TheRock 7.14)
%global debug_package %{nil}

Name:		hipcub
Version:	7.14.0
Release:	1
Summary:	CUB-like HIP wrappers on rocPRIM (header-only)
License:	BSD-3-Clause
Group:		Development/C++
URL:		https://github.com/ROCm/rocm-libraries
Source0:	https://github.com/ROCm/rocm-libraries/releases/download/therock-7.14/hipcub.tar.gz#/hipcub-%{version}.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	rocm-cmake
BuildRequires:	hipcc
BuildRequires:	rocminfo
BuildRequires:	clang-tools
BuildRequires:	rocm-hip-devel
BuildRequires:	clang >= %{rocm_llvm_maj_ver}
BuildRequires:	rocprim-devel

ExclusiveArch:	%{x86_64} %{aarch64}

%description
hipCUB provides a CUB-like API on rocPRIM. Header-only. GPU targets include gfx803.

%package devel
Summary:	Development files for hipcub
Group:		Development/C++
Requires:	%{name} = %{version}-%{release}
Requires:	rocm-hip-devel
Requires:	rocprim-devel
Provides:	hipcub-devel = %{EVRD}

%description devel
Headers and CMake package for hipcub.

%prep
%autosetup -n hipcub

export CXX=hipcc
export CC=clang
# Strip host-only -mfpmath (hipcc forwards flags to amdgcn device compiles)
CXXFLAGS=$(printf '%s' "%{optflags}" | sed 's/-mfpmath=sse//g')
export CXXFLAGS
export CFLAGS="$CXXFLAGS"
%cmake %{rocm_cmake_fhs} %{rocm_cmake_gpu_targets_prim} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DCMAKE_CXX_FLAGS="$CXXFLAGS" \
	-DBUILD_TEST=OFF \
	-DBUILD_BENCHMARK=OFF \
	-DBUILD_EXAMPLE=OFF \
	-DBUILD_DOCS=OFF \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
if [ -d %{buildroot}/usr/lib/cmake/hipcub ] && [ ! -d %{buildroot}%{_libdir}/cmake/hipcub ]; then
	mkdir -p %{buildroot}%{_libdir}/cmake
	mv %{buildroot}/usr/lib/cmake/hipcub %{buildroot}%{_libdir}/cmake/
	rmdir %{buildroot}/usr/lib/cmake 2>/dev/null || true
	rmdir %{buildroot}/usr/lib 2>/dev/null || true
fi

%files
%license LICENSE.txt
%doc README.md
%exclude %{_docdir}/hipcub/LICENSE.txt

%files devel
%{_includedir}/hipcub/
%{_libdir}/cmake/hipcub/
