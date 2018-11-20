/* The following tries to deal with the `inline` keyword used by the */
/* spinsfast module when it is not defined. */
#ifndef inline
#ifdef __inline
#define inline __inline
#else
#define inline /* nothing */
#endif
#endif
