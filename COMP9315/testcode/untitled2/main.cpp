#include <iostream>
#include <vector>

int main() {
    std::vector<int> v;

    v.resize(10);
    v.at(2) = 1;
    v[5] = 2;
    v.push_back(3);
    std::cout << "size: " << v.size() << std::endl;

    for (std::vector<int>::iterator it = v.begin(); it != v.end(); it++) {
        std::cout << *it << std::endl;
        std::cout<<'\007';
    }
}