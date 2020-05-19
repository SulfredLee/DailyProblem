#include <iostream>
#include <vector>
#include "RM_Array.h"
#include "RM_Heap.h"

using namespace std;

void TryHeap()
{
    vector<int> ivec = {0,1,2,3,4,8,9,3,5};

    RM::MakeHeap(ivec.begin(), ivec.end());
    for (size_t i = 0; i < ivec.size(); ++i)
        cout << ivec[i] << " ";
    cout << endl;

    ivec.push_back(7);
    cout << distance(ivec.begin(), ivec.end()) << " " << distance(ivec.begin(), prev(ivec.end())) << endl;
    RM::PushHeap(ivec.begin(), ivec.end());
    for (size_t i = 0; i < ivec.size(); ++i)
        cout << ivec[i] << " ";
    cout << endl;

    RM::PopHeap(ivec.begin(), ivec.end());
    cout << ivec.back() << endl;
    ivec.pop_back();

    for (size_t i = 0; i < ivec.size(); ++i)
        cout << ivec[i] << " ";
    cout << endl;

    RM::SortHeap(ivec.begin(), ivec.end());
    for (size_t i = 0; i < ivec.size(); ++i)
        cout << ivec[i] << " ";
    cout << endl;
}
int main(int argc, char *argv[])
{
    RM_Array<int> numbers(10);
    std::cout << numbers.GetSize() << std::endl;
    numbers.Clear();

    TryHeap();

    return 0;
}
