#include<bits/stdc++.h>
using namespace std;
int main(int argc, char* argv[]) {
  string topo;
  string dim_str, size_str;
  int dim = 0, size = 0;

  // Parse command line arguments
  for (int i = 1; i < argc; ++i) {
    string arg = argv[i];
    if (arg == "--topo" && i + 1 < argc) {
      topo = argv[++i];
    } else if (arg == "--dim" && i + 1 < argc) {
      dim_str = argv[++i];
      dim = stoi(dim_str);
    } else if (arg == "--size" && i + 1 < argc) {
      size_str = argv[++i];
      size = stoi(size_str);
    }
  }

  if (topo.empty() || dim <= 0 || size <= 0) {
    cerr << "Usage: gentopo --topo turos/mesh --dim n --size k\n";
    return 1;
  }
  if (size <= 2 && topo == "turos") {
    cerr << "Turos topology requires size > 2\n";
    return 1;
  }

  // Generate topology
  cout << "Generating " << dim << "D "<<topo<<" topology with size " << size << endl;
  int total_nodes = pow(size, dim);
  vector<vector<int>> coords(total_nodes, vector<int>(dim, 0));
  map<vector<int>, int> coord_to_id;
  for(int i = 0; i < total_nodes; ++i) {
    int x = i;
    for(int d = 0; d < dim; ++d) {
      coords[i][d] = x % size;
      x /= size;
    }
    coord_to_id[coords[i]] = i;
  }
  vector<pair<int, int>> edges;
  if(topo == "turos") {
    for(int i = 0; i < total_nodes; ++i) {
      for(int d = 0; d < dim; ++d) {
        vector<int> neighbor = coords[i];
        neighbor[d] = (neighbor[d] + 1) % size; // wrap around
        int neighbor_id = coord_to_id[neighbor];
        edges.emplace_back(i, neighbor_id);
        edges.emplace_back(neighbor_id, i); // undirected
      }
    }
  } else if(topo == "mesh") {
    for(int i = 0; i < total_nodes; ++i) {
      for(int d = 0; d < dim; ++d) {
        for (int k = 0; k < size; ++k) {
          if (k != coords[i][d]) {
            vector<int> neighbor = coords[i];
            neighbor[d] = k;
            int neighbor_id = coord_to_id[neighbor];
            edges.emplace_back(i, neighbor_id);
            // edges.emplace_back(neighbor_id, i); // undirected
          }
        }
      }
    }
  } else {
    cerr << "Unsupported topology: " << topo << endl;
    return 1;
  }

  char path[500];
  sprintf(path, "./data/%s_%dd_%d.topo", topo.c_str(), dim, size);
  freopen(path, "w",stdout);
  cout << total_nodes << " " << edges.size() << endl;
  for (const auto& e : edges) {
    cout << e.first << " " << e.second << endl;
  }
  fclose(stdout);
}