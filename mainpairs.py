#!/usr/bin/env python3
import requests
from pycoingecko import CoinGeckoAPI
import operator
import random
from datetime import datetime
import winsound


def coins_by_spread(coins, min_volume=5000, min_spread=2, max_spread=50):

    coins_spread = []
    for coin in coins:

        prices = []

        for m in coin['market data']:
            vol = m['volume']
            if vol >= min_volume:
                prices.append(m['price_usd'])

        if len(prices) > 1:
            spread = ((max(prices) - min(prices)) / min(prices)) * 100
            if min_spread <= spread <= max_spread:
                coins_spread.append(
                    {'name': coin['name'], 'spread': spread, 'max price': max(prices), 'min price': min(prices)})

    coins_spread.sort(key=operator.itemgetter('spread'))

    return coins_spread


def get_coins_with_spread():

    exhanges = ['Mdex BSC'
                '0x Protocol'
                '1inch'
                '1inch Liquidity Protocol'
                '1inch Liquidity Protocol (BSC)'
                'Aave'
                'Allbit'
                'Anyswap'
                'ApeSwap'
                'Bakeryswap'
                'Balancer (v1)'
                'Balancer (v2)'
                'Bamboo Relay'
                'Bancor Network'
                'BepSwap'
                'Binance DEX'
                'Binance DEX (Mini)'
                'Birake'
                'Bisq'
                'Bitcratic'
                'Blockonix'
                'BSCswap'
                'BurgerSwap'
                'ComethSwap'
                'Compound Finance'
                'Curve Finance'
                'Cybex DEX'
                'DAOfi'
                'DDEX'
                'DeFi Swap'
                'Demex'
                'Deversifi'
                'dex.blue'
                'Dfyn'
                'DMM'
                'DODO'
                'Dodo BSC'
                'Dolomite'
                'dYdX'
                'Ethex'
                'Everbloom'
                'ForkDelta'
                'Gnosis Protocol'
                'Honeyswap'
                'Idex'
                'Joyso'
                'Julswap'
                'JustSwap'
                'Kyber Network'
                'Levinswap (xDai)'
                'Linkswap'
                'Loopring'
                'Loopring AMM'
                'Luaswap'
                'Mdex'
                'Mooniswap'
                'Nash'
                'Neblidex'
                'Newdex'
                'Nexus Mutual'
                'Niftex'
                'OasisDEX'
                'Orderbook.io'
                'Pancakeswap (Others)'
                'PancakeSwap (v1)'
                'PancakeSwap (v2)'
                'Pangolin'
                'PantherSwap'
                'Paraswap'
                'PoloniDEX'
                'Polyient Dex'
                'PolyZap'
                'Quickswap'
                'Radar Relay'
                'Raydium'
                'SakeSwap'
                'Sashimiswap'
                'Saturn Network'
                'SecretSwap'
                'Serum DEX'
                'SerumSwap'
                'SpiritSwap'
                'Spookyswap'
                'StellarTerm'
                'Sushiswap'
                'Sushiswap (Fantom)'
                'Sushiswap (Polygon POS)'
                'Sushiswap (xDai)'
                'Swapr'
                'Switcheo'
                'Swop.Fi'
                'Synthetix Exchange'
                'Terraswap'
                'Tokenlon'
                'TokenSets'
                'TomoDEX'
                'TronTrade'
                'Ubeswap'
                'Unicly'
                'Uniswap (v1)'
                'Uniswap (v2)'
                'Uniswap (v3)'
                'Value Liquid'
                'ViperSwap'
                'ViteX'
                'vSwap BSC'
                'WaultSwap'
                'Zero Exchange'
                'Zilswap'
                'ZKSwap'
               ]
    coins = get_coin_pair_data(include=exhanges)
    coins = coins_by_spread(coins)

    return coins


def get_coin_pair_data(exclude=[], include=[]):

    cg = CoinGeckoAPI()
    coins = cg.get_coins_list()
    random.shuffle(coins)
    coin_data = [{'name': 'BTC/USDT', 'market data': []}]

    for coin in coins:
        try:
            market_data = cg.get_coin_by_id(coin['id'])['tickers']

            for i in market_data:

                pairs_data = {}
                pair = i['base'] + '/' + i['target']
                market = i['market']['name']

                info = {'market': i['market']['name'],
                        'pair': pair,
                        'coin_name': i['base'],
                        'target': i['target'],
                        'volume': float(i['converted_volume']['usd']),
                        'price_usd': float(i['converted_last']['usd']),
                        #'price_usd': float(i['converted_last']['busd']),
                        #'price_usd': float(i['converted_last']['cusdc']),
                        #'price_usd': float(i['converted_last']['cusdt']),
                        #'price_usd': float(i['converted_last']['ust']),
                        'price_btc': float(i['converted_last']['btc']),
                        'price_eth': float(i['converted_last']['eth']),
                        'trade_url': i['trade_url'],
                        'last_traded_at': i['last_traded_at'],
                        'is_anomaly': i['is_anomaly'],
                        'trust_score': i['trust_score']
                        }

                if len(include) == 0:
                    if market not in exclude:
                        for x, dic in enumerate(coin_data):
                            if dic['name'] == pair:
                                coin_data[x]['market data'].append(info)
                                break
                        else:
                            pairs_data['name'] = pair
                            pairs_data['market data'] = []
                            pairs_data['market data'].append(info)
                            coin_data.append(pairs_data)

                else:
                    if market in include:
                        for x, dic in enumerate(coin_data):
                            if dic['name'] == pair:
                                coin_data[x]['market data'].append(info)
                                break
                        else:
                            pairs_data['name'] = pair
                            pairs_data['market data'] = []
                            pairs_data['market data'].append(info)
                            coin_data.append(pairs_data)

        except:
            continue

    return coin_data


def main():

    f = open('pair data\pairsOUT-'
             + datetime.now().strftime('%Y-%m-%d %H-%M-%S')+'.txt', "w")


    coins = get_coins_with_spread()
    for coin in coins:
        spread = ' spread: ' + str(coin['spread'])[:4] + '%'
        if len(coin['name']) < 30:
            #print(coin['name'], spread, '  Max price:', coin['max price'], '  Min price: ', coin['min price'])
            max_price = '  Max price:'+str(coin['max price'])
            min_price = '  Min price: '+str(coin['min price'])
            f_string = str(coin['name'])+str(spread)+max_price+min_price
            print(f_string)
            f.write(f_string+' \n')

    print('\nTime: '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    freq = 2500  # Set frequency To 2500 Hertz
    dur = 1000  # Set duration To 1000 ms == 1 second
    winsound.Beep(freq, dur)

    f.close()


if __name__ == "__main__":

    main()