#!/bin/bash
# $Id:$

./order_data_vars.py | sort > YahooFinanceDataVariables.lst
grep -i 'real-time' YahooFinanceDataVariables.lst > YahooFinanceDataVariables.real-time
grep -iv 'real-time' YahooFinanceDataVariables.lst > YahooFinanceDataVariables.basic
# leftover YahooFinanceDataVariables.dict (made by ./order_data_vars.py)