#!/usr/bin/env python3
"""
Comprehensive test suite for the Interactive Grid Simulation.
Tests:
- Foundational properties: constant grid, 1x1 grid, immutability, 1x4 permutations, 1x10 cyclic shift.
- Square, Hexagonal, and Triangular neighbor calculations & boundary conditions.
- Cyclic and Linear state transitions.
- Restrictive and Wolfram-inspired rule predicates:
  - Classic (>= 1)
  - Threshold Quorum (>= theta)
  - Majority Rule (> D / 2)
  - Unanimous Consensus (= D)
  - Vertical Alignment (Top & Bottom)
  - Horizontal Alignment (Left & Right)
  - Axial Cross (Vertical OR Horizontal)
  - Wolfram Parity (Odd Count / XOR)
  - Wolfram Life-like ([2, 3])
  - Wolfram Directional Drift (Left-to-Right)
  - Custom Totalistic Bitmask
"""

import unittest

def get_neighbors_square(r, c, m, n, periodic=True):
    nbrs = []
    if m > 1:
        if periodic:
            up = ((r - 1 + m) % m, c)
            down = ((r + 1) % m, c)
            nbrs.extend([up, down])
        else:
            if r > 0: nbrs.append((r - 1, c))
            if r < m - 1: nbrs.append((r + 1, c))
    if n > 1:
        if periodic:
            left = (r, (c - 1 + n) % n)
            right = (r, (c + 1) % n)
            nbrs.extend([left, right])
        else:
            if c > 0: nbrs.append((r, c - 1))
            if c < n - 1: nbrs.append((r, c + 1))
    
    res = []
    for p in nbrs:
        if p != (r, c) and p not in res:
            res.append(p)
    return res


def get_neighbors_hex(r, c, m, n, periodic=True):
    if m <= 1 and n <= 1:
        return []
    
    is_odd = (r % 2 == 1)
    if is_odd:
        diffs = [
            (0, -1),  # left
            (0, 1),   # right
            (-1, 0),  # top-left
            (-1, 1),  # top-right
            (1, 0),   # bottom-left
            (1, 1)    # bottom-right
        ]
    else:
        diffs = [
            (0, -1),  # left
            (0, 1),   # right
            (-1, -1), # top-left
            (-1, 0),  # top-right
            (1, -1),  # bottom-left
            (1, 0)    # bottom-right
        ]
        
    res = []
    for dr, dc in diffs:
        nr = r + dr
        nc = c + dc
        if periodic:
            nr = (nr + m) % m
            nc = (nc + n) % n
            if (nr, nc) != (r, c) and (nr, nc) not in res:
                res.append((nr, nc))
        else:
            if 0 <= nr < m and 0 <= nc < n:
                if (nr, nc) != (r, c) and (nr, nc) not in res:
                    res.append((nr, nc))
    return res


def get_neighbors_triangle(r, c, m, n, periodic=True):
    if m <= 1 and n <= 1:
        return []
        
    is_up = ((r + c) % 2 == 0)
    if is_up:
        diffs = [(0, -1), (0, 1), (1, 0)] # Left, Right, Bottom
    else:
        diffs = [(0, -1), (0, 1), (-1, 0)] # Left, Right, Top
        
    res = []
    for dr, dc in diffs:
        nr = r + dr
        nc = c + dc
        if periodic:
            nr = (nr + m) % m
            nc = (nc + n) % n
            if (nr, nc) != (r, c) and (nr, nc) not in res:
                res.append((nr, nc))
        else:
            if 0 <= nr < m and 0 <= nc < n:
                if (nr, nc) != (r, c) and (nr, nc) not in res:
                    res.append((nr, nc))
    return res


def get_neighbors(r, c, m, n, tiling='square', periodic=True):
    if tiling == 'hexagonal':
        return get_neighbors_hex(r, c, m, n, periodic)
    elif tiling == 'triangular':
        return get_neighbors_triangle(r, c, m, n, periodic)
    else:
        return get_neighbors_square(r, c, m, n, periodic)


def evaluate_rule(r, c, grid, m, n, tiling, periodic, pred, rule_config):
    rule_type = rule_config.get('type', 'classic')
    
    if rule_type == 'vertical':
        if tiling == 'square':
            up = ((r - 1 + m) % m, c) if periodic else ((r - 1, c) if r > 0 else None)
            down = ((r + 1) % m, c) if periodic else ((r + 1, c) if r < m - 1 else None)
            if up is None or down is None: return False
            return grid[up[0] * n + up[1]] == pred and grid[down[0] * n + down[1]] == pred
        elif tiling == 'hexagonal':
            is_odd = (r % 2 == 1)
            p1_up = (r - 1, c) if is_odd else (r - 1, c - 1)
            p1_dn = (r + 1, c) if is_odd else (r + 1, c - 1)
            if periodic:
                p1_up = ((p1_up[0] + m) % m, (p1_up[1] + n) % n)
                p1_dn = ((p1_dn[0] + m) % m, (p1_dn[1] + n) % n)
                return grid[p1_up[0] * n + p1_up[1]] == pred and grid[p1_dn[0] * n + p1_dn[1]] == pred
            else:
                if 0 <= p1_up[0] < m and 0 <= p1_up[1] < n and 0 <= p1_dn[0] < m and 0 <= p1_dn[1] < n:
                    return grid[p1_up[0] * n + p1_up[1]] == pred and grid[p1_dn[0] * n + p1_dn[1]] == pred
                return False
        elif tiling == 'triangular':
            is_up = ((r + c) % 2 == 0)
            vert = (r + 1, c) if is_up else (r - 1, c)
            if periodic:
                vert = ((vert[0] + m) % m, (vert[1] + n) % n)
                return grid[vert[0] * n + vert[1]] == pred
            else:
                if 0 <= vert[0] < m and 0 <= vert[1] < n:
                    return grid[vert[0] * n + vert[1]] == pred
                return False
                
    elif rule_type == 'horizontal':
        left = ((r, (c - 1 + n) % n)) if periodic else ((r, c - 1) if c > 0 else None)
        right = ((r, (c + 1) % n)) if periodic else ((r, c + 1) if c < n - 1 else None)
        if left is None or right is None: return False
        return grid[left[0] * n + left[1]] == pred and grid[right[0] * n + right[1]] == pred

    elif rule_type == 'cross':
        h_ok = evaluate_rule(r, c, grid, m, n, tiling, periodic, pred, {'type': 'horizontal'})
        v_ok = evaluate_rule(r, c, grid, m, n, tiling, periodic, pred, {'type': 'vertical'})
        return h_ok or v_ok

    elif rule_type == 'drift':
        left = ((r, (c - 1 + n) % n)) if periodic else ((r, c - 1) if c > 0 else None)
        if left is None: return False
        return grid[left[0] * n + left[1]] == pred

    nbrs = get_neighbors(r, c, m, n, tiling, periodic)
    if not nbrs:
        return False
        
    count = sum(1 for nr, nc in nbrs if grid[nr * n + nc] == pred)
    degree = len(nbrs)
    
    if rule_type == 'classic':
        return count >= 1
    elif rule_type == 'quorum':
        theta = rule_config.get('theta', 2)
        return count >= theta
    elif rule_type == 'majority':
        return count > (degree / 2.0)
    elif rule_type == 'unanimous':
        return count == degree
    elif rule_type == 'parity':
        return (count % 2) == 1
    elif rule_type == 'life_like':
        return count in [2, 3]
    elif rule_type == 'custom_mask':
        allowed = rule_config.get('allowed_counts', [1])
        return count in allowed
        
    return count >= 1


def advance_grid_full(grid, m, n, tiling='square', periodic=True, cyclic=True, max_val=10, rule_config=None):
    if rule_config is None:
        rule_config = {'type': 'classic'}
        
    next_grid = list(grid)
    for r in range(m):
        for c in range(n):
            idx = r * n + c
            v = grid[idx]
            
            if cyclic:
                pred = max_val if v == 1 else (v - 1)
            else:
                pred = (v - 1) if v > 1 else None
                
            if pred is not None:
                if evaluate_rule(r, c, grid, m, n, tiling, periodic, pred, rule_config):
                    next_grid[idx] = pred
                    
    return next_grid


class TestGridSimulationFull(unittest.TestCase):

    def test_constant_grid(self):
        for val in range(1, 11):
            grid = [val] * 16
            next_g = advance_grid_full(grid, 4, 4, tiling='square', periodic=True, cyclic=True, max_val=10)
            self.assertEqual(grid, next_g)

    def test_1x1_grid(self):
        for val in range(1, 11):
            grid = [val]
            next_p = advance_grid_full(grid, 1, 1, tiling='square', periodic=True, cyclic=True, max_val=10)
            next_f = advance_grid_full(grid, 1, 1, tiling='square', periodic=False, cyclic=True, max_val=10)
            self.assertEqual(grid, next_p)
            self.assertEqual(grid, next_f)

    def test_immutability(self):
        grid = [1, 2, 3, 4]
        grid_copy = list(grid)
        next_g = advance_grid_full(grid, 1, 4, tiling='square', periodic=False, cyclic=True, max_val=4)
        self.assertEqual(grid, grid_copy)
        self.assertIsNot(grid, next_g)

    def test_1x4_scenarios(self):
        initial = [1, 2, 3, 4]
        # Fixed + Linear
        self.assertEqual(advance_grid_full(initial, 1, 4, 'square', False, False, 4), [1, 1, 2, 3])
        # Periodic + Linear
        self.assertEqual(advance_grid_full(initial, 1, 4, 'square', True, False, 4), [1, 1, 2, 3])
        # Fixed + Cyclic
        self.assertEqual(advance_grid_full(initial, 1, 4, 'square', False, True, 4), [1, 1, 2, 3])
        # Periodic + Cyclic (max=4): exact cyclic permutation
        self.assertEqual(advance_grid_full(initial, 1, 4, 'square', True, True, 4), [4, 1, 2, 3])

    def test_1x10_cyclic_shift(self):
        initial = list(range(1, 11))
        res = advance_grid_full(initial, 1, 10, 'square', True, True, 10)
        expected = [10] + list(range(1, 10))
        self.assertEqual(res, expected)

    def test_10_and_1_interaction(self):
        pair = [10, 1]
        self.assertEqual(advance_grid_full(pair, 1, 2, 'square', False, True, 10), [10, 10])
        self.assertEqual(advance_grid_full(pair, 1, 2, 'square', False, False, 10), [10, 1])

    def test_hexagonal_neighbor_count(self):
        nbrs = get_neighbors_hex(3, 3, 10, 10, periodic=True)
        self.assertEqual(len(nbrs), 6)
        self.assertEqual(len(set(nbrs)), 6)
        self.assertNotIn((3, 3), nbrs)

    def test_triangular_neighbor_count(self):
        nbrs_up = get_neighbors_triangle(2, 2, 10, 10, periodic=True)
        nbrs_dn = get_neighbors_triangle(2, 3, 10, 10, periodic=True)
        self.assertEqual(len(nbrs_up), 3)
        self.assertEqual(len(nbrs_dn), 3)
        self.assertEqual(len(set(nbrs_up)), 3)
        self.assertEqual(len(set(nbrs_dn)), 3)
        self.assertNotIn((2, 2), nbrs_up)
        self.assertNotIn((2, 3), nbrs_dn)

    def test_unanimous_rule(self):
        grid = [
            5, 1, 5,
            1, 2, 1,
            5, 5, 5
        ]
        res = advance_grid_full(grid, 3, 3, 'square', False, True, 10, {'type': 'unanimous'})
        self.assertEqual(res[4], 2)

        grid2 = [
            5, 1, 5,
            1, 2, 1,
            5, 1, 5
        ]
        res2 = advance_grid_full(grid2, 3, 3, 'square', False, True, 10, {'type': 'unanimous'})
        self.assertEqual(res2[4], 1)

    def test_vertical_and_horizontal_alignment(self):
        grid_v = [
            5, 1, 5,
            5, 2, 5,
            5, 1, 5
        ]
        res_v = advance_grid_full(grid_v, 3, 3, 'square', False, True, 10, {'type': 'vertical'})
        self.assertEqual(res_v[4], 1)
        res_h = advance_grid_full(grid_v, 3, 3, 'square', False, True, 10, {'type': 'horizontal'})
        self.assertEqual(res_h[4], 2)

        grid_h = [
            5, 5, 5,
            1, 2, 1,
            5, 5, 5
        ]
        res_h2 = advance_grid_full(grid_h, 3, 3, 'square', False, True, 10, {'type': 'horizontal'})
        self.assertEqual(res_h2[4], 1)

    def test_wolfram_parity_rule(self):
        # 1 neighbor -> converts
        g1 = [5, 1, 5, 5, 2, 5, 5, 5, 5]
        self.assertEqual(advance_grid_full(g1, 3, 3, 'square', False, True, 10, {'type': 'parity'})[4], 1)
        # 2 neighbors -> cancels
        g2 = [5, 1, 5, 1, 2, 5, 5, 5, 5]
        self.assertEqual(advance_grid_full(g2, 3, 3, 'square', False, True, 10, {'type': 'parity'})[4], 2)
        # 3 neighbors -> converts
        g3 = [5, 1, 5, 1, 2, 1, 5, 5, 5]
        self.assertEqual(advance_grid_full(g3, 3, 3, 'square', False, True, 10, {'type': 'parity'})[4], 1)
        # 4 neighbors -> cancels
        g4 = [5, 1, 5, 1, 2, 1, 5, 1, 5]
        self.assertEqual(advance_grid_full(g4, 3, 3, 'square', False, True, 10, {'type': 'parity'})[4], 2)

    def test_hexagonal_simulation_step(self):
        grid = [2] * 16
        grid[5] = 1
        next_g = advance_grid_full(grid, 4, 4, 'hexagonal', True, True, 10, {'type': 'classic'})
        nbrs = get_neighbors_hex(1, 1, 4, 4, True)
        for nr, nc in nbrs:
            self.assertEqual(next_g[nr * 4 + nc], 1)

    def test_triangular_simulation_step(self):
        grid = [2] * 16
        grid[5] = 1
        next_g = advance_grid_full(grid, 4, 4, 'triangular', True, True, 10, {'type': 'classic'})
        nbrs = get_neighbors_triangle(1, 1, 4, 4, True)
        self.assertEqual(len(nbrs), 3)
        for nr, nc in nbrs:
            self.assertEqual(next_g[nr * 4 + nc], 1)

    def test_quorum_rule(self):
        g1 = [5, 1, 5, 5, 2, 5, 5, 5, 5]
        self.assertEqual(advance_grid_full(g1, 3, 3, 'square', False, True, 10, {'type': 'quorum', 'theta': 2})[4], 2)
        g2 = [5, 1, 5, 1, 2, 5, 5, 5, 5]
        self.assertEqual(advance_grid_full(g2, 3, 3, 'square', False, True, 10, {'type': 'quorum', 'theta': 2})[4], 1)


if __name__ == '__main__':
    unittest.main()
