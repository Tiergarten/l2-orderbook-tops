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
		double *out;
		int tops_n;
		Book(int tops_n);
		void add_item(double price, double qty, set<PriceLevel> *side);
		void add_ask(double price, double qty);
		void add_bid(double price, double qty);
		double *get_tops();
};
#endif
