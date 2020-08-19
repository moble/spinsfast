#if _MSC_VER && !__INTEL_COMPILER
#include <fftw3.h>
#else
#include <complex.h>
#undef complex
#define complex _Complex double
#include <fftw3.h>
#endif
