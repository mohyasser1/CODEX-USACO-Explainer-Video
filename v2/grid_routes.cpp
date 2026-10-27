#include <algorithm>
#include <iostream>
#include <queue>
#include <string>
#include <vector>
using namespace std;
int main() {
    int h, w;
    if (!(cin >> h >> w) || h < 1 || w < 1 || h > 500 || w > 500) return 1;
    vector<string> grid(h); int start = -1, target = -1;
    for (int r = 0; r < h; ++r) {
        if (!(cin >> grid[r]) || static_cast<int>(grid[r].size()) != w) return 1;
        for (int c = 0; c < w; ++c) {
            char x = grid[r][c];
            if (x == 'S') { if (start != -1) return 1; start = r*w+c; }
            else if (x == 'T') { if (target != -1) return 1; target = r*w+c; }
            else if (x != '.' && x != '#') return 1;
        }
    }
    if (start == -1 || target == -1) return 1;
    vector<int> distance(h*w,-1), parent(h*w,-1); queue<int> pending;
    distance[start]=0; pending.push(start);
    const int dr[4]={-1,0,1,0}, dc[4]={0,1,0,-1};
    while (!pending.empty()) {
        int u=pending.front(); pending.pop(); int r=u/w,c=u%w;
        for (int k=0;k<4;++k) {
            int nr=r+dr[k],nc=c+dc[k];
            if (nr<0 || nr>=h || nc<0 || nc>=w) continue;
            if (grid[nr][nc]=='#') continue;
            int v=nr*w+nc;
            if (distance[v]!=-1) continue;
            distance[v]=distance[u]+1; parent[v]=u; pending.push(v);
        }
    }
    cout << distance[target] << '\n';
    if (distance[target]==-1) return 0;
    vector<int> path;
    for(int u=target;u!=-1;u=parent[u]) path.push_back(u);
    reverse(path.begin(),path.end());
    for (int u:path) cout << u/w << ' ' << u%w << '\n';
}
