from game import run
from player import PlayerRandom, PlayerHuman

if __name__ == "__main__":
    run([PlayerHuman("XG"), PlayerRandom(), PlayerRandom(), PlayerRandom()], 10, verbose=True)