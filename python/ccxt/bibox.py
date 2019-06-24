# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable


class bibox (Exchange):

    def describe(self):
        return self.deep_extend(super(bibox, self).describe(), {
            'id': 'bibox',
            'name': 'Bibox',
            'countries': ['CN', 'US', 'KR'],
            'version': 'v1',
            'has': {
                'CORS': False,
                'publicAPI': False,
                'fetchBalance': True,
                'fetchDeposits': True,
                'fetchWithdrawals': True,
                'fetchCurrencies': True,
                'fetchDepositAddress': True,
                'fetchFundingFees': True,
                'fetchTickers': True,
                'fetchOrder': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
                'createMarketOrder': False,  # or they will return https://github.com/ccxt/ccxt/issues/2338
                'withdraw': True,
            },
            'timeframes': {
                '1m': '1min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '2h': '2hour',
                '4h': '4hour',
                '6h': '6hour',
                '12h': '12hour',
                '1d': 'day',
                '1w': 'week',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/34902611-2be8bf1a-f830-11e7-91a2-11b2f292e750.jpg',
                'api': 'https://api.bibox.com',
                'www': 'https://www.bibox.com',
                'doc': [
                    'https://github.com/Biboxcom/api_reference/wiki/home_en',
                    'https://github.com/Biboxcom/api_reference/wiki/api_reference',
                ],
                'fees': 'https://bibox.zendesk.com/hc/en-us/articles/115004417013-Fee-Structure-on-Bibox',
                'referral': 'https://www.bibox.com/signPage?id=11114745&lang=en',
            },
            'api': {
                'public': {
                    'post': [
                        # TODO: rework for full endpoint/cmd paths here
                        'mdata',
                    ],
                    'get': [
                        'mdata',
                    ],
                },
                'private': {
                    'post': [
                        'user',
                        'orderpending',
                        'transfer',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.001,
                    'maker': 0.001,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {},
                    'deposit': {},
                },
            },
            'exceptions': {
                '2021': InsufficientFunds,  # Insufficient balance available for withdrawal
                '2015': AuthenticationError,  # Google authenticator is wrong
                '2027': InsufficientFunds,  # Insufficient balance available(for trade)
                '2033': OrderNotFound,  # operation failednot  Orders have been completed or revoked
                '2067': InvalidOrder,  # Does not support market orders
                '2068': InvalidOrder,  # The number of orders can not be less than
                '2085': InvalidOrder,  # Order quantity is too small
                '3012': AuthenticationError,  # invalid apiKey
                '3024': PermissionDenied,  # wrong apikey permissions
                '3025': AuthenticationError,  # signature failed
                '4000': ExchangeNotAvailable,  # current network is unstable
                '4003': DDoSProtection,  # server busy please try again later
            },
            'commonCurrencies': {
                'KEY': 'Bihu',
                'PAI': 'PCHAIN',
            },
        })

    def fetch_markets(self, params={}):
        request = {
            'cmd': 'marketAll',
        }
        response = self.publicGetMdata(self.extend(request, params))
        #
        #     {
        #         "result": [
        #             {
        #                 "is_hide":0,
        #                 "high_cny":"1.9478",
        #                 "amount":"272.41",
        #                 "coin_symbol":"BIX",
        #                 "last":"0.00002487",
        #                 "currency_symbol":"BTC",
        #                 "change":"+0.00000073",
        #                 "low_cny":"1.7408",
        #                 "base_last_cny":"1.84538041",
        #                 "area_id":7,
        #                 "percent":"+3.02%",
        #                 "last_cny":"1.8454",
        #                 "high":"0.00002625",
        #                 "low":"0.00002346",
        #                 "pair_type":0,
        #                 "last_usd":"0.2686",
        #                 "vol24H":"10940613",
        #                 "id":1,
        #                 "high_usd":"0.2835",
        #                 "low_usd":"0.2534"
        #             }
        #         ],
        #         "cmd":"marketAll",
        #         "ver":"1.1"
        #     }
        #
        markets = self.safe_value(response, 'result')
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            numericId = self.safe_integer(market, 'id')
            baseId = self.safe_string(market, 'coin_symbol')
            quoteId = self.safe_string(market, 'currency_symbol')
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            id = baseId + '_' + quoteId
            precision = {
                'amount': 4,
                'price': 8,
            }
            result.append({
                'id': id,
                'numericId': numericId,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': base,
                'quoteId': quote,
                'active': True,
                'info': market,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                },
            })
        return result

    def parse_ticker(self, ticker, market=None):
        # we don't set values that are not defined by the exchange
        timestamp = self.safe_integer(ticker, 'timestamp')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        else:
            baseId = self.safe_string(ticker, 'coin_symbol')
            quoteId = self.safe_string(ticker, 'currency_symbol')
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
        last = self.safe_float(ticker, 'last')
        change = self.safe_float(ticker, 'change')
        baseVolume = self.safe_float_2(ticker, 'vol', 'vol24H')
        open = None
        if (last is not None) and(change is not None):
            open = last - change
        percentage = self.safe_string(ticker, 'percent')
        if percentage is not None:
            percentage = percentage.replace('%', '')
            percentage = float(percentage)
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': self.safe_float(ticker, 'amount'),
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'cmd': 'ticker',
            'pair': market['id'],
        }
        response = self.publicGetMdata(self.extend(request, params))
        return self.parse_ticker(response['result'], market)

    def parse_tickers(self, rawTickers, symbols=None):
        tickers = []
        for i in range(0, len(rawTickers)):
            ticker = self.parse_ticker(rawTickers[i])
            if (symbols is None) or (self.in_array(ticker['symbol'], symbols)):
                tickers.append(ticker)
        return tickers

    def fetch_tickers(self, symbols=None, params={}):
        request = {
            'cmd': 'marketAll',
        }
        response = self.publicGetMdata(self.extend(request, params))
        tickers = self.parse_tickers(response['result'], symbols)
        return self.index_by(tickers, 'symbol')

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_integer_2(trade, 'time', 'createdAt')
        side = self.safe_integer_2(trade, 'side', 'order_side')
        side = 'buy' if (side == 1) else 'sell'
        symbol = None
        if market is None:
            marketId = self.safe_string(trade, 'pair')
            if marketId is None:
                baseId = self.safe_string(trade, 'coin_symbol')
                quoteId = self.safe_string(trade, 'currency_symbol')
                if (baseId is not None) and(quoteId is not None):
                    marketId = baseId + '_' + quoteId
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        fee = None
        feeCost = self.safe_float(trade, 'fee')
        feeCurrency = self.safe_string(trade, 'fee_symbol')
        if feeCurrency is not None:
            if feeCurrency in self.currencies_by_id:
                feeCurrency = self.currencies_by_id[feeCurrency]['code']
            else:
                feeCurrency = self.common_currency_code(feeCurrency)
        feeRate = None  # todo: deduce from market if market is defined
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if amount is not None:
            if cost is not None:
                cost = price * amount
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': feeCurrency,
                'rate': feeRate,
            }
        id = self.safe_string(trade, 'id')
        return {
            'info': trade,
            'id': id,
            'order': None,  # Bibox does not have it(documented) yet
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': 'limit',
            'takerOrMaker': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'cmd': 'deals',
            'pair': market['id'],
        }
        if limit is not None:
            request['size'] = limit  # default = 200
        response = self.publicGetMdata(self.extend(request, params))
        return self.parse_trades(response['result'], market, since, limit)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'cmd': 'depth',
            'pair': market['id'],
        }
        if limit is not None:
            request['size'] = limit  # default = 200
        response = self.publicGetMdata(self.extend(request, params))
        return self.parse_order_book(response['result'], self.safe_float(response['result'], 'update_time'), 'bids', 'asks', 'price', 'volume')

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv['time'],
            self.safe_float(ohlcv, 'open'),
            self.safe_float(ohlcv, 'high'),
            self.safe_float(ohlcv, 'low'),
            self.safe_float(ohlcv, 'close'),
            self.safe_float(ohlcv, 'vol'),
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=1000, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'cmd': 'kline',
            'pair': market['id'],
            'period': self.timeframes[timeframe],
            'size': limit,
        }
        response = self.publicGetMdata(self.extend(request, params))
        return self.parse_ohlcvs(response['result'], market, timeframe, since, limit)

    def fetch_currencies(self, params={}):
        if not self.apiKey or not self.secret:
            raise AuthenticationError(self.id + " fetchCurrencies is an authenticated endpoint, therefore it requires 'apiKey' and 'secret' credentials. If you don't need currency details, set exchange.has['fetchCurrencies'] = False before calling its methods.")
        request = {
            'cmd': 'transfer/coinList',
            'body': {},
        }
        response = self.privatePostTransfer(self.extend(request, params))
        currencies = self.safe_value(response, 'result')
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            id = self.safe_string(currency, 'symbol')
            name = self.safe_string(currency, 'name')
            code = self.common_currency_code(id)
            precision = 8
            deposit = self.safe_value(currency, 'enable_deposit')
            withdraw = self.safe_value(currency, 'enable_withdraw')
            active = (deposit and withdraw)
            result[code] = {
                'id': id,
                'code': code,
                'info': currency,
                'name': name,
                'active': active,
                'fee': None,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision),
                        'max': math.pow(10, precision),
                    },
                    'price': {
                        'min': math.pow(10, -precision),
                        'max': math.pow(10, precision),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': None,
                        'max': math.pow(10, precision),
                    },
                },
            }
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        request = {
            'cmd': 'transfer/mainAssets',
            'body': self.extend({
                'select': 1,
            }, params),
        }
        response = self.privatePostTransfer(request)
        balances = self.safe_value(response, 'result')
        result = {'info': balances}
        indexed = None
        if 'assets_list' in balances:
            indexed = self.index_by(balances['assets_list'], 'coin_symbol')
        else:
            indexed = balances
        keys = list(indexed.keys())
        for i in range(0, len(keys)):
            id = keys[i]
            code = id.upper()
            if code.find('TOTAL_') >= 0:
                code = code[6:]
            if code in self.currencies_by_id:
                code = self.currencies_by_id[code]['code']
            account = self.account()
            balance = indexed[id]
            if isinstance(balance, basestring):
                balance = float(balance)
                account['free'] = balance
                account['used'] = 0.0
                account['total'] = balance
            else:
                account['free'] = self.safe_float(balance, 'balance')
                account['used'] = self.safe_float(balance, 'freeze')
            result[code] = account
        return self.parse_balance(result)

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        currency = None
        request = {
            'page': 1,
        }
        if code is not None:
            currency = self.currency(code)
            request['symbol'] = currency['id']
        if limit is not None:
            request['size'] = limit
        else:
            request['size'] = 100
        response = self.privatePostTransfer({
            'cmd': 'transfer/transferInList',
            'body': self.extend(request, params),
        })
        deposits = self.safe_value(response['result'], 'items', [])
        for i in range(0, len(deposits)):
            deposits[i]['type'] = 'deposit'
        return self.parseTransactions(deposits, currency, since, limit)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        currency = None
        request = {
            'page': 1,
        }
        if code is not None:
            currency = self.currency(code)
            request['symbol'] = currency['id']
        if limit is not None:
            request['size'] = limit
        else:
            request['size'] = 100
        response = self.privatePostTransfer({
            'cmd': 'transfer/transferOutList',
            'body': self.extend(request, params),
        })
        withdrawals = self.safe_value(response['result'], 'items', [])
        for i in range(0, len(withdrawals)):
            withdrawals[i]['type'] = 'withdrawal'
        return self.parseTransactions(withdrawals, currency, since, limit)

    def parse_transaction(self, transaction, currency=None):
        #
        # fetchDeposits
        #
        #     {
        #         'id': 1023291,
        #         'coin_symbol': 'ETH',
        #         'to_address': '0x7263....',
        #         'amount': '0.49170000',
        #         'confirmCount': '16',
        #         'createdAt': 1553123867000,
        #         'status': 2
        #     }
        #
        # fetchWithdrawals
        #
        #     {
        #         'id': 521844,
        #         'coin_symbol': 'ETH',
        #         'to_address': '0xfd4e....',
        #         'addr_remark': '',
        #         'amount': '0.39452750',
        #         'fee': '0.00600000',
        #         'createdAt': 1553226906000,
        #         'memo': '',
        #         'status': 3
        #     }
        #
        id = self.safe_string(transaction, 'id')
        address = self.safe_string(transaction, 'to_address')
        code = None
        currencyId = self.safe_string(transaction, 'coin_symbol')
        if currencyId in self.currencies_by_id:
            currency = self.currencies_by_id[currencyId]
        else:
            code = self.common_currency_code(currencyId)
        if currency is not None:
            code = currency['code']
        timestamp = self.safe_string(transaction, 'createdAt')
        tag = self.safe_string(transaction, 'addr_remark')
        type = self.safe_string(transaction, 'type')
        status = self.parse_transaction_status_by_type(self.safe_string(transaction, 'status'), type)
        amount = self.safe_float(transaction, 'amount')
        feeCost = self.safe_float(transaction, 'fee')
        if type == 'deposit':
            feeCost = 0
            tag = None
        fee = {
            'cost': feeCost,
            'currency': code,
        }
        return {
            'info': transaction,
            'id': id,
            'txid': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'address': address,
            'tag': tag,
            'type': type,
            'amount': amount,
            'currency': code,
            'status': status,
            'updated': None,
            'fee': fee,
        }

    def parse_transaction_status_by_type(self, status, type=None):
        statuses = {
            'deposit': {
                '1': 'pending',
                '2': 'ok',
            },
            'withdrawal': {
                '0': 'pending',
                '3': 'ok',
            },
        }
        return self.safe_string(self.safe_value(statuses, type, {}), status, status)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        orderType = 2 if (type == 'limit') else 1
        orderSide = 1 if (side == 'buy') else 2
        request = {
            'cmd': 'orderpending/trade',
            'body': self.extend({
                'pair': market['id'],
                'account_type': 0,
                'order_type': orderType,
                'order_side': orderSide,
                'pay_bix': 0,
                'amount': amount,
                'price': price,
            }, params),
        }
        response = self.privatePostOrderpending(request)
        return {
            'info': response,
            'id': self.safe_string(response, 'result'),
        }

    def cancel_order(self, id, symbol=None, params={}):
        request = {
            'cmd': 'orderpending/cancelTrade',
            'body': self.extend({
                'orders_id': id,
            }, params),
        }
        response = self.privatePostOrderpending(request)
        return response

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'cmd': 'orderpending/order',
            'body': self.extend({
                'id': str(id),
                'account_type': 0,  # 0 = spot account
            }, params),
        }
        response = self.privatePostOrderpending(request)
        order = self.safe_value(response, 'result')
        if self.is_empty(order):
            raise OrderNotFound(self.id + ' order ' + id + ' not found')
        return self.parse_order(order)

    def parse_order(self, order, market=None):
        symbol = None
        if market is None:
            marketId = None
            baseId = self.safe_string(order, 'coin_symbol')
            quoteId = self.safe_string(order, 'currency_symbol')
            if (baseId is not None) and(quoteId is not None):
                marketId = baseId + '_' + quoteId
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        type = 'market' if (order['order_type'] == 1) else 'limit'
        timestamp = order['createdAt']
        price = self.safe_float(order, 'price')
        average = self.safe_float(order, 'deal_price')
        filled = self.safe_float(order, 'deal_amount')
        amount = self.safe_float(order, 'amount')
        cost = self.safe_float_2(order, 'deal_money', 'money')
        remaining = None
        if filled is not None:
            if amount is not None:
                remaining = amount - filled
            if cost is None:
                cost = price * filled
        side = 'buy' if (order['order_side'] == 1) else 'sell'
        status = self.parse_order_status(self.safe_string(order, 'status'))
        id = self.safe_string(order, 'id')
        feeCost = self.safe_float(order, 'fee')
        fee = None
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': None,
            }
        cost = cost if cost else float(price) * filled
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'average': average,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
        }

    def parse_order_status(self, status):
        statuses = {
            # original comments from bibox:
            '1': 'open',  # pending
            '2': 'open',  # part completed
            '3': 'closed',  # completed
            '4': 'canceled',  # part canceled
            '5': 'canceled',  # canceled
            '6': 'canceled',  # canceling
        }
        return self.safe_string(statuses, status, status)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        market = None
        pair = None
        if symbol is not None:
            self.load_markets()
            market = self.market(symbol)
            pair = market['id']
        size = limit if (limit) else 200
        request = {
            'cmd': 'orderpending/orderPendingList',
            'body': self.extend({
                'pair': pair,
                'account_type': 0,  # 0 - regular, 1 - margin
                'page': 1,
                'size': size,
            }, params),
        }
        response = self.privatePostOrderpending(request)
        orders = self.safe_value(response['result'], 'items', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=200, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchClosedOrders requires a `symbol` argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'cmd': 'orderpending/pendingHistoryList',
            'body': self.extend({
                'pair': market['id'],
                'account_type': 0,  # 0 - regular, 1 - margin
                'page': 1,
                'size': limit,
            }, params),
        }
        response = self.privatePostOrderpending(request)
        orders = self.safe_value(response['result'], 'items', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a `symbol` argument')
        self.load_markets()
        market = self.market(symbol)
        size = limit if (limit) else 200
        request = {
            'cmd': 'orderpending/orderHistoryList',
            'body': self.extend({
                'pair': market['id'],
                'account_type': 0,  # 0 - regular, 1 - margin
                'page': 1,
                'size': size,
                'coin_symbol': market['baseId'],
                'currency_symbol': market['quoteId'],
            }, params),
        }
        response = self.privatePostOrderpending(request)
        trades = self.safe_value(response['result'], 'items', [])
        return self.parse_trades(trades, market, since, limit)

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {
            'cmd': 'transfer/transferIn',
            'body': self.extend({
                'coin_symbol': currency['id'],
            }, params),
        }
        response = self.privatePostTransfer(request)
        address = self.safe_string(response, 'result')
        tag = None  # todo: figure self out
        return {
            'currency': code,
            'address': address,
            'tag': tag,
            'info': response,
        }

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        if self.password is None:
            if not('trade_pwd' in list(params.keys())):
                raise ExchangeError(self.id + ' withdraw() requires self.password set on the exchange instance or a trade_pwd parameter')
        if not('totp_code' in list(params.keys())):
            raise ExchangeError(self.id + ' withdraw() requires a totp_code parameter for 2FA authentication')
        request = {
            'trade_pwd': self.password,
            'coin_symbol': currency['id'],
            'amount': amount,
            'addr': address,
        }
        if tag is not None:
            request['address_remark'] = tag
        response = self.privatePostTransfer({
            'cmd': 'transfer/transferOut',
            'body': self.extend(request, params),
        })
        return {
            'info': response,
            'id': None,
        }

    def fetch_funding_fees(self, codes=None, params={}):
        # by default it will try load withdrawal fees of all currencies(with separate requests)
        # however if you define codes = ['ETH', 'BTC'] in args it will only load those
        self.load_markets()
        withdrawFees = {}
        info = {}
        if codes is None:
            codes = list(self.currencies.keys())
        for i in range(0, len(codes)):
            code = codes[i]
            currency = self.currency(code)
            request = {
                'cmd': 'transfer/coinConfig',
                'body': self.extend({
                    'coin_symbol': currency['id'],
                }, params),
            }
            response = self.privatePostTransfer(request)
            info[code] = response
            withdrawFees[code] = self.safe_float(response['result'], 'withdraw_fee')
        return {
            'info': info,
            'withdraw': withdrawFees,
            'deposit': {},
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + path
        cmds = self.json([params])
        if api == 'public':
            if method != 'GET':
                body = {'cmds': cmds}
            elif params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            body = {
                'cmds': cmds,
                'apikey': self.apiKey,
                'sign': self.hmac(self.encode(cmds), self.encode(self.secret), hashlib.md5),
            }
        if body is not None:
            body = self.json(body, {'convertArraysToObjects': True})
        headers = {'Content-Type': 'application/json'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response):
        if response is None:
            return
        if 'error' in response:
            if 'code' in response['error']:
                code = self.safe_string(response['error'], 'code')
                feedback = self.id + ' ' + body
                exceptions = self.exceptions
                if code in exceptions:
                    raise exceptions[code](feedback)
                else:
                    raise ExchangeError(feedback)
            raise ExchangeError(self.id + ': "error" in response: ' + body)
        if not('result' in list(response.keys())):
            raise ExchangeError(self.id + ' ' + body)

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if method == 'GET':
            return response
        else:
            return response['result'][0]
