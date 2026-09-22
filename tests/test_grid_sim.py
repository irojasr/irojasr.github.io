#!/usr/bin/env python3
"""
Test suite for the Interactive Grid Simulation.
Tests mathematical state transitions, boundary behaviors, cyclic/linear rules,
and edge cases.
"""

import unittest

def get_neighbors(r, c, m, n, periodic=True):
    """
    Returns unique orthogonal neighbor coordinates for cell (r, c).
    Guarantees no self-loops and no duplicate neighbors.
    """
    neighbors = []
    
    # Vertical neighbors
    if m > 1:
        if periodic:
            up = ((r - 1 + m) % m, c)
            down = ((r + 1) % m, c)
            neighbors.append(up)
            if down != up:
                neighbors.append(down)
        else:
            if r > 0:
                neighbors.append((r - 1, c))
            if r < m - 1:
                neighbors.append((r + 1, c))
                
    # Horizontal neighbors
    if n > 1:
        if periodic:
            left = (r, (c - 1 + n) % n)
            right = (r, (c + 1) % n)
            neighbors.append(left)
            if right != left:
                neighbors.append(right)
        else:
            if c > 0:
                neighbors.append((r, c - 1))
            if c < n - 1:
                neighbors.append((r, c + 1))
                
    # Filter out any accidental self-neighbor (should never occur with m>1/n>1 checks)
    distinct = []
    for nbr in neighbors:
        if nbr != (r, c) and nbr not in distinct:
            distinct.append(nbr)
    return distinct


def advance_grid(grid, m, n, periodic=True, cyclic=True, max_val=10):
    """
    Deterministic pure function for one synchronous grid step.
    grid: 1D list of length m * n with integers in 1..max_val.
    Returns: new 1D list of length m * n.
    """
    next_grid = list(grid)
    
    for r in range(m):
        for c in range(n):
            idx = r * n + c
            v = grid[idx]
            
            # Determine target predecessor value that can convert this cell
            if cyclic:
                pred = max_val if v == 1 else (v - 1)
            else:
                pred = (v - 1) if v > 1 else None
                
            if pred is not None:
                nbrs = get_neighbors(r, c, m, n, periodic)
                has_pred = any(grid[nr * n + nc] == pred for nr, nc in nbrs)
                if has_pred:
                    next_grid[idx] = pred
                    
    return next_grid


class TestGridSimulation(unittest.TestCase):

    def test_constant_grid(self):
        """A constant grid should be a fixed point."""
        for val in range(1, 11):
            grid = [val] * 16
            next_g = advance_grid(grid, 4, 4, periodic=True, cyclic=True, max_val=10)
            self.assertEqual(grid, next_g, f"Constant grid of {val} must not change")

    def test_1x1_grid(self):
        """A 1x1 grid has 0 neighbors and must remain fixed."""
        for val in range(1, 11):
            grid = [val]
            next_p = advance_grid(grid, 1, 1, periodic=True, cyclic=True, max_val=10)
            next_f = advance_grid(grid, 1, 1, periodic=False, cyclic=True, max_val=10)
            self.assertEqual(grid, next_p, "1x1 periodic grid must remain fixed")
            self.assertEqual(grid, next_f, "1x1 fixed grid must remain fixed")

    def test_immutability(self):
        """advance_grid must not mutate the original grid."""
        grid = [1, 2, 3, 4]
        grid_copy = list(grid)
        next_g = advance_grid(grid, 1, 4, periodic=False, cyclic=True, max_val=4)
        self.assertEqual(grid, grid_copy, "Original grid must not be mutated")
        self.assertIsNot(grid, next_g, "New grid must be a distinct object")

    def test_1x4_all_scenarios(self):
        """
        Verify the four claimed scenarios for (1, 2, 3, 4):
        1. Fixed + Linear
        2. Periodic + Linear
        3. Fixed + Cyclic
        4. Periodic + Cyclic
        """
        initial = [1, 2, 3, 4]
        
        # 1. Fixed + Linear:
        res1 = advance_grid(initial, 1, 4, periodic=False, cyclic=False, max_val=4)
        self.assertEqual(res1, [1, 1, 2, 3], "Fixed + Linear must yield [1, 1, 2, 3]")
        
        # 2. Periodic + Linear:
        res2 = advance_grid(initial, 1, 4, periodic=True, cyclic=False, max_val=4)
        self.assertEqual(res2, [1, 1, 2, 3], "Periodic + Linear must yield [1, 1, 2, 3]")
        
        # 3. Fixed + Cyclic (with max_val=4):
        res3 = advance_grid(initial, 1, 4, periodic=False, cyclic=True, max_val=4)
        self.assertEqual(res3, [1, 1, 2, 3], "Fixed + Cyclic must yield [1, 1, 2, 3]")
        
        # 4. Periodic + Cyclic (with max_val=4):
        # Here 4 is adjacent to 1, and 4 wraps to 1 (4 converts 1 into 4).
        # Every entry shifts right cyclically!
        res4 = advance_grid(initial, 1, 4, periodic=True, cyclic=True, max_val=4)
        self.assertEqual(res4, [4, 1, 2, 3], "Periodic + Cyclic (max=4) must cyclically shift to [4, 1, 2, 3]")
        
        # Subsequent steps of the 4-cycle:
        step2 = advance_grid(res4, 1, 4, periodic=True, cyclic=True, max_val=4)
        self.assertEqual(step2, [3, 4, 1, 2])
        step3 = advance_grid(step2, 1, 4, periodic=True, cyclic=True, max_val=4)
        self.assertEqual(step3, [2, 3, 4, 1])
        step4 = advance_grid(step3, 1, 4, periodic=True, cyclic=True, max_val=4)
        self.assertEqual(step4, [1, 2, 3, 4], "After 4 steps, state must return to initial configuration")

    def test_1x10_cyclic_shift(self):
        """Under periodic + cyclic max_val=10, a 1x10 grid with 1..10 cyclically shifts."""
        initial = list(range(1, 11))
        res = advance_grid(initial, 1, 10, periodic=True, cyclic=True, max_val=10)
        expected = [10] + list(range(1, 10))
        self.assertEqual(res, expected, "(1..10) must cyclically shift right to (10, 1..9)")

    def test_mx1_vertical_cyclic_shift(self):
        """A column grid (4x1) with periodic + cyclic max_val=4 also cyclically shifts downwards."""
        initial = [1, 2, 3, 4]
        res = advance_grid(initial, 4, 1, periodic=True, cyclic=True, max_val=4)
        self.assertEqual(res, [4, 1, 2, 3], "Vertical 4x1 grid must shift down cyclically")

    def test_10_and_1_interaction(self):
        """Test interaction between 10 and 1."""
        # Under cyclic: 10 converts 1 to 10
        pair = [10, 1]
        res_cyclic = advance_grid(pair, 1, 2, periodic=False, cyclic=True, max_val=10)
        self.assertEqual(res_cyclic, [10, 10], "In cyclic mode, 10 converts adjacent 1 into 10")
        
        # Under linear: 10 cannot convert 1, and 1 cannot convert 10 (difference is 9 != 1)
        res_linear = advance_grid(pair, 1, 2, periodic=False, cyclic=False, max_val=10)
        self.assertEqual(res_linear, [10, 1], "In linear mode, [10, 1] is permanently frozen")

    def test_simultaneous_updates(self):
        """
        Verify that updates are strictly synchronous and not sequential.
        Consider [1, 2, 3]:
        Synchronous:
          1 converts 2 -> 1
          2 converts 3 -> 2
          Result: [1, 1, 2]
        If it were sequential left-to-right:
          1 converts 2 to 1.
          Then modified 1 would NOT convert 3.
        """
        grid = [1, 2, 3]
        res = advance_grid(grid, 1, 3, periodic=False, cyclic=False, max_val=10)
        self.assertEqual(res, [1, 1, 2], "Synchronous update must produce [1, 1, 2]")

    def test_competing_updates_no_conflict(self):
        """
        A cell with value 2 surrounded by multiple 1s:
        All 1s try to convert 2 to 1. The result is deterministically 1 with no conflict.
        """
        grid = [
            0, 1, 0,
            1, 2, 1,
            0, 1, 0
        ]
        # Replace 0s with 5 (which does not interact with 1 or 2)
        grid = [5 if x == 0 else x for x in grid]
        res = advance_grid(grid, 3, 3, periodic=False, cyclic=True, max_val=10)
        center_idx = 1 * 3 + 1
        self.assertEqual(res[center_idx], 1, "Cell with value 2 surrounded by 1s must become 1")

    def test_single_low_value_expansion(self):
        """A single 1 surrounded by 2s expands in a diamond wavefront."""
        grid = [2] * 25
        grid[12] = 1 # center cell (2, 2) in 5x5
        
        # Step 1: center cell's 4 orthogonal neighbors become 1
        s1 = advance_grid(grid, 5, 5, periodic=False, cyclic=True, max_val=10)
        self.assertEqual(s1[12], 1)
        self.assertEqual(s1[7], 1)  # up
        self.assertEqual(s1[17], 1) # down
        self.assertEqual(s1[11], 1) # left
        self.assertEqual(s1[13], 1) # right
        # Diagonals still 2
        self.assertEqual(s1[6], 2)
        self.assertEqual(s1[8], 2)
        self.assertEqual(s1[16], 2)
        self.assertEqual(s1[18], 2)

    def test_no_valid_updates(self):
        """Grid with only odd values (1, 3, 5) has no adjacent k and k+1; remains unchanged."""
        grid = [1, 3, 5, 1, 3, 5, 1, 3, 5]
        res = advance_grid(grid, 3, 3, periodic=True, cyclic=True, max_val=10)
        self.assertEqual(grid, res, "Grid with no adjacent k and k+1 must remain unchanged")


if __name__ == '__main__':
    unittest.main()
