import server_trainer
import intelligence
import random
import matplotlib.pyplot as plt
from tqdm import tqdm

X = 0.26
Y = 0.6
host, port = ('localhost', 5566) # le 5566 a été paramétré par port forward sur ma machine pour être ouvert au réseau extérieur (pour le faire fonctionner chez vous il faut ouvrir le port 5566 sur les paramètres du routeur) 
BLINDE = 2 # la petite blinde pour la partie
MONEY = 100 # la monnaie de départ des joueurs
NB_CLIENTS = 0 # le nombre de clients (joueurs humains)
NB_IAS = 6 # le nombre d'IA
server = server_trainer.Server((host, port),  NB_IAS)
server.conns = [None] * NB_IAS
NB_GAMES = 1000
DEPTH = 100
HANDS_PER_LEVEL = 100
victory = [0] * NB_IAS
ids = [0] * NB_IAS

plt.bar(range(NB_IAS), victory, tick_label = ["naive", "RC", "PR", "CL", "ERC", "CBPR"])
plt.ion()
plt.show()
for i in tqdm(range(NB_GAMES)):
    server.conns[0] = server_trainer.AIThread(server, "naive")
    server.conns[1] = server_trainer.AIThread(server, "RC", depth = DEPTH, hands_tested = HANDS_PER_LEVEL, min_lim_couche = 0.15, max_lim_couche = 0.35, min_lim_relance = 0.6, max_lim_relance = 0.8)
    server.conns[2] = server_trainer.AIThread(server, "PR", depth = DEPTH, hands_tested = HANDS_PER_LEVEL, min_lim_couche = 0.8, max_lim_couche = 1, min_lim_relance = 1.3, max_lim_relance = 1.5)
    server.conns[3] = server_trainer.AIThread(server, "CL")
    #server.conns[4] = server_trainer.AIThread(server, "GB")
    server.conns[4] = server_trainer.AIThread(server, "ERC", depth = DEPTH, hands_tested = HANDS_PER_LEVEL)
    server.conns[5] = server_trainer.AIThread(server, "CBPR", depth = DEPTH, hands_tested = HANDS_PER_LEVEL, lim1 = 0.8, lim2 = 1, lim3 = 1.3)
    for i in range(NB_IAS): ids[i] = server.conns[i].id
    coup, exec, winner = server.run(BLINDE, MONEY)
    victory[ids.index(winner)] += 1
    #print(f"Naif: {victory[0]} - RC: {victory[1]} - ERC: {victory[2]} - CL: {victory[3]} - GB: {victory[4]}", end = "\r")
    plt.clf()
    plt.bar(range(NB_IAS), victory, tick_label = ["NAIF", "RC", "PR", "CL", "ERC", "CBPR"])
    plt.pause(0.2)
    plt.ion()
    plt.show()
print(f"Naif: {victory[0]} - RC: {victory[1]} - PR: {victory[2]} - CL: {victory[3]} - ERC: {victory[4]} - CBPR: {victory[5]}")
plt.clf()
plt.bar(range(NB_IAS), victory, tick_label = ["naive", "RC", "PR", "CL", "ERC", "CBPR"])
plt.pause(0.2)
plt.show()
input()