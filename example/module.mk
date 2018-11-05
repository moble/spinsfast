EXEC+=$(EXECDIR)/example_spin $(EXECDIR)/example_multispin $(EXECDIR)/example_multispin_looped $(EXECDIR)/example_iqu

LIB_example:= -Llib -lspinsfast $(LIBFFTW) -lm

$(EXECDIR)/example_spin : example/example_spin.c lib/libspinsfast.a
	$(CC) $(INC) -o $@ $< $(LIB_example)

$(EXECDIR)/example_multispin : example/example_multispin.c lib/libspinsfast.a
	$(CC) $(INC) -o $@ $< $(LIB_example)

$(EXECDIR)/example_multispin_looped : example/example_multispin_looped.c lib/libspinsfast.a
	$(CC) $(INC) -o $@ $< $(LIB_example)

$(EXECDIR)/example_iqu : example/example_iqu.c lib/libspinsfast.a
	$(CC) $(INC) -o $@ $< $(LIB_example)
