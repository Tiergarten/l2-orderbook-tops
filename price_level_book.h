#ifndef PRICELEVEL_H
#define PRICELEVEL_H

#include <set>
using namespace std;

class PriceLevel {
	public:
		double price;
		mutable double qty;
		PriceLevel(double p, double q);
		bool operator<(const PriceLevel& rhs) const;
};

class Book {
	public:
		set<PriceLevel> *bids, *asks;
		double bid_qty, ask_qty;
		double *out;
		int tops_n;

		Book(int tops_n);
		int out_len();
		void update_qty(double price, double qty, int _side);
		void add_item(double price, double qty, int _side);
		void add_ask(double price, double qty);
		void add_bid(double price, double qty);
		double *get_tops();
};
#endif
