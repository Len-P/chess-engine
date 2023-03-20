---
author:
- Faber Pas, Len Pasic, Ayoub Elgharrafi
date: December 2022
title: "AI opdracht 4: Chess AI"
---

# Inleiding

Schaak is een uitgebreid spel met ontzettend veel mogelijkheden. Een
schaak AI zal dus niet alleen veel mogelijke zetten moeten doorlopen,
maar ook voor elke zet snel moeten kunnen berekenen hoe goed die zet is.
Om dit te doen maakt men gebruik van een utility functie. Dit is een
functie die voor elke zet berekent wat de waarde van die zet is aan de
hand van enkele features. Het zijn vooral die features en hun
implementatie die de sterkte van de AI zullen bepalen.

# Features

De code achter de zaken die in deze sectie besproken worden wordt
gevonden in chessutility.py.

## Material value

Een eerste en zeer belangrijke feature die ingevoerd werd is de waarde
van de stukken op het bord. Het is in een schaakspel belangrijk om geen
stukken te verliezen, dat is intuïtief duidelijk. Verschillende stukken
hebben verschillende waarden, in verhouding hieronder opgelijst:

-   Pion: waarde 1

-   Paard, loper: waarde 3

-   Toren: waarde 5

-   Dame: waarde 9

Dit wordt op een vrij simpele manier geïmplementeerd: de *materialscore*
functie kijkt welke stukken nog op het bord staan per kleur, en trekt de
waarde van de zwarte stukken van die van de witte stukken af. De
returned value is dus de utility voor wit. De relatieve waarden van de
stukken werden hier maal 100 gedaan, bv. 300 voor een paard.

## Position value

Ook de positie van de stukken op het bord is natuurlijk van belang. Een
koning moet niet in het midden van het veld staan, maar ergens beschermd
in een hoekje. Een pion is niet veel waard, maar kan veranderen in een
dame wanneer hij het veld oversteekt. In het algemeen zijn de waarden
die men kan verdienen voor een goede positionering een ordegrootte
kleiner dan de waarden van de stukken zelf.

Om dit te implementeren maken we gebruik van piece-square table (PST):

Een voorbeeld van een PST voor het paard is te zien in figuur
[1](#PST){reference-type="ref" reference="PST"}

[Een voorbeeld van een piece-square table voor het paard. Links de
waarden die de computer krijgt, rechts een grafische illustratie.]{#PST
.image .placeholder original-image-src="https://github.com/Len-P/chess-engine/blob/master/PST.png?raw=true"
original-image-title="fig:" width="100%"}

## Castle score

Rokeren is een speciale zet in schaak, en zou een grote waarde moeten
dragen aangezien het de koning in veiligheid brengt en de toren in een
goede positie brengt. Onrechtstreeks zit dit in de PST's aangezien de
koning en de toren goede scores krijgen op de posities waar ze belanden
na het rokeren, maar dit zorgt er vaker voor dat de AI de koning
handmatig naar de hoek zal bewegen dan rokeren, dus werd er een aparte
feature gemaakt die het rokeren beloond.

De implementatie verliep als volgt:

-   Kijk na of rokeren met 1 van de torens mogelijk is in de huidige
    positie. Dit is een voorwaardelijk statement dat ten eerste
    rokeer-rechten (rokeren mag niet altijd) en ten tweede de positie
    van de torens in rekening brengt.

-   Geef een beloning van 90 als de voorwaarden voldaan zijn. Deze
    waarde wordt gekozen omdat er een grote nadruk moet zijn op het
    belang van rokeren, terwijl het niet gewenst is dat een pion
    evenwaardig is als de actie van het rokeren.

-   Geef geen beloning, maar ook geen straf (beloning 0) indien de
    voorwaarden niet voldaan zijn. Op het eerste zicht zou men denken
    dat een straf hier van toepassing zou zijn, maar dit zou resulteren
    in een straf zodra het rokeren voltooid wordt. Doordat rokeren niet
    meer kan nadat het is uitgevoerd, zou de AI nu bij elke volgende zet
    een straf krijgen. Het is eerder gewenst dat rokeren wordt
    nagestreefd en zodra het is uitgevoerd dat men verdergaat zoals
    gewoonlijk en de volledige Castle Score method overslaat.

## Check score

Door de tegenstander schaak te zetten dwing je hem/haar hierop te
reageren en zet je druk op de structuur rond de koning. Een schaker moet
dus proberen op zoek te gaan naar kansen om de tegenstander schaak te
zetten, en in de meeste gevallen is het ook goed om die kansen te
benutten. Er werd daarom een feature ingebouwd die de AI aanzet om de
tegenstander schaak te zetten.

De implementatie is als volgt:

-   Kijk na of de koning van de speler die aan de beurt is schaak wordt
    gezet.

-   Geef een straf van -90 indien de koning schaak wordt gezet.

-   Doe niets als de koning niet schaak wordt gezet.

-   Aan de hand hiervan zal de AI zoeken naar de positie waarin de
    tegenstander schaak gezet wordt. De positie waarin hijzelf schaak
    wordt gezet zal worden vermeden. Net zoals bij Castle Score wordt
    een waarde van 90 gekozen met dezelfde redenering.

## Kans op materiële verliezen

Een situatie die geregeld voorkomt is dat een stuk zowel aangevallen als
gedekt staat, en hier is het natuurlijk belangrijk dat het aantal
dekkende stukken groter is dan het aantal aanvallers. De *materialscore*
functie die daarnet besproken werd zal tot op zekere hoogte hiervoor
zorgen, maar om het programma snel genoeg te houden kijken we meestal
maar 3-4 zetten in de toekomst, waardoor bepaalde scenario's niet
volledig uitgerekend zullen kunnen worden. Er werd daarom een feature
ingevoerd die specifiek berekent of een stuk nog genoeg gedekt staat.

De implementatie is vrij straight-forward, met een paar subtiliteiten.

-   Minder dekkers dan aanvallers: in dit geval zou de verdediger, in
    het geval dat hij de zet toch speelt, alle dekkers en het stuk dat
    gespeeld wordt verliezen. We gaan er vanuit dat de aanvaller eerst
    met al zijn slechtste stukken zal pakken. Hij verliest dus zijn
    slechtste stukken, en evenveel als dat er dekkers zijn. Verder moet
    er nog een uitzondering gemaakt worden indien er bij de dekkers een
    koning zit: deze zal niet meer kunnen meedoen want je mag jezelf
    natuurlijk niet schaak zetten. De benodigde waarden worden berekend,
    en het netto verlies wordt gegeven. Het verlies kan nog steeds
    negatief zijn (i.e. de verdediger kan winst maken) als de dekkers
    bijvoorbeeld twee pionnen en een paard zijn terwijl de aanvallers 4
    dames zijn.

-   Evenveel dekkers als aanvallers: eerst wordt er gecontroleerd of er
    een koning bij de aanvallers zit, want alle aanvallers zullen in het
    potentieel duel sneuvelen. Bij de dekkers mag er een koning zitten,
    deze zal dan als laatste nemen. De netto loss wordt berekend door er
    van uit te gaan dat de aanvaller alle aanvallers verliest, en de
    verdediger verliest alle dekkers behalve de meest waardevolle
    (waarmee hij als laatste neemt) en het stuk dat hij heeft gezet.

-   Meer dekkers dan aanvallers: hier wordt dezelfde redenering
    toegepast als in de eerste situatie, met dan de rol van de aanvaller
    en verdediger omgewisseld.

## Board value

De *Boardvalue* functie berekent alle features die net besproken werden
voor een bepaalde zet, en levert de totale waarde. Deze zal opgeroepen
worden door de chess agent (zie sectie 3).

## Transposition table class

Omdat de waardeberekening van een bord niet triviaal is, zoals blijkt
uit alle net besproken features, is het nuttig om over een
transpositietabel te beschikken. Deze tabel registreert elk bord dat
tegengekomen wordt bij het verkennen en zijn waarde. Wanneer dat zelfde
bord door een andere zettencombinatie later nog eens terugkomt, kan men
gewoon de waarde van dit bord uit de tabel halen. De implementatie is
zeer basic en zal hier niet verder besproken worden. Om de borden te
identificeren gebruikt men de python-chess *board.epd()* functie die een
bord omzet naar een string.

# De uitvoering

De code achter de zaken die in deze sectie besproken worden wordt
gevonden in chessagent.py.

De chess agent zal tijdens het spelen telkens enkele zetten vooruit
kijken en de board value berekenen voor alle legale zetten op dat
moment. Uiteindelijk zal hij de zet spelen met de grootste waarde. Deze
waarde wordt bepaald aan de hand van het minimax algoritme met
alpha-beta pruning.

## Grandmaster moves

Aan chess-AI's wordt vaak een lijst met 'grandmaster moves' meegegeven,
dat zijn zetten die, volgens verschillende grootmeesters, in een
bepaalde situatie altijd het best zijn. Deze zetten zijn meestal aan het
begin van het spel. Hier werden deze zetten beperkt tot de allereerste
zet van het spel; er zal altijd geopend worden met e4 of e5, afhankelijk
van de positie waarin gestart wordt.

## Alpha-beta pruning

De abpruning method is de implementatie van het minimax algoritme met
alpha-beta pruning. Het neemt een schaakbord, twee floats die de alpha
en beta waarden voorstellen, een integer die de search depth voorstelt,
een boolean die aangeeft of de search maximaliserend of minimaliserend
is, en een transposition table. Het alpha-beta pruning-algoritme wordt
gebruikt om de efficiëntie van de minimax search te verbeteren door
takken van de search tree af te snijden die de uiteindelijke beslissing
niet kunnen beïnvloeden.

De implementatie gebeurt als volgt:

-   De methode abpruning controleert eerst of de waarde van het bord al
    is opgeslagen in de transpositietabel. Zo ja, dan wordt de
    opgeslagen waarde gegeven om herberekening te voorkomen.

-   Indien de search depth gelijk is aan 0 of de verstreken tijd sinds
    het begin van de zoekopdracht de tijdslimiet heeft overschreden,
    geeft de method de waarde van het bord terug aan de hand van de
    boardvalue method (uit chessutility.py).

-   Als de search een maximaliserende search is, worden de legale zetten
    doorlopen en wordt de waarde van elke zet berekend door de abpruning
    method recursief op te roepen tot de reeds vermelde eindvoorwaarden
    bereikt worden. Het slaat de maximale waarde op en werkt de waarde
    van alpha bij. Als de betawaarde kleiner of gelijk is aan de
    alphawaarde, wordt de search afgebroken.

-   Als de zoekopdracht een minimaliserende zoekopdracht is, wordt
    hetzelfde gedaan, maar dan met de minimumwaarde en de betawaarde.

# Niet-uitgevoerde ideeën

Het verzinnen van goede features was geen makkelijke taak. Het had mooi
geweest om een neuraal netwerk te bouwen dat geregistreerde
schaakspellen als input neemt en daaruit bepaalde features afleidt. Er
zijn namelijk ongetwijfeld goede features waar je door pure redenering
onmogelijk op kan komen. Je hebt dan meer aan een computer die patronen
ziet waar een mens dat soms niet doet.

Ook de grandmaster moves hadden uitgebreider gekund, maar er was geen
tijd om dit verder te implementeren. Dit had gekund door bijvoorbeeld
bepaalde borden op te lijsten en direct te linken aan een zet.

Ten slotte was het nog mogelijk geweest om het search algoritme te
verbeteren door dieper te zoeken in branches met een hoger potentieel
risico (quiescent search).
