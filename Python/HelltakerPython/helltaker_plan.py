import sys
from helltaker_utils import grid_from_file, check_plan


def monsuperplanificateur(infos):
    print(infos)
    h, l, = infos["m"], infos["n"]
    max_steps = infos["max_steps"]
    grid = infos["grid"]
    me = get_position(grid, "H")[0]
    goal = get_position(grid, "D")[0]
    actions = []
    print(me, goal)
    s0 = (me, actions)
    return "hbgd"


def get_position(grid, indicator):
    pos = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == indicator:
                pos.append((i, j))
    return pos


def main():
    # récupération du nom du fichier depuis la ligne de commande
    filename = "tests/level1.txt"

    # récupération de al grille et de toutes les infos
    infos = grid_from_file(filename)

    # calcul du plan
    plan = monsuperplanificateur(infos)

    # affichage du résultat
    if check_plan(plan):
        print("[OK]", plan)
    else:
        print("[Err]", plan, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
