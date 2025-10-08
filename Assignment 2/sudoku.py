# Sudoku problems.
# The CSP.ac_3() and CSP.backtrack() methods need to be implemented

from csp import CSP, alldiff
import time

def print_solution(solution):
    """
    Convert the representation of a Sudoku solution, as returned from
    the method CSP.backtracking_search(), into a Sudoku board.
    """
    for row in range(width):
        for col in range(width):
            print(solution[f'X{row+1}{col+1}'], end=" ")
            if col == 2 or col == 5:
                print('|', end=" ")
        print("")
        if row == 2 or row == 5:
            print('------+-------+------')

def domain_summary(domains):
    """Returns a summary of the domains.
    Parameters
    ----------
    domains : dict[str, set[Any]]
        The domains of the variables
    Returns
    -------
    dict[str, float | int]
        A summary of the domains with keys:
        - min: The size of the smallest domain
        - max: The size of the largest domain
        - avg: The average size of the domains
        - singles: The number of domains with a single value
        - total: The total size of all domains
    """
        sizes = [len(domains[v]) for v in sorted(domains)]
        return {
            "min": min(sizes),
            "max": max(sizes),
            "avg": sum(sizes)/len(sizes),
            "singles": sum(1 for s in sizes if s == 1),
            "total": sum(sizes)
        }
sudoku_files = ["sudoku_easy.txt", "sudoku_medium.txt", "sudoku_hard.txt","sudoku_very_hard.txt"]

for sudoku_file in sudoku_files:
    grid = open(sudoku_file).read().split()

    width = 9
    box_width = 3

    domains = {}
    for row in range(width):
        for col in range(width):
            if grid[row][col] == '0':
                domains[f'X{row+1}{col+1}'] = set(range(1, 10))
            else:
                domains[f'X{row+1}{col+1}'] = {int(grid[row][col])}

    edges = []
    for row in range(width):
        edges += alldiff([f'X{row+1}{col+1}' for col in range(width)])
    for col in range(width):
        edges += alldiff([f'X{row+1}{col+1}' for row in range(width)])
    for box_row in range(box_width):
        for box_col in range(box_width):
            cells = []
            edges += alldiff(
                [
                    f'X{row+1}{col+1}' for row in range(box_row * box_width, (box_row + 1) * box_width)
                    for col in range(box_col * box_width, (box_col + 1) * box_width)
                ]
            )

    csp = CSP(
        variables=[f'X{row+1}{col+1}' for row in range(width) for col in range(width)],
        domains=domains,
        edges=edges,
    )

    print(f"Solving {sudoku_file}:")
    t0 = time.perf_counter()
    csp.ac_3()
    t1 = time.perf_counter()
    print("AC3 time:", round(t1 - t0, 5))
    print(domain_summary(csp.domains))
    t2 = time.perf_counter()
    solution = csp.backtracking_search()
    t3 = time.perf_counter()
    print_solution(solution)
    print("Backtrack time:", round(t3 - t2, 5))
    print("total time:", round((t1 - t0) + (t3 - t2), 5))
    print("Backtrack calls:", csp.backtrack_calls)
    print("Backtrack failures:", csp.backtrack_failures)
# Expected output after implementing csp.ac_3() and csp.backtracking_search():
# True
# 7 8 4 | 9 3 2 | 1 5 6
# 6 1 9 | 4 8 5 | 3 2 7
# 2 3 5 | 1 7 6 | 4 8 9
# ------+-------+------
# 5 7 8 | 2 6 1 | 9 3 4
# 3 4 1 | 8 9 7 | 5 6 2
# 9 2 6 | 5 4 3 | 8 7 1
# ------+-------+------
# 4 5 3 | 7 2 9 | 6 1 8
# 8 6 2 | 3 1 4 | 7 9 5
# 1 9 7 | 6 5 8 | 2 4 3
