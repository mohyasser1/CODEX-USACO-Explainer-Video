// n target, then n signed values; count subsets of indices summing to target.
// n <= 20, |value| <= 10^9, |target| <= 2*10^10. Includes the empty subset.
#include <iostream>
#include <vector>
long long count_subsets(const std::vector<long long> &a, int i, long long sum,
                        long long target) {
  if (i == static_cast<int>(a.size()))
    return sum == target;
  // Exclude and include the current index. No unsafe sum>target pruning.
  return count_subsets(a, i + 1, sum, target) +
         count_subsets(a, i + 1, sum + a[i], target);
}
int main() {
  int n;
  long long target;
  if (!(std::cin >> n >> target) || n < 0 || n > 20 ||
      target < -20000000000LL || target > 20000000000LL)
    return 1;
  std::vector<long long> a(n);
  for (auto &x : a)
    if (!(std::cin >> x) || x < -1000000000LL || x > 1000000000LL)
      return 1;
  std::cout << count_subsets(a, 0, 0, target) << '\n';
}
