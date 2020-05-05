#include <iostream>

class Solution
{
public:
    // 2.1.1 Remove Duplicates from Sorted Array
    int removeDuplicates(int A[], int n)
    {
        if (n <= 1) return 0;

        int index = 0;
        for (int i = 1; i < n; i++)
        {
            if (A[index] != A[i])
                A[++index] = A[i];
        }

        return index + 1;
    }
    // 2.1.2 Remove Duplicates from Sorted Array II
    int removeDuplicates2(int A[], int n, int d)
    {
        if (n <= d) return 0;

        int index = d;
        for (int i = d; i < n; i++)
        {
            if (A[index - d] != A[i])
                A[index++] = A[i];
        }

        return index + 1;
    }
};

int main(int argc, char *argv[])
{
    Solution solution;
    {
        int A[3] = {1, 1, 2};
        std::cout << "2.1.1: " << solution.removeDuplicates(A, sizeof(A)/sizeof(int)) << std::endl;
    }
    {
        int A[6] {1, 1, 1, 2, 2, 3};
        std::cout << "2.1.2: " << solution.removeDuplicates2(A, sizeof(A)/sizeof(int), 2) << std::endl;
    }

    return 0;
}
