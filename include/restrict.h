/* The following tries to deal with the `restrict` keyword used by the */
/* spinsfast module when it is not defined. */
#ifndef restrict
#ifdef __restrict
#define restrict /* __restrict */
#else
#define restrict /* nothing */
#endif
#endif
