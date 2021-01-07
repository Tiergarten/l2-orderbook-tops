#include <iostream>
#include <set>
#include <vector>
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

vector<double> Book::get_tops(int top_n) {
	int out_len = 2*2*top_n;
	//double *out = new double[out_len]();
	vector<double> out;

	std::set<PriceLevel>::reverse_iterator rit = this->bids->rbegin();
	for (int i=0;i<out_len/2;i+=2) {
		if (rit != this->bids->rend()) {
			out.push_back(rit->price);
			out.push_back(rit->qty);
			rit++;
			continue;
		}
		out.push_back(0);
		out.push_back(0);
	}

	std::set<PriceLevel>::iterator it = this->asks->begin();
	for (int i=out_len/2;i < out_len;i+=2) {
		if (it != this->asks->end()) {
			out.push_back(it->price);
			out.push_back(it->qty);
			it++;
			continue;
		}
		out.push_back(0);
		out.push_back(0);
	}

	return out;
}
