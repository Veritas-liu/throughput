import sys
import os
import datetime
import ortools.linear_solver.pywraplp as pywraplp

def solve_mlu(n, edges, paths):
  solver = pywraplp.Solver.CreateSolver('GLOP')
  edge_indices = {e: i for i, e in enumerate(edges)}
  # For each path, create a variable for its flow
  path_vars = {}
  for (src, dst), plist in paths.items():
    for pi, path in enumerate(plist):
      path_vars[(src, dst, pi)] = solver.NumVar(0, 1, f'f_{src}_{dst}_{pi}')
  # For each edge, sum flows over all paths using this edge
  edge_load = [solver.NumVar(0, solver.infinity(), f'load_{i}') for i in range(len(edges))]
  for ei, (u, v) in enumerate(edges):
    expr = solver.Sum([
      path_vars[(src, dst, pi)]
      for (src, dst), plist in paths.items()
      for pi, path in enumerate(plist)
      if any((path[j], path[j+1]) == (u, v) for j in range(len(path)-1))
    ])
    solver.Add(edge_load[ei] == expr)
  # For each src-dst, sum of flows over all paths = 1
  for (src, dst), plist in paths.items():
    solver.Add(solver.Sum([path_vars[(src, dst, pi)] for pi in range(len(plist))]) == 1)
  # MLU variable
  mlu = solver.NumVar(0, solver.infinity(), 'mlu')
  for load in edge_load:
    solver.Add(load <= mlu)
  solver.Minimize(mlu)
  status = solver.Solve()
  if status == pywraplp.Solver.OPTIMAL:
    # flows = {}
    # for key, var in path_vars.items():
    #   flows[key] = var.solution_value()
    # print("Path flows:")
    # for (src, dst, pi), flow in flows.items():
    #   print(f"src={src}, dst={dst}, path_index={pi}, flow={flow}, path={paths[(src, dst)][pi]}")
    # print("Edge loads:")
    # for ei, (u, v) in enumerate(edges):
    #   print(f"edge=({u},{v}), load={edge_load[ei].solution_value()}")
    return mlu.solution_value()
  else:
    return None

def read_topology(filename):
  with open(filename, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]
  n, m = map(int, lines[0].split())
  edges = []
  for i in range(1, m+1):
    u, v = map(int, lines[i].split())
    edges.append((u, v))
  return n, edges

def read_paths(filename):
  # format: src dst path_count path1 path2 ...
  # each path: length node1 node2 ...
  with open(filename, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]
  paths = {}
  for line in lines:
    parts = line.split()
    src, dst, k = int(parts[0]), int(parts[1]), int(parts[2])
    path_list = []
    idx = 3
    for _ in range(k):
      plen = int(parts[idx])
      # plen+1 nodes: src, ..., dst
      path = tuple(map(int, parts[idx+1:idx+1+plen+1]))
      path_list.append(path)
      idx += 2 + plen
    paths[(src, dst)] = path_list
  return paths

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Usage: python solve.py <toponame>")
    sys.exit(1)

  topo_name = sys.argv[1]
  topo_file = os.path.join('.', 'data', f'{topo_name}.topo')
  path_file = os.path.join('.', 'data', f'{topo_name}.path')

  n, edges = read_topology(topo_file)
  paths = read_paths(path_file)
  mlu = solve_mlu(n, edges, paths)
  print(f'Minimum MLU: {mlu}')
  log_dir = './log'
  os.makedirs(log_dir, exist_ok=True)
  log_file = os.path.join(log_dir, f'{topo_name}.log')
  with open(log_file, 'a') as f:
    f.write(f"{datetime.datetime.now().isoformat()} {topo_name} {mlu}\n")