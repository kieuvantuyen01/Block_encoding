# This is encoding for this formula A:
# X1 -> (X2 ^ X3 ^...^ Xk) ^ (-Xk+1 ^ -Xk+2 ^...^ -Xn)
# -X1 ^ X2 -> (X3 ^ X4 ^...^ Xk+1) ^ (-Xk+2 ^ -Xk+3 ^...^ -Xn)
# -X2 ^ X3 -> (X4 ^ X5 ^...^ Xk+2) ^ (-Xk+3 ^ -Xk+4 ^...^ -Xn)
# ...
# -Xn-k-1 ^ Xn-k -> (Xn-k+1 ^ Xn-k+2 ^...^ Xn-1) ^ (-Xn)
# -Xn-k ^ Xn-k+1 -> Xn-k+2 ^ Xn-k+3 ^...^ Xn

# Idea: We devide the right part the formula to 2 types of blocks: block All Zero and block All One
# Block All Zero has staircase structure:
# -Xk+1 ^ -Xk+2 ^ -Xk+3^...^ -Xn-1 ^ -Xn
#         -Xk+2 ^ -Xk+3^...^ -Xn-1 ^ -Xn
#                       ...
#                 -Xn-2 ^ -Xn-1 ^ -Xn
#                         -Xn-1 ^ -Xn
#                                 -Xn

# We use auxiliary variables R(a) to encode the block All Zero:
# -Xn-1 ^ -Xn <-> R1
# -Xn-2 ^ -Xn-1 ^ -Xn <-> R2
# ...
# -Xk+2 ^ -Xk+3^...^ -Xn-1 ^ -Xn <-> Rn-k-2
# -Xk+1 ^ -Xk+2 ^ -Xk+3^...^ -Xn-1 ^ -Xn <-> Rn-k-1
# We encode the block All Zero by the following clauses:
# For R1: 3 clauses
# -Xn-1 ^ -Xn -> R1
# Xn-1 -> -R1
# Xn -> -R1
# For m >= 1:
# -Xn-m-1 ^ Rm -> Rm+1
# Xn-m-1 -> -Rm+1
# -Rm -> -Rm+1

# Block All One:
# X2 ^ X3 ^ X4 ^...^ Xk
#      X3 ^ X4 ^...^ Xk ^ Xk+1
#           X4 ^...^ Xk ^ Xk+1 ^ Xk+2
#              ...
#                   Xn-k-3 ^ Xn-k-2 ^...^ Xn-1

# We must devide this structure to [[n/(k-1)] sub-blocks has size (k-1):
# Xi ^ Xi+1 ^ Xi+3 ^...^ Xi+k-3 ^ Xi+k-2
#      Xi+1 ^ Xi+3 ^...^ Xi+k-3 ^ Xi+k-2 ^ Xi+k-1
#           ...
#                        Xi+k-3 ^ Xi+k-2 ^...^ Xi+2k-6 ^ Xi+2k-5
#                                 Xi+k-2 ^ Xi+k-1 ^...^ Xi+2k-3 ^ Xi+2k-4



# The left sub-block:
# Xi ^ Xi+1 ^ Xi+3 ^...^ Xi+k-4 ^ Xi+k-3 <-> R(k-3)
#      Xi+1 ^ Xi+3 ^...^ Xi+k-4 ^ Xi+k-3 <-> R(k-4)
#           ...
#               Xi+k-5 ^ Xi+k-4 ^ Xi+k-3 <-> R2
#                        Xi+k-4 ^ Xi+k-3 <-> R1
#                                 Xi+k-3
# We encode this sub-block by the following clauses:
# For R1: 3 clauses
# Xi+k-4 ^ Xi+k-3 -> R1
# -Xi+k-4 -> -R1
# -Xi+k-3 -> -R1
# For m >= 1:
# Xi+k-m-4 ^ Rm -> Rm+1
# -Xi+k-m-4 -> -Rm+1
# -Rm -> -Rm+1

# The right sub-block:
# Xi+k-2
# Xi+k-2 ^ Xi+k-1 <-> R1
# Xi+k-2 ^ Xi+k-1 ^ Xi+k <-> R2
#    ...
# Xi+k-2 ^ Xi+k-1 ^...^ Xi+2k-6 ^ Xi+2k-5 <-> R(k-3)
# Xi+k-2 ^ Xi+k-1 ^...^ Xi+2k-6 ^ Xi+2k-5 ^ Xi+2k-4 <-> R(k-2)
# We encode this sub-block by the following clauses and use auxiliary variables R(c) to encode them:
# For R1: 3 clauses
# Xi+k-2 ^ Xi+k-1 -> R1
# -Xi+k-2 -> -R1
# -Xi+k-1 -> -R1
# For m >= 1:
# Xi+k+m-1 ^ Rm -> Rm+1
# -Xi+k+m-1 -> -Rm+1
# -Rm -> -Rm+1

# We iterate this process for all sub-blocks, but the last sub-block has size < k-1, we must handle it separately
# In there, we try build the last sub-block has size k-1 by extend the representation of origin block All One in order to: size of block divisible by k-1

# We convert the formula A to:
# X1 -> Ra,1 ^ Rb,1 ^ Rc,1
# -X1 ^ X2 -> Ra,2 ^ Rb,2 ^ Rc,2
# -X2 ^ X3 -> Ra,3 ^ Rb,3 ^ Rc,3
# ...
# -Xn-k ^ Xn-k+1 -> Ra,n-k+1 ^ Rb,n-k+1 ^ Rc,n-k+1
# In there, Ra,i is the encoding of block All Zero, Rb,i and Rc,i are the encoding of block All One

# var_index is the index of the first auxiliary variable
# X is list of variables (size n)
# def block_encoding(X, k, var_index):

def block_encoding(X, k, var_index):
    n = len(X) - 1
    clauses = []
    aux_vars = {}  # Keep track of auxiliary variables
    current_var_index = var_index

    ra_clauses, current_var_index, ra_final = encode_all_zero_block(X, n, k, current_var_index)
    clauses.extend(ra_clauses)

    rb_clauses, current_var_index, rb_final = encode_left_all_one_block(X, n, k, current_var_index)
    clauses.extend(rb_clauses)

    rc_clauses, current_var_index, rc_final = encode_right_all_one_block(X, n, k, current_var_index)
    clauses.extend(rc_clauses)

    # Add the main implication clause
    # For each implication in the formula
    # First line
    # X1 -> Ra,1 ^ Rb,1 ^ Rc,1
    clauses.append([-X[1], ra_final[0]])
    if rb_final[0]:
        clauses.append([-X[1], rb_final[0]])
    clauses.append([-X[1], rc_final[0]])
    for i in range(2, n-k+1):
        # -X[i-1] ^ X[i] -> Ra,i ^ Rb,i ^ Rc,i
        clauses.append([X[i-1], -X[i], ra_final[i-1]])
        if rb_final[i-1]:
            clauses.append([X[i-1], -X[i], rb_final[i-1]])
        if rc_final:
            clauses.append([X[i-1], -X[i], rc_final[i-1]])

    # Last line
    if len(rb_final) >= n-k+1:
        if rb_final[n-k]:
            clauses.append([X[n-k], -X[n-k+1], rb_final[n-k]])
    if rc_final:
        clauses.append([X[n-k], -X[n-k+1], rc_final[n-k]])
    
    # # For each implication in the formula
    # for i in range(1, n-k+2):
    #     # Encode block All Zero (Ra,i)
    #     zero_block_vars = []
    #     # Start from k+i and go to n
    #     for j in range(k+i, n+1):
    #         zero_block_vars.append(-X[j-1])  # -1 because X is 0-based
            
    #     ra_clauses, current_var_index, ra_final = encode_all_zero_block(
    #         zero_block_vars, current_var_index)
    #     clauses.extend(ra_clauses)
        
    #     # Encode block All One (split into Rb,i and Rc,i)
    #     one_block_vars = []
    #     # Start from i+1 and collect k-1 variables
    #     for j in range(i+1, min(i+k, n+1)):
    #         one_block_vars.append(X[j-1])
            
    #     rb_rc_clauses, current_var_index, rb_final, rc_final = encode_all_one_block(
    #         one_block_vars, k-1, current_var_index)
    #     clauses.extend(rb_rc_clauses)
        
    #     # Add the main implication clause
    #     if i == 1:
    #         # X1 -> Ra,1 ^ Rb,1 ^ Rc,1
    #         clauses.append([-X[0], ra_final])
    #         clauses.append([-X[0], rb_final])
    #         if rc_final:  # rc_final might be None for small blocks
    #             clauses.append([-X[0], rc_final])
    #     else:
    #         # -X[i-1] ^ X[i] -> Ra,i ^ Rb,i ^ Rc,i
    #         clauses.append([X[i-2], -X[i-1], ra_final])
    #         clauses.append([X[i-2], -X[i-1], rb_final])
    #         if rc_final:
    #             clauses.append([X[i-2], -X[i-1], rc_final])
    
    return clauses, current_var_index

# def encode_all_zero_block(vars, var_index):
#     """Encode block All Zero using auxiliary variables"""
#     clauses = []
#     if not vars:
#         return clauses, var_index, None
        
#     # If we have only one variable
#     if len(vars) == 1:
#         return clauses, var_index, vars[0]
        
#     # First clause: -Xn-1 ^ -Xn -> R1
#     if len(vars) == 2:
#         r1 = var_index
#         clauses.append([*vars[-2:], r1])
#         clauses.append([-vars[-2], -r1])
#         clauses.append([-vars[-1], -r1])

#         return clauses, var_index + 1, r1

#     if len(vars) > 2:
#         current_r = var_index
#         # For remaining variables
#         # for i in range(len(vars)-3, -1, -1):
#         new_r = var_index + 1
#         var_index += 1
#         # -Xn-m-1 ^ Rm -> Rm+1
#         clauses.append([vars[0], current_r, new_r])
#         # Xn-m-1 -> -Rm+1
#         clauses.append([-vars[0], -new_r])
#         # -Rm -> -Rm+1
#         clauses.append([-current_r, -new_r])
#         current_r = new_r
        
#         return clauses, var_index + 1, current_r

def encode_all_zero_block(X, n, k, var_index):
    """Encode block All Zero using auxiliary variables"""
    clauses = []
    r_vars = []  # Store all r variables

    # Add the last variable
    r_vars.append(-X[n])
    
    # First clause: -Xn-1 ^ -Xn -> R1
    r1 = var_index
    clauses.append([X[-2], X[-1], r1])
    clauses.append([-X[-2], -r1])
    clauses.append([-X[-1], -r1])
    r_vars.append(r1)
    current_r = r1  # Initialize current_r
    
    # For remaining variables
    for i in range(n-2, n-k-1, -1):
        new_r = var_index + 1
        var_index += 1
        # -Xn-m-1 ^ Rm -> Rm+1
        clauses.append([X[i], current_r, new_r])
        # Xn-m-1 -> -Rm+1
        clauses.append([-X[i], -new_r])
        # -Rm -> -Rm+1
        clauses.append([-current_r, -new_r])
        current_r = new_r
        r_vars.append(new_r)
    
    r_vars.reverse()
    return clauses, var_index + 1, r_vars

def encode_left_all_one_block(X, n, k, var_index):
    clauses = []
    r_vars = []
    start_id = 2
    end_id = start_id + k - 3
    
    while (start_id < n and end_id < n):
        r_vars_tmp = []
        # Add the last variable
        r_vars_tmp.append(X[end_id])

        if start_id > end_id:
            break
        if start_id == end_id:
            # r_vars.append(X[end_id])
            break
            
        r1 = var_index
        clauses.append([-X[end_id-1], -X[end_id], r1])
        clauses.append([X[end_id-1], -r1])
        clauses.append([X[end_id], -r1])
        r_vars_tmp.append(r1)
        current_r = r1  # Update current_r

        for i in range(end_id-2, start_id-1, -1):
            new_r = var_index + 1
            var_index += 1
            clauses.append([-X[i], -current_r, new_r])
            clauses.append([X[i], -new_r])
            clauses.append([current_r, -new_r])
            current_r = new_r
            r_vars_tmp.append(new_r)

        start_id = start_id + k - 1
        end_id = start_id + k - 3
        r_vars_tmp.reverse()  # Reverse in place
        r_vars.extend(r_vars_tmp)  # Then extend
        if (start_id < n and end_id < n):
            var_index += 1
            r_vars.append(0)
    
    return clauses, var_index + 1, r_vars
    
def encode_right_all_one_block(X, n, k, var_index):
    clauses = []
    r_vars = []
    start_id = k
    end_id = start_id + k - 2

    while (start_id <= n and end_id <= n):
        # Add the first variable
        r_vars.append(X[start_id])

        if start_id > end_id:
            break
        if start_id == end_id:
            # r_vars.append(X[end_id])
            break

        r1 = var_index
        clauses.append([-X[start_id], -X[start_id+1], r1])
        clauses.append([X[start_id], -r1])
        clauses.append([X[start_id+1], -r1])
        r_vars.append(r1)
        current_r = r1  # Update current_r

        for i in range(start_id+2, end_id+1):
            new_r = var_index + 1
            var_index += 1
            clauses.append([-X[i], -current_r, new_r])
            clauses.append([X[i], -new_r])
            clauses.append([current_r, -new_r])
            current_r = new_r
            r_vars.append(new_r)

        start_id = start_id + k - 1
        end_id = start_id + k - 2
        if (start_id <= n):
            var_index += 1

    if start_id <= n and end_id > n:
        r1 = var_index
        clauses.append([-X[start_id], -X[start_id+1], r1])
        clauses.append([X[start_id], -r1])
        clauses.append([X[start_id+1], -r1])
        r_vars.append(r1)
        current_r = r1  # Update current_r

        for i in range(start_id+2, n+1):
            new_r = var_index + 1
            var_index += 1
            clauses.append([-X[i], -current_r, new_r])
            clauses.append([X[i], -new_r])
            clauses.append([current_r, -new_r])
            current_r = new_r
            r_vars.append(new_r)

    return clauses, var_index + 1, r_vars

# def encode_all_one_block(vars, block_size, var_index):
#     """Encode block All One by splitting into two sub-blocks"""
#     clauses = []
#     if not vars:
#         return clauses, var_index, None, None
        
#     # Split into left and right sub-blocks
#     mid = block_size-1
#     left_vars = vars[:mid]
#     right_vars = vars[mid:]
    
#     # Encode left sub-block
#     left_clauses, var_index, rb_final = encode_sub_block(
#         left_vars, var_index, is_right=False)
#     clauses.extend(left_clauses)
    
#     # Encode right sub-block
#     right_clauses, var_index, rc_final = encode_sub_block(
#         right_vars, var_index, is_right=True)
#     clauses.extend(right_clauses)
    
#     return clauses, var_index, rb_final, rc_final

# def encode_sub_block(vars, var_index, is_right):
#     """Encode a sub-block of All One block"""
#     clauses = []
#     if not vars:
#         return clauses, var_index, None
    
#     if len(vars) == 1:
#         return clauses, var_index, vars[0]
        
#     # First clause
#     if len(vars) == 2:
#         r1 = var_index
#         clauses.append([*[-x for x in vars[:2]], r1])
#         clauses.append([vars[0], -r1])
#         clauses.append([vars[1], -r1])

#         return clauses, var_index + 1, r1
        
#     if len(vars) > 2:
#         current_r = var_index
#         # For remaining variables
#         # for i in range(2, len(vars)):
#         new_r = var_index + 1
#         var_index += 1
#         if is_right:
#             clauses.append([-vars[len(vars)-1], current_r, new_r])
#             clauses.append([vars[len(vars)-1], -new_r])
#             clauses.append([-current_r, -new_r])
#         else:
#             clauses.append([-vars[0], current_r, new_r])
#             clauses.append([vars[0], -new_r])
#             clauses.append([-current_r, -new_r])
#         current_r = new_r
    
#         return clauses, var_index + 1, current_r


def test_block_encoding(n, k):
    """
    Test the block encoding implementation with detailed clause printing
    Args:
        n: number of variables
        k: parameter k from the formula
    """
    # Create list of variables [1, 2, ..., n]
    X = list(range(0, n + 1))
    
    # Start auxiliary variables after n
    initial_var_index = n + 1
    
    # Get the encoding
    clauses, final_var_index = block_encoding(X, k, initial_var_index)
    
    # Calculate statistics
    num_aux_vars = final_var_index - initial_var_index
    num_clauses = len(clauses)
    
    # Print results
    print(f"\nStatistics for n={n}, k={k}:")
    print(f"Number of original variables: {n}")
    print(f"Number of auxiliary variables: {num_aux_vars}")
    print(f"Total number of variables: {final_var_index - 1}")
    print(f"Number of clauses: {num_clauses}")
    
    # Print clauses in readable format
    print("\nClauses in detail:")
    print("Format: [literals] means (literal1 ∨ literal2 ∨ ...)")
    print("Negative numbers represent negated variables")
    print("-" * 50)
    
    for i, clause in enumerate(clauses, 1):
        # Convert clause to readable format
        literals = []
        for lit in clause:
            if lit > 0:
                if lit <= n:
                    literals.append(f"X{lit}")
                else:
                    literals.append(f"R{lit-n}")
            else:
                if abs(lit) <= n:
                    literals.append(f"-X{abs(lit)}")
                else:
                    literals.append(f"-R{abs(lit)-n}")
        
        clause_str = " ∨ ".join(literals)
        print(f"Clause {i:3d}: {clause} => ({clause_str})")

# Example usage
if __name__ == "__main__":
    # Test with different values
    test_block_encoding(n=9, k=4)
    print("\n" + "="*50 + "\n")
    # test_block_encoding(n=15, k=4)
