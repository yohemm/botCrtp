sma <|sma > >|sma: haussier else baissier
bool : range < 10
rsi > 70 ne pas achter, <30 ne pas vendre
ema >sma > ema: lg therme haussier else baissier
2 bougie rouge in ?

- ou place les supressions d'ordre
- vente achat symétrique?

1.
```
si rsi < 70:
    si croisement haussier:
        order
        order:startsell del
    si order:start
        si not range bool AND rsi < 70:
            achat
si rsi > 30:
    si croisement baissier:
        order:start del 
        order
    si order:startsell
        si not range bool AND rsi > 30:
            vente
```
2.
```
si rsi < 70:
    si croisement haussier:
        order
    si order:start
        si rsi < 70:
            si lg themer haussier:
                achat
            sinn:
                if bool > 10:
                    achat
si rsi > 30:
    si croisement baissier:
        order
    si order:startsell
        si (not range bool | lgthermeBaissier ) AND rsi > 30:
            vente
```