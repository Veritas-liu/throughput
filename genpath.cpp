#include <iostream>
#include <vector>
#include <queue>
#include <map>
#include <algorithm>
#include <filesystem>
#include <fstream>
#include <string>

namespace fs = std::filesystem;
using namespace std;

struct Path {
  vector<int> nodes;
  int len;
};

int n, m;
vector<vector<int>> adj;
vector<vector<vector<Path>>> all_paths; // all_paths[src][dst] = vector of Paths

void bfs_all_paths(int src) {
  vector<int> dist(n, -1);
  vector<vector<vector<int>>> paths(n); // paths[v]: list of paths to v
  queue<int> q;
  dist[src] = 0;
  paths[src].push_back({src});
  q.push(src);

  while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int v : adj[u]) {
      if (dist[v] == -1) {
        dist[v] = dist[u] + 1;
        q.push(v);
      }
      if (dist[v] == dist[u] + 1) {
        for (auto &p : paths[u]) {
          auto np = p;
          np.push_back(v);
          paths[v].push_back(np);
        }
      }
    }
  }

  for (int dst = 0; dst < n; ++dst) {
    vector<Path> dst_paths;
    for (auto &p : paths[dst]) {
      dst_paths.push_back({p, (int)p.size() - 1});
    }
    all_paths[src][dst] = dst_paths;
  }
}

int main() {
  string data_dir = "./data/";
  for (const auto& entry : fs::directory_iterator(data_dir)) {
    if (entry.path().extension() == ".topo") {
      string topo_file = entry.path().string();
      string path_file = topo_file.substr(0, topo_file.size() - 5) + ".path";
      if (fs::exists(path_file)) {
        cout << path_file << " already exist" << endl;
        continue;
      }
      ifstream fin(topo_file);
      if (!fin) {
        cerr << "Failed to open " << topo_file << endl;
        continue;
      }
      fin >> n >> m;
      adj.assign(n, vector<int>());
      for (int i = 0; i < m; ++i) {
        int u, v;
        fin >> u >> v;
        adj[u].push_back(v);
      }
      fin.close();

      all_paths.assign(n, vector<vector<Path>>(n));
      for (int src = 0; src < n; ++src) {
        bfs_all_paths(src);
      }

      ofstream fout(path_file);
      for (int src = 0; src < n; ++src) {
        for (int dst = 0; dst < n; ++dst) {
          auto& paths = all_paths[src][dst];
          if (paths.empty()) continue;
          fout << src << " " << dst << " " << paths.size();
          for (auto& p : paths) {
            fout << " " << p.len;
            for (int node : p.nodes) fout << " " << node;
          }
          fout << endl;
        }
      }
      fout.close();
      cout << "Created " << path_file << endl;
    }
  }
  return 0;
}