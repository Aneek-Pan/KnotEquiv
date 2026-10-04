import snappy
from knot.structure import Knot
from knot.canonical import knots_equal
from knot.seeds import SEEDS

new_knots = {
    '5_2': Knot.from_tokens([(1,'U','+'),(2,'O','+'),(5,'U','+'),(4,'O','+'),(3,'U','+'),(1,'O','+'),(2,'U','+'),(3,'O','+'),(4,'U','+'),(5,'O','+')]),
    '6_1': Knot.from_tokens([(1,'U','-'),(6,'O','+'),(5,'U','+'),(4,'O','+'),(3,'U','+'),(1,'O','-'),(2,'U','-'),(3,'O','+'),(4,'U','+'),(5,'O','+'),(6,'U','+'),(2,'O','-')]),
    '6_2': Knot.from_tokens([(1,'U','+'),(2,'O','+'),(3,'U','+'),(4,'O','+'),(5,'U','-'),(6,'O','-'),(4,'U','+'),(1,'O','+'),(2,'U','+'),(3,'O','+'),(6,'U','-'),(5,'O','-')]),
    '6_3': Knot.from_tokens([(1,'U','-'),(5,'O','-'),(6,'U','-'),(1,'O','-'),(2,'U','+'),(3,'O','+'),(4,'U','+'),(2,'O','+'),(5,'U','-'),(6,'O','-'),(3,'U','+'),(4,'O','+')]),
}

all_known = dict(SEEDS)
print("Checking new knots against each other and existing seeds...\n")
names = list(new_knots.keys())
for i in range(len(names)):
    for j in range(i+1, len(names)):
        eq = knots_equal(new_knots[names[i]], new_knots[names[j]])
        print(f"{names[i]} == {names[j]}: {eq}")

for new_name, new_k in new_knots.items():
    for seed_name, seed_fn in all_known.items():
        eq = knots_equal(new_k, seed_fn())
        if eq:
            print(f"WARNING: {new_name} == existing seed {seed_name}!")
print("\nDone. Any unflagged pair is confirmed distinct.")