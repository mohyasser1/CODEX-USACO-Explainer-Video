// n intervals start end, 0<=start<end<=10^9, n<=200000.
// Choose maximum number of nonoverlapping half-open intervals; print count/IDs.
#include <algorithm>
#include <iostream>
#include <tuple>
#include <vector>
int main() {
  int n;
  if (!(std::cin >> n) || n < 0 || n > 200000)
    return 1;
  std::vector<std::tuple<int, int, int>> events;
  for (int i = 0; i < n; ++i) {
    int start, end;
    if (!(std::cin >> start >> end) || start < 0 || start >= end ||
        end > 1000000000)
      return 1;
    events.push_back({end, start, i});
  }
  std::sort(events.begin(), events.end());
  int previous_end = -1;
  std::vector<int> chosen;
  for (auto [end, start, id] : events)
    if (start >= previous_end) {
      chosen.push_back(id);
      previous_end = end;
    }
  std::cout << chosen.size() << '\n';
  for (int i = 0; i < static_cast<int>(chosen.size()); ++i)
    std::cout << (i ? " " : "") << chosen[i];
  std::cout << '\n';
}
