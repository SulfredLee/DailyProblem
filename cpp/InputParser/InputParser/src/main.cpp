#include <iostream>
#include "InputParser.h"

// Usage: ./InputParser --input abc.txt
// Usage: ./InputParser
int main(int argc, char *argv[])
{
    InputParser parser;
    parser.AddOption("i", "input", true); // required value example
    parser.AddOption("n", "number", false, "20"); // default value example
    parser.AddOption("o", "output"); // optional value example
    if (!parser.DoParse(argc, argv, true))
    {
        std::cout << "ERR not enough arguments" << std::endl;
        return 1;
    }

    std::cout << "input: " << parser["i"] << std::endl;
    std::cout << "number: " << std::stoi(parser["n"]) << std::endl;
    std::cout << "output: " << parser["o"] << std::endl;
    return 0;
}
