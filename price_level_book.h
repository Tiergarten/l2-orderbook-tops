#ifndef PRICELEVEL_H
#define PRICELEVEL_H

#include <set>
#include <vector>
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
		Book();
		void add_item(double price, double qty, set<PriceLevel> *side);
		void add_ask(double price, double qty);
		void add_bid(double price, double qty);
		vector<double> get_tops(int top_n);
};
#endif
