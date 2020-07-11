#ifndef FUN_LINEAR_REGRESSION_H
#define FUN_LINEAR_REGRESSION_H
#include <string>
#include <vector>

class FunLinearRegression
{
 public:
    FunLinearRegression();
    ~FunLinearRegression();

    bool InitComponent(std::string dataFile);
    bool Train();
    void GetModel(double& p1, double& p2, double& degree);
    double Predict(int x);
 private:
    void ReadData(const std::string& dataFile);
    int CountLine(const std::string& dataFile, const char delim);
    double GetCost(const double& p1, const double& p2);
    double TrainCore(double p1Start, double p1End, double p1Step, double p2Start, double p2End, double p2Step, double minCost);
 private:
    std::vector<int> m_x;
    std::vector<int> m_yLo;
    std::vector<int> m_yHi;
    std::string m_dataFile;

    // model
    double m_p1;
    double m_p2;
    double m_p2Degree;
};

#endif
