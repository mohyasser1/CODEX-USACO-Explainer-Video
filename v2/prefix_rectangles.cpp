// rows cols q, row-major values, then half-open queries r1 c1 r2 c2.
// 1<=rows,cols<=1000; |value|<=10^9; q<=100000. Empty rectangles allowed.
#include <iostream>
#include <vector>
int main() {
  int rows, cols, q;
  if (!(std::cin >> rows >> cols >> q) || rows < 1 || rows > 1000 || cols < 1 ||
      cols > 1000 || q < 0 || q > 100000)
    return 1;
  std::vector<std::vector<long long>> p(rows + 1,
                                        std::vector<long long>(cols + 1, 0));
  for (int r = 0; r < rows; ++r)
    for (int c = 0; c < cols; ++c) {
      long long x;
      if (!(std::cin >> x) || x < -1000000000LL || x > 1000000000LL)
        return 1;
      p[r + 1][c + 1] = x + p[r][c + 1] + p[r + 1][c] - p[r][c];
    }
  for (int i = 0; i < q; ++i) {
    int r1, c1, r2, c2;
    if (!(std::cin >> r1 >> c1 >> r2 >> c2) || r1 < 0 || r1 > r2 || r2 > rows ||
        c1 < 0 || c1 > c2 || c2 > cols)
      return 1;
    std::cout << p[r2][c2] - p[r1][c2] - p[r2][c1] + p[r1][c1] << '\n';
  }
}
