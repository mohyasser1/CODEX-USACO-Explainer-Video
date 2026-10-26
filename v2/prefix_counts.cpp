// Course contract: n>=1, q>=0, both <=100000; categories 1..3.
// Queries use 1-based inclusive l,r. Outputs counts for categories 1,2,3.
// stdin/stdout; historical Breed Counting uses bcount.in/bcount.out instead.
#include <array>
#include <iostream>
#include <vector>
int main() {
  int n, q;
  if (!(std::cin >> n >> q) || n < 1 || n > 100000 || q < 0 || q > 100000)
    return 1;
  std::vector<std::array<int, 3>> prefix(n + 1, std::array<int, 3>{0, 0, 0});
  for (int i = 0; i < n; ++i) {
    int category;
    if (!(std::cin >> category) || category < 1 || category > 3)
      return 1;
    prefix[i + 1] = prefix[i];
    ++prefix[i + 1][category - 1];
  }
  for (int j = 0; j < q; ++j) {
    int l, r;
    if (!(std::cin >> l >> r) || l < 1 || l > r || r > n)
      return 1;
    for (int c = 0; c < 3; ++c) {
      if (c)
        std::cout << ' ';
      std::cout << prefix[r][c] - prefix[l - 1][c];
    }
    std::cout << '\n';
  }
}
