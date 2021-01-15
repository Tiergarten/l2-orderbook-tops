all:
	pip uninstall l2-orderbook-tops -y
	pip install .
	cd tests && python plb_test.py; cd -
