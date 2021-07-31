# Cricket: Player consistency vs strike rate

This project is used to investigate whether in criket whether fast scoring players are less consistent. I followed [this](https://www.espncricinfo.com/story/a-consistency-index-for-batsmen-614199) article for my definition of consistency. This project will use data from everybatsman whom scored more than 3000 runs, debuted after 1970 and had an averge over 25. It will plot these batsman strike rate against there consistency index.

You can find the dataset and jpg of the plot inside the output directory

## Setup

run the following to install the required packages

```
pip install
```

## Fetch Player data

run the following if you wish to refetch the player data

```
python3 getPlayerData.py
```

## Create plot

run the following if you wish to create the plot

```
python3 createPlot.py
```




