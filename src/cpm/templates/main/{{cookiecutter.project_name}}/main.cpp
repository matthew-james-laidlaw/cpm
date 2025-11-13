#include <iostream>

int main()
{
    std::cout << "Hello, {{ cookiecutter.project_name }}!";

#ifdef _DEBUG
    std::cout << " [Debug]";
#else
    std::cout << " [Release]";
#endif

    std::cout << std::endl;

    return 0;
}
