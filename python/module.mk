LIB+=$(LIBDIR)/spinsfast.so

$(LIBDIR)/spinsfast.so : python/spinsfast_module.c setup.py $(LIBDIR)/libspinsfast.a
	python setup.py build --build-base $(OBJDIR) install --install-lib $(LIBDIR)
