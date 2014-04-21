## Process this file with automake to produce Makefile.in

TESTS = check_libsf
check_PROGRAMS = check_libsf
check_libsf_SOURCES = check_libsf.c $(top_builddir)/include/libsf.h $(top_builddir)/libsf/structs.h
check_libsf_CFLAGS = -I$(top_builddir)/include -I$(top_builddir)/libsf @CHECK_CFLAGS@
check_libsf_LDADD = $(top_builddir)/libsf/libsf.la @CHECK_LIBS@ -lm -lpthread -lrt