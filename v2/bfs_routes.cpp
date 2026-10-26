// n m start target, then m undirected edges. Vertices are 0..n-1.
// Print all distances (-1 if unreachable), then one shortest path or UNREACHABLE.
// Every edge represents one equal-cost step. 1<=n<=200000, 0<=m<=200000.
#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>
int main() {
    int n,m,start,target;
    if (!(std::cin>>n>>m>>start>>target) || n<1 || n>200000 || m<0 || m>200000 || start<0 || start>=n || target<0 || target>=n) return 1;
    std::vector<std::vector<int>> g(n);
    for (int i=0;i<m;++i) {
        int u,v;
        if (!(std::cin>>u>>v) || u<0 || u>=n || v<0 || v>=n) return 1;
        g[u].push_back(v);g[v].push_back(u);
    }
    std::vector<int> distance(n,-1),parent(n,-1);
    std::queue<int> q;
    distance[start]=0;q.push(start);
    while (!q.empty()) {
        int u=q.front();q.pop();
        for (int v:g[u]) {
            if (distance[v]!=-1) continue;
            distance[v]=distance[u]+1;parent[v]=u;q.push(v);
        }
    }
    for (int v=0;v<n;++v) std::cout<<(v?" ":"")<<distance[v];
    std::cout<<'\n';
    if (distance[target]==-1) {std::cout<<"UNREACHABLE\n";return 0;}
    std::vector<int> path;
    for (int v=target;v!=-1;v=parent[v]) path.push_back(v);
    std::reverse(path.begin(),path.end());
    for (int i=0;i<static_cast<int>(path.size());++i) std::cout<<(i?" ":"")<<path[i];
    std::cout<<'\n';
}
