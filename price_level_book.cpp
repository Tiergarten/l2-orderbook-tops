#include <iostream>
#include <set>
#include "price_level_book.h"
using namespace std;

PriceLevel::PriceLevel(double p, double q) {
	this->price = p;
	this->qty = q;
}

bool PriceLevel::operator<(const PriceLevel& rhs) const
{
	return price < rhs.price;
}

Book::Book() {
	this->bids = new set<PriceLevel>();
	this->asks = new set<PriceLevel>();
};

void Book::add_item(double price, double qty, set<PriceLevel> *side) {
	std::set<PriceLevel>::iterator it = side->begin();
	while (it != side->end()) {
		if (it->price == price) {
			side->erase(it);
			break;
		}
		it++;
	}

	if (qty != 0.0) {
		side->insert(PriceLevel(price, qty));
	}
}

void Book::add_ask(double price, double qty) {
	add_item(price, qty, this->asks);
}

void Book::add_bid(double price, double qty) {
	add_item(price, qty, this->bids);
}

double *Book::get_tops(int top_n) {
	int out_len = 2*2*top_n;
	double *out = new double[out_len]();

	std::set<PriceLevel>::iterator rit = this->bids->begin();
	for (int i=0;i<out_len/2;i+=2) {
		if (rit != this->bids->end()) {
			out[i] = rit->price;
			out[i+1] = rit->qty;
			rit++;
		}
	}

	std::set<PriceLevel>::iterator it = this->asks->begin();
	for (int i=out_len/2;i < out_len;i+=2) {
		if (it != this->asks->end()) {
			out[i] = it->price;
			out[i+1] = it->qty;
			it++;
		}
	}

	return out;
}
