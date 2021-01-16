all:
	pip uninstall l2-orderbook-tops -y
	pip install .
	pytest
