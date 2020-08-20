#if _MSC_VER && !__INTEL_COMPILER
#define FFTW_DLL
#include <fftw3.h>
#include <complex.h>
typedef double fftw_complex[2];
const _Dcomplex I = {0.0, 1.0};
#else
#include <complex.h>
#undef complex
#define complex _Complex double
#include <fftw3.h>
#endif
