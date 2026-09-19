from knot.seeds import trefoil, figure_eight, cinquefoil
from visualization.plot import plot_knot

plot_knot(trefoil(), title="Trefoil (3_1)", save_path="trefoil.png")
plot_knot(figure_eight(), title="Figure-eight (4_1)", save_path="figure_eight.png")
plot_knot(cinquefoil(), title="Cinquefoil (5_1)", save_path="cinquefoil.png")