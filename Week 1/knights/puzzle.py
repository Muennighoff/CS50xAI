from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    # Each character is one or the other  -  exclusive or
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), 
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    # Knights always tell the truth, Knaves always lie
    # You can always transform Implication to Or structure via Implication Elimination

    #   Implication(And(AKnight, AKnave), AKnight),
    #   Implication(Not(And(AKnight, AKnave)), AKnave),

    Or(Not(And(AKnight, AKnave)), AKnight),
    Or(And(AKnight, AKnave), AKnave)

    # Explanation:
    # A cannot be both, hence he must be lying and be a knave

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO

    # Each character is one or the other  -  exclusive or
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), 
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    # If A tells the truth that both are knaves, A is a knight
    Implication(Biconditional(AKnave, BKnave), AKnight),

    # If A lies that both are knaves, then A must be a Knave
    Implication(Not(And(AKnave, BKnave)), AKnave)

    # Explanation:
    # If A were a knight, he wouldn't say We are both Knaves, cuz it would be wrong, so he must be a knave
    # But if he's a knave then he must be lying so B must be a knight!

)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    # Each character is one or the other  -  exclusive or
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), 
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
    
    # Translating information from A: 
    Implication(AKnight, BKnight),
    Implication(AKnave, BKnight),

    # Translating information from B
    Implication(BKnight, AKnave),
    Implication(BKnave, AKnave)

    # Explanation
    # A cannot be a knight since B would then be lying, hence A has to be a knave and B a knight
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

knowledge3 = And(
    # TODO
     # Each character is one or the other  -  exclusive or
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), 
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    # Translating information from A - Knowledge Engineering
    Implication(AKnight, AKnight),
    Implication(AKnave, AKnight),

    # Translating information from B
    # First Statement - Implication in both directions
    Biconditional(BKnight, AKnave),
    Biconditional(BKnave, AKnight),

    # Second Statement
    Implication(BKnight, CKnave),
    Implication(BKnave, CKnight),

    # Translating information from C
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave)

    # Explanation
    # By the games rules it is not possible to say "I am a knave", so A must be a knight, hence B must be a knave and C a knight

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
