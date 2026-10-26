// Two integers, each in [-10^9,10^9]. Print their sum.
#include <iostream>
int main() {
    long long a,b;
    if (!(std::cin>>a>>b)) return 1;
    if (a < -1000000000LL || a > 1000000000LL || b < -1000000000LL || b > 1000000000LL) return 1;
    std::cout<<a+b<<'\n';
}
