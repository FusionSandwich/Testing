PYTHON ?= python3
LATEXMK ?= latexmk

.PHONY: verify paper clean

verify:
	$(PYTHON) computation/verify_target_a_coefficient.py > /tmp/target_a_coefficient_output.txt
	diff -u computation/target_a_coefficient_output.txt /tmp/target_a_coefficient_output.txt
	@echo "Target-A exact coefficient certificate: PASS"

paper:
	cd paper && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error erdos_1084_target_a.tex

clean:
	cd paper && $(LATEXMK) -C erdos_1084_target_a.tex
