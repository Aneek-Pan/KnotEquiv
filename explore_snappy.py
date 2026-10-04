from knot.seeds import figure_eight

def canonical_gauss_form(seq, allow_mirror=False):
    n = len(seq)
    variants = []

    def relabel(s):
        mapping, next_id, out = {}, 1, []
        for label, ou, sign in s:
            if label not in mapping:
                mapping[label] = next_id
                next_id += 1
            out.append((mapping[label], ou, sign))
        return out

    def flip_sign(s):
        return [(l, ou, '+' if sign == '-' else '-') for l, ou, sign in s]

    base_seqs = [seq, seq[::-1]]
    if allow_mirror:
        base_seqs += [flip_sign(s) for s in base_seqs]

    for s in base_seqs:
        for i in range(n):
            rotated = s[i:] + s[:i]
            variants.append(tuple(relabel(rotated)))

    return min(variants)


snappy_fig8 = [(1, 'U', '-'), (2, 'O', '-'), (3, 'U', '+'), (4, 'O', '+'),
               (2, 'U', '-'), (1, 'O', '-'), (4, 'U', '+'), (3, 'O', '+')]
our_fig8 = figure_eight().seq

print("Same, no mirror allowed:", canonical_gauss_form(snappy_fig8) == canonical_gauss_form(our_fig8))
print("Same, mirror allowed:   ", canonical_gauss_form(snappy_fig8, allow_mirror=True) == canonical_gauss_form(our_fig8, allow_mirror=True))