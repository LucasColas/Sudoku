import numpy as np
import subprocess

from typing import List, Tuple

Grid1 = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
])


Grid2 = np.array([
    [0, 0, 0, 0, 2, 7, 5, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 4, 6],
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 2, 0],
    [0, 0, 0, 8, 1, 0, 0, 0, 0],
    [4, 0, 6, 3, 0, 1, 0, 0, 9],
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 2, 0, 0, 0, 0, 3, 1, 0],
])


Empty_Grid = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
])

def cell_to_variable(i, j, val):
    return 81 * i + 9 * j + val + 1


def variable_to_cell(var: int):
    k = (var - 1) % 9
    j = ((var - k) // 9) % 9
    i = (var - k - 9 * j) // 81
    return np.array([i,j,k])


def create_clauses(Grid):
    Clauses = []
    rows, cols = 9,9
    n = 9
    #Every cell contains at least one number
    for i in range(rows):
        for j in range(cols):
            Clauses.append(np.array([cell_to_variable(i, j, val) for val in range(n)]))

    #Every cell contains at most one number
    for i in range(rows):
        for j in range(cols):

            for x in range(n):
                for y in range(n):
                    if x != y:
                        Clauses.append(np.array([-cell_to_variable(i, j, x), -cell_to_variable(i, j, y)]))


    #Every row contains every number
    for i in range(rows):
        for x in range(n):
            Clauses.append(np.array([cell_to_variable(i, j, x) for j in range(cols)]))

    #Every column contains every number
    for j in range(cols):
        for x in range(n):
            Clauses.append(np.array([cell_to_variable(i, j, x) for i in range(cols)]))

    #Every 3x3 box contains every number
    for val in range(n):
        for col in range(0, cols, 3):
            for row in range(0, rows, 3):
                Clause = []
                for i in range(row, row+3):
                    for j in range(col, col+3):
                        Clause.append(cell_to_variable(i, j, val))


    #Numbers in Grid
    for x in range(0, Grid.shape[0]):
        for y in range(0, Grid.shape[1]):
            if Grid[x,y] != 0:

                Clauses.append([cell_to_variable(x,y,Grid[x,y]-1)])


    return Clauses



def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def exec_gophersat(
    filename: str, cmd: str = "gophersat", encoding: str = "utf8"
) -> Tuple[bool, List[int]]:
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:-2].split(" ")

    return True, [int(x) for x in model]

def clauses_to_dimacs(clauses, nb_vars):
    end_of_line = "0\n"
    res = "p cnf " + str(nb_vars) + " " + str(len(clauses)) + "\n"
    for clause in clauses:
        line = ""
        for val in clause:
            line = line + str(val) + " "
        line += end_of_line
        res += line
    return res

def recuperation_grille_resultat(Grid, Result):
    """
    A partir de la chaine resultante comprenant les valeurs des variables, on construit la grille de sudoku solution
    :return: la grille de sudoku solution
    """
    grille_solution = np.ones((9,9))
    for x in range(Grid.shape[0]):
        for y in range(Grid.shape[1]):
            grille_solution[x,y] = Grid[x,y]

    for val in Result:
        if str(val)[0] != "-":
            Var_to_cell = variable_to_cell(val)
            grille_solution[Var_to_cell[0], Var_to_cell[1]] = Var_to_cell[2]+1





    return grille_solution

def main():
    print(Grid1)
    nb_vars = 729
    clauses = create_clauses(Grid1)
    file_name = "sudoku_np.cnf"
    file_name_res = "sudoku.txt"

    #print(clauses)
    dimacs = clauses_to_dimacs(clauses, nb_vars)
    #print(dimacs)
    write_dimacs_file(dimacs, file_name)
    Res = exec_gophersat(file_name)
    #print(len(Res[1]))
    grille_solution = recuperation_grille_resultat(Grid1, Res[1])
    print(grille_solution)

if __name__ == "__main__":
    main()
