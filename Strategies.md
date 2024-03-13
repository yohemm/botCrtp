# Elément de base
- indicateur de tendance:
  Objectif : Trouver les tendances aucier et baissier Et déclencher un potentiel achat
  Ex :
  - Croisement de moyenne mobile 
- Filtre de volatilité:
  Objectif : detecter les périodes de range
  Ex :
  - Bolliger bands
- Tendance long therme:
  Objectif : diminué les risques de fake out en détectant les grandes phasese tendance
  Ex :
  - Super Trend: Atr_muliplicateur ~= 7
  - MA200 VS sma:
    - Haussier : MA < sma 
    - Baissier : MA > sma 
  - MACD:
- Momentum:
  Objectif : Déclencher une action au bon moment
  Ex :
  - Stochastic RSI :  K2~=1
    - achat <= zone neutre 
    - vent >= zone neutre 
  - attendre un pull back
    - si break: attendre de retoucher la trend pour vendre
    - sinn: acheter

# Reflexion
## The Filter
### Besoin
Néssécité de stocker tout les Achat en cour pour préparer la revente
Stocker PotentielAchat/Vente
Vente implique supression d'Achat en cour
### Strats
#### Pour Achat : 
  ##### croisement sma Haussier:
    Bolliger bands filtre de volatilité
    > 10:
      Stochastic RSI / Pull Back?
    sinn:
      - longtherme  MA200 VS sma:
        - Haussier: 
          Stochastic RSI / Pull Back?
        - Baissier: 
          - Achat en attent
 
  Achat en attente:
  vérif a chaque tour de condition jusqu'a suppression de l'element si croisement baisier
#### Pour Vente : 
  ##### Trade __prositif__ : 
    __croisement sma__ Baissier:
      Bolliger bands filtre de volatilité
      > 10:
        vend
      sinn:
        - longtherme __MA200 VS sma__:
          - Baissier: 
            Stochastic RSI / Pull Back?
          - Haussier: 
          - Vente en attent
          - 
  ##### Trade __négatif__:
    - longtherme __MA200 VS sma__:
      - Haussier: 
        __sma__ Baissier:
          Bolliger bands filtre de volatilité
          > 10:
            vend
          sinon:
            attendre
        __sma__ Haussier:
          attent
      - Baissier: 
          Stochastic RSI / Pull Back?
         
Que Fait stratégie
Courbe -> Indicateur
date() -> BTC, Stable
Nécessite de gérere les courbe de l'indicateur sur une longuer périodes et de commencé a une date plus récente
Stocker
- Vente en attente:
  vérif a chaque tour de condition Trade négatif de jusqu'a suppression de l'element si croisement haussier

# Ultime DCA
Acheter progressivement lors des baisse si on a des stableCoin
Vendre lors des hausses si on a des crypto
Faire un action proportionel au pourcentage de hausse par rapport au movement du marcher
Déduire le meilleur moment pour effectuer une action a partir d'indicateur 
## Variable
Achat prix moyen sur la crypto