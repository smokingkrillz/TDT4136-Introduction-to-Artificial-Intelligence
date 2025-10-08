from typing import Any
from queue import Queue
import timeit

class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        """Constructs a CSP instance with the given variables, domains and edges.

        Parameters
        ----------
        variables : list[str]
            The variables for the CSP
        domains : dict[str, set]
            The domains of the variables
        edges : list[tuple[str, str]]
            Pairs of variables that must not be assigned the same value
        """
        self.variables = variables
        self.domains = domains

        self.binary_constraints: dict[tuple[str, str], set] = {}
        for variable1, variable2 in edges:
            self.binary_constraints[(variable1, variable2)] = set()
            self.binary_constraints[(variable2, variable1)] = set()

            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add(
                            (value1, value2)
                        )
                        self.binary_constraints[(variable2, variable1)].add(
                            (value2, value1)
                        )
        self.neighbors = {var: set() for var in variables}
        # make a neighbor , type is dict of set
        for a, b in edges:
            self.neighbors[a].add(b)
            self.neighbors[b].add(a)

    def ac_3(self) -> bool:
        """Performs AC-3 on the CSP.
        Meant to be run prior to calling backtracking_search() to reduce the search for some problems.

        Returns
        -------
        bool
            False if a domain becomes empty, otherwise True
        """

        def revise(xi: str, xj: str) -> bool:
            """Revises the domain of xi to satisfy the constraint between xi and xj.
            Parameters
            ----------
            xi : str
                A variable
            xj : str
                A variable that is a neighbor of xi
            Returns
            -------
            bool
                True if the domain of xi was revised, otherwise False
            """

            revised = False
            # allowed pairs for the constraint between xi and xj, it is type of set of tuple
            allowed = self.binary_constraints.get((xi, xj), set())
            # pairs that need to be removed from the domain of xi
            to_remove = set()
            for x in self.domains[xi]:
                
                if all((x, y) not in allowed for y in self.domains[xj]):
                    to_remove.add(x)
            if to_remove:
                self.domains[xi] -= to_remove
                revised = True
            return revised

        queue_ac3 = Queue()
        for xi, xj in self.binary_constraints:
            # add all arcs to the queue
            queue_ac3.put((xi, xj))
        while queue_ac3.empty() is False:
            # we remove an arc from the queue, FIFO
            (xi, xj) = queue_ac3.get()
            # if the domain of xi is revised or not
            if revise(xi, xj) is True:
                if len(self.domains[xi]) == 0:
                    return False
                for neighbor in self.neighbors[xi]:
                    if neighbor != xj:
                        queue_ac3.put((neighbor, xi))
        return True

    def backtracking_search(self) -> None | dict[str, Any]:
        """Performs backtracking search on the CSP.

        Returns
        -------
        None | dict[str, Any]
            A solution if any exists, otherwise None
        """

        def satisfy_constraint(variable, value, assignment):
            """Checks if the assignment of a value to a variable satisfies all constraints.

            Args:
                variable (str): The variable being assigned.
                value (Any): The value being assigned to the variable.
                assignment (dict[str, Any]): The current assignment of values to variables.

            Returns:
                bool: True if the assignment is consistent with all constraints, False otherwise.
            """
            # check only neighbour constraints
            for neighbour in self.neighbors[variable]:
                if neighbour not in assignment:
                    continue
                
                # Get the allowed pairs for this constraint
                allowed = self.binary_constraints.get((variable, neighbour), set())
                pair = (value, assignment[neighbour])
                
                # Check if this pair is allowed by the constraint
                if pair not in allowed:
                    return False

            return True

        def order_domain_values(var: str) -> list[Any]:
            """Returns the domain values of a variable.
            Parameters
            ----------
            var : str
                A variable
                Returns
                -------
                list[Any]
                    The domain values of the variable
            """
            return sorted(self.domains[var])

        def select_unassigned_variable(assignment: dict[str, Any]) -> str | None:
            """Selects an unassigned variable from the CSP.

            Args:
                assignment (dict[str, Any]): The current assignment of values to variables.

            Returns:
                str | None: The first unassigned variable found, or None if all variables are assigned.
            """
            # Any unassigned variable
            for v in self.variables:
                if v not in assignment:
                    return v
            return None
        self.backtrack_calls = 0
        self.backtrack_failures = 0
        
        def backtrack(assignment: dict[str, Any]):
            """Performs backtracking search to find a solution to the CSP.
            Parameters
            ----------
            assignment : dict[str, Any]
                The current assignment of values to variables
            Returns
            -------
            None | dict[str, Any]
                A solution if any exists, otherwise None
            """
            self.backtrack_calls += 1
            if len(assignment) == len(self.variables):
                return assignment

            unassigned_variable = select_unassigned_variable(assignment)
            # check domain and if it satisfies constraint
            for state in order_domain_values(unassigned_variable):
                if satisfy_constraint(unassigned_variable, state, assignment):
                    assignment[unassigned_variable] = state
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                    del assignment[unassigned_variable]
            self.backtrack_failures += 1
            return None

        return backtrack({})


def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    """Returns a list of edges interconnecting all of the input variables

    Parameters
    ----------
    variables : list[str]
        The variables that all must be different

    Returns
    -------
    list[tuple[str, str]]
        List of edges in the form (a, b)
    """
    return [
        (variables[i], variables[j])
        for i in range(len(variables) - 1)
        for j in range(i + 1, len(variables))
    ]
