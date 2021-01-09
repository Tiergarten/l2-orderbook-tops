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

int Book::out_len() {
    return (this->tops_n*2*2)+2;
}

Book::Book(int tops_n) {
	this->bids = new set<PriceLevel>();
	this->bid_qty = 0.0;

	this->asks = new set<PriceLevel>();
	this->ask_qty = 0.0;

	this->tops_n = tops_n;
	this->out = new double[this->out_len()]();
};

void Book::update_qty(double qty, int _side) {
    if (_side == 1) {
        this->bid_qty += qty;
    } else {
        this->ask_qty += qty;
    }
}

void Book::add_item(double price, double qty, int _side) {
	set<PriceLevel> *side;
	set<PriceLevel>::iterator it;
	PriceLevel in = PriceLevel(price, qty);

    if (_side == 1) {
        side = this->bids;
    } else {
        side = this->asks;
    }

	if ((it = side->find(in)) == side->end()) {
	    side->insert(in);
        this->update_qty(in.qty, _side);
	    return;
	}

    if (qty == 0.0) {
        this->update_qty(-(it->qty), _side);
        side->erase(it);
    } else {
        this->update_qty((qty - (it->qty)), _side);
        it->qty = qty;
    }
}

void Book::add_ask(double price, double qty) {
	add_item(price, qty, 0);
}

void Book::add_bid(double price, double qty) {
	add_item(price, qty, 1);
}

double *Book::get_tops() {
    // top_n * 2 (price/qty) * 2 (bid/ask) + 2 (total_bid_qty, total_ask_qty)
    int i;
    int _out_len = this->out_len();
	memset(this->out, 0, _out_len);

	std::set<PriceLevel>::reverse_iterator rit = this->bids->rbegin();
	for (i=0;i<_out_len/2;i+=2) {
		if (rit != this->bids->rend()) {
			this->out[i] = rit->price;
			this->out[i+1] = rit->qty;
			rit++;
		}
	}

	std::set<PriceLevel>::iterator it = this->asks->begin();
	for (i=_out_len/2;i < _out_len;i+=2) {
		if (it != this->asks->end()) {
			this->out[i] = it->price;
			this->out[i+1] = it->qty;
			it++;
		}
	}

	this->out[_out_len-2] = this->bid_qty;
	this->out[_out_len-1] = this->ask_qty;

	return this->out;
}
