import itertools

def get_adj_count(board, r, c):
    """Calculates how many targets are adjacent to the given tile."""
    return sum(1 for br, bc in board if max(abs(br - r), abs(bc - c)) <= 1 and (br, bc)!= (r, c))

def main():
    # A 5x5 grid uses coordinates from 0 to 4
    grid_coords = [(r, c) for r in range(5) for c in range(5)]
    
    # Generate all 12,650 possible starting combinations of 4 targets
    valid_boards = list(itertools.combinations(grid_coords, 4))
    revealed = {}

    print("--- 5x5 Grid Solver Initialized ---")
    print("Displays are in 1-based indexing (1 to 5). Top-left is '1, 1'.")
    print("Please INPUT your moves using 0-based indexing (0 to 4) as before.")
    
    try:
        b_input = input("Enter your Bonus 'B' value (default 0): ").strip()
        B = int(b_input) if b_input else 0
    except:
        B = 0
        
    print("Optimal First Move: Center tile at '3, 3'.\n")
    
    while True:
        if len(valid_boards) == 0:
            print("Error: No valid boards left. Double-check your inputted clues.")
            break
            
        if len(valid_boards) == 1:
            print("\nBOARD COMPLETELY SOLVED! The 4 targets are located at (1-based):")
            print([(r + 1, c + 1) for r, c in valid_boards[0]])
            break

        # 0. Count targets and moves
        ts_found = sum(1 for c, val in revealed.items() if val == 'T')
        numbers_found = sum(1 for c, val in revealed.items() if val != 'T')
        clicks_left = 7 - numbers_found - (1 if ts_found == 4 else 0)

        # 1. Calculate efficiency (Points per Move Spent) for each unrevealed tile
        expected_points = {coord: 0.0 for coord in grid_coords if coord not in revealed}
        probs = {coord: 0.0 for coord in grid_coords if coord not in revealed}
        
        points_mapping = [10+B, 20+B, 35+B, 55+B, 90+B]
        target_pts = (150+B) if ts_found == 3 else (5+B)
        
        for coord in expected_points:
            t_count = sum(1 for b in valid_boards if coord in b)
            num_pts_sum = sum(points_mapping[get_adj_count(b, coord[0], coord[1])] for b in valid_boards if coord not in b)
            
            prob_t = t_count / len(valid_boards)
            probs[coord] = prob_t
            
            exp_num_pts = num_pts_sum / len(valid_boards)

            unk_neighbors = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    nr, nc = coord[0] + dr, coord[1] + dc
                    if 0 <= nr < 5 and 0 <= nc < 5:
                        if (nr, nc) not in revealed:
                            unk_neighbors += 1
            info_bonus = unk_neighbors * B * 0.2

            exp_moves = 1.0 if ts_found == 3 else (1 - prob_t)
            if exp_moves < 0.0001: exp_moves = 0.0001
            
            expected_points[coord] = (prob_t * target_pts + exp_num_pts + info_bonus) / exp_moves

        # 2. Determine the best next move
        print(f"\n--- Remaining Configurations: {len(valid_boards)} | Clicks Left: {max(0, clicks_left)} ---")
        if ts_found == 3:
            print("🚨 3 Purples Found: The RED TILE is revealed! 🚨")
        elif len(valid_boards) == 1:
            print("BOARD COMPLETELY SOLVED!")
            
        guaranteed_targets = [coord for coord, p in probs.items() if p == 1.0]
        best_guess_coord = max(expected_points.items(), key=lambda x: x[1])[0]
        best_p = probs[best_guess_coord]

        if clicks_left <= 0 and best_p < 1.0:
            print("BEST MOVE: Out of clicks! Game Over.")
        elif guaranteed_targets and ts_found < 3:
            print(f"BEST MOVE: Click {[(r+1, c+1) for r, c in guaranteed_targets]}! FREE Guaranteed Target.")
        elif best_p == 1.0 and ts_found == 3:
            print(f"BEST MOVE: Click {(best_guess_coord[0]+1, best_guess_coord[1]+1)}! RED TILE (150+B pts).")
        else:
            print(f"BEST MOVE: Click {(best_guess_coord[0]+1, best_guess_coord[1]+1)} (Target Chance: {best_p*100:.1f}%, Efficiency: {expected_points[best_guess_coord]:.2f})")

        if len(valid_boards) == 1 and ts_found == 4 and clicks_left > 0:
            board = valid_boards[0]
            farmable_numbers = []
            for r in range(5):
                for c in range(5):
                    if (r, c) not in board and (r, c) not in revealed:
                        val = get_adj_count(board, r, c)
                        if val > 0: farmable_numbers.append(((r, c), val))
            farmable_numbers.sort(key=lambda x: x[1], reverse=True)
            if farmable_numbers:
                print("FARMING TIME! Use your remaining clicks on these extra points:")
                for coord, val in farmable_numbers:
                    print(f"  - Click {(coord[0]+1, coord[1]+1)} for {points_mapping[val]} points.")

        # 3. Print the board state visually
        print("\nGrid Probabilities (Target %):")
        for r in range(5):
            row_str = []
            for c in range(5):
                if (r, c) in revealed:
                    # Show the revealed clue
                    row_str.append(f"[{revealed[(r, c)]:>3}]")
                else:
                    # Show the probability of being a 100-point tile
                    row_str.append(f"{probs[(r, c)]*100:>4.0f}%")
            print(" ".join(row_str))

        # 4. Ask the user for the result
        try:
            user_input = input("\nEnter move as 'row col value' (INPUT 0-4): ").strip().upper()
            if not user_input: 
                continue
            r_str, c_str, val = user_input.split()
            r, c = int(r_str), int(c_str)
            
            revealed[(r, c)] = val
            
            # 5. Filter the remaining valid boards based on the new information
            new_boards =
            for board in valid_boards:
                if val == 'T':
                    # If it's a target, keep boards that have a target at this location
                    if (r, c) in board:
                        new_boards.append(board)
                else:
                    # If it's a number, keep boards where the target count matches the clue
                    if (r, c) not in board and get_adj_count(board, r, c) == int(val):
                        new_boards.append(board)
            valid_boards = new_boards
            
        except Exception as e:
            print("Invalid input. Please ensure you type it as 'row col value' separated by spaces.")

if __name__ == "__main__":
    main()