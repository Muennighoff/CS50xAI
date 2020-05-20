import sys

from crossword import *




class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

        # Sorting Algorithm for select_unassigned_variable:
        # Sort first by secondary key -- Degree Heuristics
        self.arc_dict = {k[0]: k[1] for k, v in self.crossword.overlaps.items() if v is not None}
        self.arc_list = []
        for k, v in self.arc_dict.items():
            self.arc_list.append(k)
            self.arc_list.append(v)
        self.dh_list = sorted(self.arc_list, key=self.arc_list.count, reverse=True)

        # Sort then by primary key -- Minimum Remaining Values
        self.mrv_dh_list = sorted(self.dh_list, key=lambda d_key: len(self.domains[d_key]))

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        # print("BEFORE ENC: ", self.domains) - Works fine
        self.enforce_node_consistency()
        # print("BEFORE AC3: ", self.domains) - Works fine
        self.ac3()
        # print("BEFORE BT: ", self.domains)
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Iterate through all variables & their respective domains
        for key, values in self.domains.items():
            # Iterate through the domains and delete (Taking a copy here to avoid set changed during iteration error)
            for value in values.copy():
                if key.length != len(value):
                    self.domains[key].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False

        # Can only overlap once! -- one index for each
        indices = self.crossword.overlaps[x,y]

       # print("INDICES: ", indices, x, y)

        for domain_x in self.domains[x].copy():
            found_fit = False

            for domain_y in self.domains[y]:
                # If we found a fit the domain is arc consistent & we can move on


                if domain_x[indices[0]] == domain_y[indices[1]]:
                    found_fit = True
                    break

            if found_fit == True:
                continue
            else:
                # domain_x is not arc consistent
                self.domains[x].remove(domain_x)
                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if arcs is None:
            # Initialize arcs to all overlaps - We need to sort out the Variables where overlap is None
            arc_dict = {k: v for k, v in self.crossword.overlaps.items() if v is not None}
            queue = list(arc_dict)

            # print("QUEUE:", queue)

        else:
            queue = arcs

        while len(queue) != 0:
            # Pop an item from queue
            arc_pair = queue.pop(0)

            X = arc_pair[0]
            Y = arc_pair[1]

            if self.revise(X, Y):

                # If problem cannot be solved:
                if len(self.domains[X]) == 0:
                    return False

                # We must add(/re-add) new pairs since our available values for var x have changed
                for neighbor in self.crossword.neighbors(X):
                    queue.append((X, neighbor))

        return True



    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        for key in assignment:
            if len(assignment[key]) > 1:
                return False

        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # a All values are distinct (binary constraint)
        # b All values have correct length (unary constraint)
        # c All values have no conflicts with neighbors (binary constraint)

        unique_list = []

        arc_dict = {k: v for k, v in self.crossword.overlaps.items() if v is not None}

        # b:
        for key, value in assignment.items():

            if key.length != len(value):
                print("RETURNING FALSE AS: ", key.length, len(value))
                return False

            # Create list of values to ensure unique
            unique_list.append(value)

        # c:
        for key in arc_dict:
            # Check if the arc keys are in the assignment
            if key[0] in assignment and key[1] in assignment:
                # Check if the chars of each var's value are equal
                if assignment[key[0]][arc_dict[key][0]] != assignment[key[1]][arc_dict[key][1]]:
                    # print("RETURNING FALSE AS: ", key[0], key[1])
                    return False
        # a:
        if len(unique_list) != len(set(unique_list)):
            return False


        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Get all overlaps
        arc_dict = {k: v for k, v in self.crossword.overlaps.items() if v is not None and (k[0] == var or k[1] == var)}
        # Dict with value as key and the number of values the key rules out for neighbors
        dict_v = {}
        # Iterate through all values in var's domain
        for value in self.domains[var]:

            dict_v[value] = 0

            # Iterate through neighbors and count how many values it will rule out for the neighbors
            for neighbor in self.crossword.neighbors(var):

                if arc_dict[var, neighbor] is not None:
                    constraint = arc_dict[var, neighbor]
                elif arc_dict[neighbor, var] is not None:
                    constraint = arc_dict[neighbor, var]
                    # Reverse tuple
                    tmp = constraint[0]
                    constraint[0] = constraint[1]
                    constraint[1] = tmp
                else:
                    print("ERRORRRR")

                # Iterate through value in the neighbor keep cout of how many it rules out
                for value_n in self.domains[neighbor]:

                    # If it rules out a neighbor's value we increase its count
                    if value[constraint[0]] != value_n[constraint[1]]:
                        dict_v[value] += 1


        list_v = sorted(dict_v, key=lambda key: dict_v[key])

        return list_v


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # I moved the sorting algorithm to the global variables of the class to improve performance

        # Sort first by secondary key -- Degree Heuristics
        # arc_dict = {k[0]: k[1] for k, v in self.crossword.overlaps.items() if v is not None}
        # arc_list = []
        # for k, v in arc_dict.items():
            # arc_list.append(k)
            # arc_list.append(v)
        # dh_list = sorted(arc_list, key=arc_list.count, reverse=True)
        # Sort then by primary key -- Minimum Remaining Values
        # mrv_dh_list = sorted(dh_list, key=lambda d_key: len(self.domains[d_key]))


        # Turn into a set and check if not yet assigned
        for i in set(self.mrv_dh_list):
            if i not in assignment:
                return i

        return None






    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment complete - Fine
        if len(assignment) == len(self.domains):
            return assignment

        # Start with a variable
        var = self.select_unassigned_variable(assignment)

        # Get domain of the variable
        for value in self.order_domain_values(var, assignment):

            # Assign & check if consistent with assignment
            assignment[var] = value
            if self.consistent(assignment):

                assignment[var] = value

                # Here we could modify ac3 to only go through the queue of neighboring var's to save time
                # No need to call normal ac3, since already called in solve()
                # self.ac3()

                # Going with that value:
                result = self.backtrack(assignment)

                if result is not None:
                    return result

            # If variable is not consistent or does not lead to a result --
            # We delete not remove, since we don't have a list but just a key, value pair
            del assignment[var]

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
