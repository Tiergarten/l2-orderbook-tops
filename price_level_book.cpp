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

Book::Book(int tops_n) {
	this->bids = new set<PriceLevel>();
	this->asks = new set<PriceLevel>();

	this->tops_n = tops_n;
	this->out = new double[this->tops_n*2*2]();
};

void Book::add_item(double price, double qty, set<PriceLevel> *side) {
	PriceLevel in = PriceLevel(price, qty);

	std::set<PriceLevel>::iterator it = side->find(in);
	if (it != side->end()) {
		if (qty == 0.0) {
			side->erase(it);
		} else {
			it->qty = qty;
		}
		return;
	}

	side->insert(in);
}

void Book::add_ask(double price, double qty) {
	add_item(price, qty, this->asks);
}

void Book::add_bid(double price, double qty) {
	add_item(price, qty, this->bids);
}

double *Book::get_tops() {
	int out_len = this->tops_n*2*2;
	memset(this->out, 0, out_len);

	std::set<PriceLevel>::reverse_iterator rit = this->bids->rbegin();
	for (int i=0;i<out_len/2;i+=2) {
		if (rit != this->bids->rend()) {
			this->out[i] = rit->price;
			this->out[i+1] = rit->qty;
			rit++;
		}
	}

	std::set<PriceLevel>::iterator it = this->asks->begin();
	for (int i=out_len/2;i < out_len;i+=2) {
		if (it != this->asks->end()) {
			this->out[i] = it->price;
			this->out[i+1] = it->qty;
			it++;
		}
	}

	return this->out;
}
