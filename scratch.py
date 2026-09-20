from knot.seeds import trefoil, figure_eight
from dataset.negative import generate_negative_pair
from visualization.plot import plot_knot

result = generate_negative_pair(trefoil(), figure_eight(), num_moves=15, trials=10, seed=1)

print("Crossing count diff:", result['diff'])
print("Moves applied to A:", [str(m) for m in result['moves_a']])
print("Moves applied to B:", [str(m) for m in result['moves_b']])

plot_knot(result['knot_a_end'], title="Knot A (started trefoil)", save_path="neg_a.png")
plot_knot(result['knot_b_end'], title="Knot B (started figure-eight)", save_path="neg_b.png")