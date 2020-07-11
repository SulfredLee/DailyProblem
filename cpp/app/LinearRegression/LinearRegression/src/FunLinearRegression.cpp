#include "FunLinearRegression.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include "Tools.h"
#include <algorithm>
#include <math.h> // tan
#include <limits>

FunLinearRegression::FunLinearRegression()
{
}

FunLinearRegression::~FunLinearRegression()
{
}

bool FunLinearRegression::InitComponent(std::string dataFile)
{
    m_dataFile = dataFile;

    ReadData(m_dataFile);

    return true;
}

bool FunLinearRegression::Train()
{
    // get min max from y_lo y_hi
    int minY = std::min(*std::min_element(m_yLo.begin(), m_yLo.end()), *std::min_element(m_yHi.begin(), m_yHi.end()));
    int maxY = std::max(*std::max_element(m_yLo.begin(), m_yLo.end()), *std::max_element(m_yHi.begin(), m_yHi.end()));
    std::cout << "minY: " << minY << " maxY: " << maxY << std::endl;

    // add buffer
    minY -= 50;
    maxY += 50;
    std::cout << "minY: " << minY << " maxY: " << maxY << std::endl;

    double minCost = TrainCore(minY, maxY, 0.01, -89, 89, 0.01, std::numeric_limits<double>::max());
    // TrainCore(m_p1-5, m_p1+5, 0.01, m_p2Degree-5, m_p2Degree+5, 0.01, minCost);

    // rounding
    m_p1 = (int)((m_p1 * 100) + 0.5) / 100.0;
    m_p2 = (int)((m_p2 * 100) + 0.5) / 100.0;

    return true;
}

void FunLinearRegression::GetModel(double& p1, double& p2, double& degree)
{
    p1 = m_p1;
    p2 = m_p2;
    degree = m_p2Degree;
}

double FunLinearRegression::Predict(int x)
{
    return m_p1 + m_p2 * x;
}

void FunLinearRegression::ReadData(const std::string& dataFile)
{
    std::cout << "Going to read file: " << dataFile << std::endl;

    const char delim = 0x0D;
    int N = CountLine(dataFile, delim);

    m_x.clear(); m_x.reserve(N-1);
    m_yLo.clear(); m_yLo.reserve(N-1);
    m_yHi.clear(); m_yHi.reserve(N-1);

    std::ifstream FH(dataFile);
    std::string line;
    std::getline(FH, line, delim);
    while (std::getline(FH, line, delim))
    {
        std::vector<std::string> parts = Utility::SplitString(line, ',');
        m_x.push_back(stoi(parts[1]));
        m_yLo.push_back(stoi(parts[2]));
        m_yHi.push_back(stoi(parts[3]));
    }

    std::cout << "N: " << N << " m_x.size(): " << m_x.size() << std::endl;
}

int FunLinearRegression::CountLine(const std::string& dataFile, const char delim)
{
    std::ifstream FH(dataFile);
    std::string line;
    int count = 0;
    std::getline(FH, line, delim);
    while (std::getline(FH, line, delim))
    {
        count++;
    }
    return count;
}

double FunLinearRegression::GetCost(const double& p1, const double& p2)
{
    double result = 0;
    for (size_t i = 0; i < m_x.size(); i++)
    {
        double curPredict = p1 + p2 * m_x[i];
        if (curPredict > m_yHi[i])
            result += curPredict - m_yHi[i];
        else if (curPredict < m_yLo[i])
            result += m_yLo[i] - curPredict;
    }

    return result / m_x.size();
}

double FunLinearRegression::TrainCore(double p1Start, double p1End, double p1Step, double p2DStart, double p2DEnd, double p2Step, double minCost)
{
    if (p2DStart < -89) p2DStart = -89;
    if (p2DEnd > 89) p2DEnd = 89;

    const double PI = 3.14159265;
    for (double p1 = p1Start; p1 <= p1End; p1+=p1Step)
    {
        for (double degree = p2DStart; degree <= p2DEnd; degree+=p2Step)
        {
            double p2 = tan(degree * PI / 180.0);
            double curCost = GetCost(p1, p2);
            if (curCost < minCost)
            {
                minCost = curCost;
                m_p1 = p1;
                m_p2 = p2;
                m_p2Degree = degree;
                std::cout << "Updated p1: " << p1 << " degree: " << degree << " minCost: " << minCost << std::endl;
            }
        }
    }
    return minCost;
}
