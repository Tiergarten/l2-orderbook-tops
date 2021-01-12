#include <iostream>
#include <set>
#include <cstdlib>

#include "price_level_book.h"
using namespace std;

PriceLevel::PriceLevel(unsigned int p, unsigned int q) {
	this->price = p;
	this->qty = q;
}

bool PriceLevel::operator<(const PriceLevel& rhs) const
{
	return price < rhs.price;
}

int Book::out_len() {
    // tops_n * price/qty * bid/ask + total_bid/total_ask
    return (this->tops_n*2*2)+2;
}

Book::Book(int tops_n) {
	this->bids = new set<PriceLevel>();
	this->asks = new set<PriceLevel>();

	this->tops_n = tops_n;
	this->out = new unsigned int[this->out_len()]();
};

void Book::add_item(unsigned int price, unsigned int qty, int _side) {
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
	    return;
	}

    if (qty == 0.0) {
        side->erase(it);
    } else {
        it->qty = qty;
    }
}

void Book::add_ask(unsigned int price, unsigned int qty) {
	add_item(price, qty, 0);
}

void Book::add_bid(unsigned int price, unsigned int qty) {
	add_item(price, qty, 1);
}

// TODO: refactor this 
unsigned int Book::get_resting_qty(unsigned int _side, unsigned int distance_from_mid) {
    unsigned int out = 0;
    unsigned int start = 0;
    set<PriceLevel> *side;

    if (_side == 1) {
        side = this->bids;
    } else {
        side = this->asks;
    }

    if (side->begin() == side->end()) {
	    return 0;
    }

    if (_side == 0) {
        // Increasing
        std::set<PriceLevel>::iterator it = side->begin();
        start = it->price;
	
        while (it != side->end()) {
            if ((it->price - start) > distance_from_mid) {
                break;
            }

            out += it->qty;
            it++;
        }


    } else {
        // Decreasing
        std::set<PriceLevel>::reverse_iterator rit = side->rbegin();
        start = rit->price;

        while (rit != side->rend()) {
            if ((start - rit->price) > distance_from_mid) {
                break;
            }

            out += rit->qty;
            rit++;
        }

    }

    return out;
}

unsigned int *Book::get_tops(unsigned int total_dollar_depth) {
    // top_n * 2 (price/qty) * 2 (bid/ask) + 2 (total_bid_qty, total_ask_qty)
    int i;
    int _out_len = this->out_len();
    memset(this->out, 0, _out_len);

	std::set<PriceLevel>::reverse_iterator rit = this->bids->rbegin();
	for (i=0;i<this->tops_n*2;i+=2) {
		if (rit != this->bids->rend()) {
			this->out[i] = rit->price;
			this->out[i+1] = rit->qty;
			rit++;
		}
	}

	std::set<PriceLevel>::iterator it = this->asks->begin();
	for (;i < this->tops_n*2*2;i+=2) {
		if (it != this->asks->end()) {
			this->out[i] = it->price;
			this->out[i+1] = it->qty;
			it++;
		}
	}

	if (total_dollar_depth > 0) {
		this->out[_out_len-2] = this->get_resting_qty(1, total_dollar_depth);
		this->out[_out_len-1] = this->get_resting_qty(0, total_dollar_depth);
	}

	return this->out;
}
