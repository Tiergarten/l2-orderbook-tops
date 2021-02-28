all: clean
	pip uninstall l2-orderbook-tops -y
	python setup.py install

	# TODO: pytest behaves differently based on what directory its run from
	cd tests && pytest -s && cd -

clean:
	rm l2_orderbook_tops/*.so || true
	rm -rf l2_orderbook_tops.egg-info
	rm l2_orderbook_tops/py_price_level_book.cpp
	rm l2_orderbook_tops/py_price_level_book.html

