#include <iostream>

int main()
{
    std::cout << "Hello, test!";

#ifdef _DEBUG
    std::cout << " [Debug]";
#else
    std::cout << " [Release]";
#endif

    std::cout << std::endl;

    return 0;
}
