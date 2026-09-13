.PHONY: test doctor demo package

test:
	PYTHONPATH=src python -m unittest discover -s tests -v

doctor:
	PYTHONPATH=src python -m ec doctor

demo:
	PYTHONPATH=src python -m ec demo-manufacturing

package:
	python scripts/package_release.py
