#include <iostream>
#include <algorithm>
#include <sstream>
#include <string>
#include <vector>
#include <stack>
#include <climits>

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) { }
};
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
    // 3.12 Count and Say
    std::string countAndSay(int n)
    {
        std::string s("1");

        while (--n)
            s = getNext(s);

        return s;
    }
    std::string getNext(const std::string &s)
    {
        std::stringstream ss;

        for (auto i = s.begin(); i != s.end(); )
        {
            auto j = std::find_if(i, s.end(), std::bind1st(std::not_equal_to<char>(), *i));
            ss << std::distance(i, j) << *i;
            i = j;
        }

        return ss.str();
    }
    // 4.1.3 Largest Rectangle in Histogram
    int largestRectangleArea(std::vector<int> &height) {
        std::stack<int> s;
        height.push_back(0);
        int result = 0;
        for (size_t i = 0; i < height.size(); ) {
            if (s.empty() || height[i] > height[s.top()])
                s.push(i++);
            else {
                int tmp = s.top();
                s.pop();
                result = std::max(result,
                                  (int)(height[tmp] * (s.empty() ? i : i - s.top() - 1)));
                std::cout << "result: " << result << std::endl;
            }
        }
        return result;
    }
    // 2.2.5 Remove Duplicates from Sorted List II
    ListNode *deleteDuplicates(ListNode *head)
    {
        ListNode dummy(INT_MIN); dummy.next = head;
        ListNode *prev = &dummy;
        ListNode *cur = head;
        ListNode *next = cur != nullptr ? cur->next : nullptr;

        while (next != nullptr)
        {
            bool duplicated = false;
            while (next && cur->val == next->val)
            {
                duplicated = true;
                prev->next = next;
                delete cur;
                cur = next;
                next = cur != nullptr ? cur->next : nullptr;
            }
            if (duplicated)
            {
                prev->next = next;
                delete cur;
            }
            else
                prev = cur;
            cur = next;
            next = cur != nullptr ? cur->next : nullptr;
        }
        return dummy.next;
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
    std::cout << "3.12: " << solution.countAndSay(10) << std::endl;
    std::vector<int> vv = {5, 6, 5, 2, 3};
    std::cout << "4.1.3: " << solution.largestRectangleArea(vv);
    {
        ListNode dummy(0);
        ListNode *p = &dummy;
        int A[7] = {1, 2, 3, 3, 4, 4, 5};
        for (int i = 0; i < 7; i++)
        {
            ListNode *cur = new ListNode(A[i]);
            p->next = cur;
            p = cur;
        }
        p->next = nullptr;
        solution.deleteDuplicates(dummy.next);
    }

    return 0;
}
