##ship format

Dictionary

|Key|Values|
|name|string, name of the ship|
|id|int, id of the ship(itˇs position in shiplist)|
|length|int, length of the ship|
|coords|list, [x, y], origin point of ship|
|orientation|tuple, (x, y), vector of ship orientation|

##shiplist format

List

|Position|Ship|
|0|Carrier|
|1|Battleship|
|2|Cruiser|
|3|Submarine|
|4|Destroyer|

##field format

Two dimensional list, first is x, second is y, each spot is dictionary

|Key|Values|
|content|"water" or "ship" string|
|hit|True/False, if the spot has been hit|
|shipID|int, id of the ship occupying the spot|
