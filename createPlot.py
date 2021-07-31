import json
import matplotlib.pyplot as plt
import re

nationColors = {
  'INDIA': '#26c2f4',
  'AUS': '#f6da09',
  'SL': '#0a4a9b',
  'ENG': '#003b7A',
  'WI': '#800000',
  'SA': '#14bc1b',
  'NZ': '#292728',
  'PAK': '#006600',
  'BDESH': '#4db252',
  'ZIM': '#cb5431',
}

def extractColor(playerName):
  nationRe = re.compile("\((.*)\)")
  nationRaw = nationRe.search(playerName).group(1)
  nation = nationRaw.removeprefix('ICC/').removesuffix('/ICC')
  return nationColors[nation];

def update_annot(ind):
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
                           " ".join([names[n] for n in ind["ind"]]))
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

def getPlayerData():
  with open('./outputs/playerData.json') as f:
    playerData = json.load(f)
  return playerData


playerData = getPlayerData()
xAxis = list(map(lambda p: p['sr'], playerData))
yAxis = list(map(lambda p: p['consIndex'], playerData))
names = list(map(lambda p: p['name'], playerData))
c = list(map(extractColor, names))

fig,ax = plt.subplots()
sc = plt.scatter(xAxis, yAxis, marker='o', c=c);
plt.gca().invert_yaxis()

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

fig.canvas.mpl_connect("motion_notify_event", hover)
plt.show()


