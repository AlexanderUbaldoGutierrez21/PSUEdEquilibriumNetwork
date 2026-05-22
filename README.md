# Frank-Wolfe Algorithm for Traffic Equilibrium

This project implements the Frank-Wolfe algorithm with diminishing step size for solving the Traffic Assignment Problem. It computes user equilibrium flows in a transportation network where travel costs depend on the flow on each link.

## Capabilities

- **Beckmann Formulation**: Implements the cost function with flow-dependent travel times
- **Dijkstra Shortest Path**: Uses Dijkstra's algorithm to find minimum cost routes on each iteration
- **Analytical Line Search**: Computes optimal step size (alpha) for faster convergence
- **Convergence Monitoring**: Tracks Total Misplaced Flow (TMF) and Average Excess Cost (AEC)
- **OD Pair Analysis**: Analyzes equilibrium between origin node 1 and destination node 4

## Usage

Terminal MAC Run Script
```
python3 edequilibrium_fw.py
```

## Algorithm Details

The algorithm:
1. Initializes flow using all-or-nothing assignment on free-flow costs
2. Computes shortest paths using Dijkstra with current arc costs
3. Performs analytical line search to find optimal step size
4. Updates flow vector and checks TMF convergence criterion
5. Repeats until convergence or maximum iterations reached

### Network Structure

```
Nodes: 1, 2, 3, 4
Arcs: (1,3), (1,2), (3,4), (2,4), (3,2)
```

## Research Purposes

Designed for educational purposes. Serves as a starting point for more complex traffic assignment models and could be adapted for real-time traffic simulation, but it is not intended for production use. It prioritizes clarity over performance, making it suitable for learning and experimentation.
Penn State University (PSU), CE 521 Transportation Network and Systems Analysis. Fall 2025.