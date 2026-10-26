// Complete runnable counterpart of the hook sample.
#include <iostream>
int main() {
  std::cout << std::boolalpha;
  bool lamp = false;
  std::cout << "start: " << lamp << '\n';
  for (int i = 1; i <= 3; ++i) {
    lamp = !lamp;
    std::cout << "toggle " << i << ": " << lamp << '\n';
  }
  lamp = false;
  for (int i = 1; i <= 3; ++i) {
    lamp = true;
    std::cout << "assign " << i << ": " << lamp << '\n';
  }
}
