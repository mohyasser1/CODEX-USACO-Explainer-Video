// Fixed small values keep arithmetic within int's range.
#include <iostream>
int increment_copy(int value) {
  ++value;
  return value;
}
void increment_reference(int &value) { ++value; }
int main() {
  int x = 7;
  increment_copy(x);      // The returned 8 is deliberately ignored here.
  std::cout << x << '\n'; // 7: the caller's x was not changed.
  x = increment_copy(x);
  std::cout << x << '\n'; // 8: this assignment changes x.
  increment_reference(x);
  std::cout << x << '\n'; // 9: the reference aliases x.
}
