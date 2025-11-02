import numpy as np
import heapq

# COST FUNCTIONS 
def t_a(x):
    """Arc indices: 0:(1,3), 1:(1,2), 2:(3,4), 3:(2,4), 4:(3,2)"""
    return np.array([50 + x[0], 10 + x[1], 10 * x[2], 50 + x[3], 10 + x[4]])
def t_prime():
    return np.array([1.0, 1.0, 10.0, 1.0, 1.0])

# FRANK-WOLFE ALGORITHM WITH DIMINISHING STEP SIZE 

def frank_wolfe_diminishing(TMF_threshold=0.01, max_iter=2000):

    # NETWORK DEFINITION (OD PAIR 1-4) 
    A = { 1: [(3, 0), (2, 1)], 2: [(4, 3)], 3: [(4, 2), (2, 4)], 4: [] }
    num_arcs = 5
    t_prime_vec = t_prime()

    # INITIALIZATION (ALL-OR-NOTHING ON FREE-FLOW)
    kappa_0 = 50.0
    D_0 = max(0, 15 - kappa_0 / 30.0) 

    x_k = np.zeros(num_arcs)
    x_k[1] = D_0 # FLOW ON (1, 2)
    x_k[3] = D_0 # FLOW ON (2, 4)
    D_k = D_0

    TMF = float('inf')
    k = 0

    print(f"Starting FW with Analytical Line Search...")

    while TMF > TMF_threshold and k < max_iter:
        k += 1

        # CALCULATE ARC COSTS 
        current_costs = t_a(x_k)

        # DIJKSTRA (FIND KAPPA AND PREDECESSORS) 
        distances = {node: np.inf for node in A}
        distances[1] = 0.0
        predecessors = {node: None for node in A}
        priority_queue = [(0.0, 1)]

        while priority_queue:
            dist_u, u = heapq.heappop(priority_queue)
            if dist_u > distances[u]: continue
            if u == 4: break

            for v, arc_index in A.get(u, []):
                new_dist = distances[u] + current_costs[arc_index]
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    predecessors[v] = (u, arc_index)
                    heapq.heappush(priority_queue, (new_dist, v))

        # MINIMUM COST (EQUILIBRIUM COST) 
        kappa = distances[4]

        # UPDATE DEMAND AND ALL-OR-NOTHING FLOW (Y)
        D_new = max(0, 15 - kappa / 30.0)
        y = np.zeros(num_arcs)

        # TRACEBACK TO LOAD FLOW Y
        current_node = 4
        if distances[4] != np.inf and D_new > 0:
            while current_node != 1 and predecessors.get(current_node) is not None:
                prev_node, arc_index = predecessors[current_node]
                y[arc_index] = D_new
                current_node = prev_node

        # ANALYTICAL LINE SEARCH (ALPHA) 
        d = y - x_k 

        A_coeff = np.sum(d**2 * t_prime_vec)
        B_coeff = np.sum(current_costs * d)

        if A_coeff > 1e-9: 
            alpha_star = -B_coeff / A_coeff
            alpha = np.clip(alpha_star, 0.0, 1.0)
        else:
            alpha = 0.0 

        # UPDATE FLOWS AND CONVERGENE CHECK 
        d = y - x_k 
        x_k_plus_1 = x_k + alpha * d

        # CONVERGENCE CHECK: TMF IS CALCULATED BETWEEN NEW FLOW AND THE TARGET Y
        TMF = np.sum(np.abs(x_k_plus_1 - y))

        x_k = x_k_plus_1
        D_k = D_new

        # DEBUGGING HOOK: TO SHOW THE SLOW CONVERGENCE
        # IF K == 100:
        #    PRINT("KK") PRNT (F"--- ITERATION 100 RESULTS ---")
        #    PRINT(F"KAPPA: {KAPPA:.4F}, D: {D_K:.4F}, TMF: {TMF:.6F}")

    # REPORT FINAL RESULTS
    final_costs = t_a(x_k)
    AEC = (np.sum(final_costs * x_k) - kappa * D_k) / D_k if D_k > 0 else 0

    print("\n--- Final Equilibrium Results ---")
    print(f"Converged after {k} iterations (TMF < {TMF_threshold})")
    print("-" * 40)
    print(f"Equilibrium Cost (kappa): {kappa:.4f}")
    print(f"Equilibrium Demand (D): {D_k:.4f}")
    print(f"Final Flows (x): {x_k.round(4)}")
    print(f"Total Misplaced Flow (TMF): {TMF:.6f}")
    print(f"Average Excess Cost (AEC): {AEC:.6f}")
    print("-" * 40)

    return k

# EXECUTVE FRANK-WOLFE ALGORITHM 
required_iterations = frank_wolfe_diminishing(TMF_threshold=0.01)