#include <iostream>
#include <vector>
int main() {
  int n;
  if (!(std::cin >> n) || n < 0 || n > 100000)
    return 1;
  std::vector<int> a(n);
  for (int &x : a)
    if (!(std::cin >> x) || x < -1000000000 || x > 1000000000)
      return 1;
  long long total = 0;
  for (int i = 0; i < n; ++i) {
    total += a[i];
  }
  std::cout << total << '\n';
}
