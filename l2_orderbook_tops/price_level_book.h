#ifndef PRICELEVEL_H
#define PRICELEVEL_H

#include <set>
using namespace std;

class PriceLevel {
	public:
		unsigned int price;
		mutable unsigned int qty;
		PriceLevel(unsigned int p, unsigned int q);
		bool operator<(const PriceLevel& rhs) const;
};

class Book {
	public:
		set<PriceLevel> *bids, *asks;
		unsigned int bid_qty, ask_qty;
		unsigned int *out;
		int tops_n;

		Book(int tops_n);
		int out_len();
		unsigned int get_resting_qty(unsigned int _side, unsigned int distance_from_mid);
		void add_item(unsigned int price, unsigned int qty, int _side);
		void add_ask(unsigned int price, unsigned int qty);
		void add_bid(unsigned int price, unsigned int qty);
		unsigned int *get_tops(unsigned int total_dollar_depth);
};
#endif
