import itertools
import math

def get_adj_count(board, r, c):
    return sum(1 for br, bc in board if max(abs(br - r), abs(bc - c)) <= 1 and (br, bc) != (r, c))

grid_coords = [(r, c) for r in range(5) for c in range(5)]
all_boards = list(itertools.combinations(grid_coords, 4))

# Scenario: (2,2) is a T
valid_boards = [b for b in all_boards if (2,2) in b]

print(f"Total valid boards: {len(valid_boards)}")

results = []
for r in range(5):
    for c in range(5):
        if (r, c) == (2,2): continue
        freqs = {'T': 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        for b in valid_boards:
            if (r, c) in b:
                freqs['T'] += 1
            else:
                freqs[get_adj_count(b, r, c)] += 1
        
        entropy = 0
        N = len(valid_boards)
        for v, count in freqs.items():
            if count > 0:
                p = count / N
                entropy -= p * math.log2(p)
                
        pT = freqs['T'] / N
        exp_pts = (freqs['T'] * 100 + sum(v * freqs[v] for v in range(5) if v != 'T')) / N
        
        results.append(((r+1, c+1), pT, exp_pts, entropy))

print("\n--- Sorted by Expected Points ---")
for res in sorted(results, key=lambda x: x[2], reverse=True)[:5]:
    print(f"Tile {res[0]}: P(T)={res[1]*100:.1f}%, ExpPts={res[2]:.2f}, Entropy={res[3]:.3f}")

print("\n--- Sorted by Entropy (Information Gain) ---")
for res in sorted(results, key=lambda x: x[3], reverse=True)[:5]:
    print(f"Tile {res[0]}: P(T)={res[1]*100:.1f}%, ExpPts={res[2]:.2f}, Entropy={res[3]:.3f}")
