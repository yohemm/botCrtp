# Stratégie
- init(wallet, close)
- graph()
  - wallet
  - order
    - nb
    - avg
    - max
    - min
  - sell
    - nb
    - avg
    - max
    - min
  - buy
    - nb
    - avg
    - max
    - min
- task() -> percent/direction
- sell()
- buy()
- indicator_list : str*
- walletStart : int
- minSumByOrder
- maxSumByOrder
- canSell
- canBuy
- maxOrder
- close : pd.Series(timestamps, close, open, low, high)
- order : pd.Series(timestamps, coin, stableCoin)
  
# Indicator
- init(close)
- graph()
- ta{}
- name
- type
- results : pd.Series(trend1, ...)

# Backlog
- init()
- start()
- graph()
- strategy
- pair: str
- walletStart
- timeStart

<!-- ! OU SONT RANGE LES ORDER ? INDIC/BACK -->
# GESTION Du back test
La strat demande une date pour etre tester, si elle n'est pas préser en parametre alors mettre la dernier dans de l'obj df de la start
Il n'y a pas d'historique des ordres apres la vente dans strat mais ca doit etre stocker dans backlog