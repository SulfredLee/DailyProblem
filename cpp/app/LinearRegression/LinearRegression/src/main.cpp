#include <iostream>
#include <iomanip>
#include <string>
#include "FunLinearRegression.h"

int main(int argc, char* argv[])
{
    std::string dataFile = "./dataFile.csv";
    FunLinearRegression helper;
    helper.InitComponent(dataFile);
    helper.Train();

    // p1 is intersection
    // p2 is slope
    double p1, p2, p2Degree;
    helper.GetModel(p1, p2, p2Degree);
    std::cout << "Model p1: " << p1 << " p2: " << p2 << " p2Degree: " << p2Degree << std::endl;

    return 0;
}
