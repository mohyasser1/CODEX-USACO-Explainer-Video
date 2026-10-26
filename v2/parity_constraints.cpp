// stdin adaptation of the same/different constraint model.
// n m, then m lines: S|D u v (1-based). Print number of solutions in binary.
#include <iostream>
#include <queue>
#include <utility>
#include <vector>
#include <string>
int main() {
    int n,m;
    if (!(std::cin>>n>>m) || n<1 || n>100000 || m<0 || m>100000) return 1;
    std::vector<std::vector<std::pair<int,int>>> g(n);
    for (int i=0;i<m;++i) {
        char kind; int u,v;
        if (!(std::cin>>kind>>u>>v) || (kind!='S' && kind!='D') || u<1 || u>n || v<1 || v>n) return 1;
        --u; --v;
        int parity=(kind=='D');
        g[u].push_back({v,parity}); g[v].push_back({u,parity});
    }
    std::vector<int> color(n,-1);
    int components=0;
    for (int root=0;root<n;++root) {
        if (color[root]!=-1) continue;
        ++components;
        std::queue<int> q; color[root]=0; q.push(root);
        while (!q.empty()) {
            int u=q.front();q.pop();
            for (auto [v,parity]:g[u]) {
                int required=color[u]^parity;
                if (color[v]==-1) {color[v]=required;q.push(v);}
                else if (color[v]!=required) {std::cout<<"0\n";return 0;}
            }
        }
    }
    // Each consistent connected component has exactly two assignments.
    // 2^components is 1 followed by components zeroes in binary.
    std::cout<<'1'<<std::string(components,'0')<<'\n';
}
