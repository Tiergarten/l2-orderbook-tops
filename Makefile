all:
	pip uninstall l2-orderbook-tops -y
	python setup.py install

	# TODO: pytest behaves differently based on what directory its run from
	cd tests && pytest && cd -
