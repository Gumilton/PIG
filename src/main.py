from game import run
from player import PlayerRandom

if __name__ == "__main__":
    run([PlayerRandom(), PlayerRandom(), PlayerRandom(), PlayerRandom()], 10, verbose=True)