#include <iostream>
#include <algorithm>
#include <sstream>
#include <string>
#include <vector>
#include <stack>
#include <climits>
#include <unordered_set>
#include <unordered_map>
#include <list>
#include <set>

using namespace std;

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
    vector<string> wordBreak(string s, unordered_set<string>& dict)
    {
        vector<string> result;
        if (s.size() == 0) return result;

        vector<vector<int> > f(s.size(), vector<int>(s.size(), -1));
        for (size_t l = 1; l <= s.size(); l++)
        {
            for (size_t i = 0; i < s.size() - l + 1; i++)
            {
                size_t j = i + l - 1;
                string temp = s.substr(i, l);
                if (dict.find(s.substr(i, l)) != dict.end())
                {
                    f[i][j] = i;
                }
                else
                {
                    for (size_t k = i; k < j; k++)
                    {
                        if (f[i][k] != -1 && f[k+1][j] != -1)
                        {
                            f[i][j] = k + 1;
                            break;
                        }
                    }
                }
            }
        }

        if (f[0][s.size() - 1] == -1) return result;

        int i = 0; int j = s.size() - 1;
        while (i < j)
        {
            int k = f[i][j];
            if (i == k)
            {
                result.push_back(s.substr(i, j - i + 1));
                break;
            }
            result.push_back(s.substr(i, k - i));
            i = k;
        }
        return result;
    }
public:
    int networkDelayTime(vector<vector<int>>& times, int endPoint, int startPoint)
    {
        unordered_map<int, list<GraphNode> > graph = BuildGraph(times); // key: startNode value: neighbours
        // PrintGraph(graph);
        vector<int> distCache(endPoint, INT_MAX); distCache[startPoint - 1] = 0;
        set<pair<int, int> > queue; // pair first: node number, pair second: cost

        queue.insert(make_pair(startPoint, 0));
        while (!queue.empty())
        {
            pair<int, int> curNode = *queue.begin();
            queue.erase(queue.begin());

            const auto& it = graph.find(curNode.first);
            if (it == graph.end()) continue;

            for (const GraphNode& neighbour : it->second)
            {
                int curDist = distCache[curNode.first - 1] + neighbour.m_weight;
                if (distCache[neighbour.m_nodeNumber - 1] > curDist)
                {
                    const auto& qIT = queue.find(make_pair(neighbour.m_nodeNumber, neighbour.m_weight));
                    if (qIT != queue.end())
                        queue.erase(qIT);

                    distCache[neighbour.m_nodeNumber - 1] = curDist;
                    queue.insert(make_pair(neighbour.m_nodeNumber, neighbour.m_weight));
                }
            }
        }
        // return result
        // PrintDistCache(distCache);
        return distCache[endPoint - 1];
    }
private:
    struct GraphNode
    {
        int m_nodeNumber;
        int m_weight;

        GraphNode(int to, int weight)
            : m_nodeNumber(to), m_weight(weight)
        {
        }
    };
    unordered_map<int, list<GraphNode> > BuildGraph(const vector<vector<int> >& times)
    {
        unordered_map<int, list<GraphNode> > result;
        for (const auto& time : times)
        {
            int startNode = time[0];
            int endNode = time[1];
            int weight = time[2];

            auto it = result.find(startNode);
            if (it == result.end())
            {
                it = result.insert(it, make_pair(startNode, list<GraphNode>()));
            }
            it->second.push_back(GraphNode(endNode, weight));
        }

        return result;
    }
    void PrintDistCache(const vector<int>& distCache)
    {
        for (const auto& dist : distCache)
        {
            cout << dist << endl;
        }
    }
    void PrintGraph(const unordered_map<int, list<GraphNode> >& graph)
    {
        for (const auto& node : graph)
        {
            cout << node.first << " ---> ";
            for (const auto& naboNode : node.second)
            {
                cout << "(" << naboNode.m_nodeNumber << "," << naboNode.m_weight << "),";
            }
            cout << endl;
        }
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
    {
        cout << endl;
        unordered_set<string> dict;
        dict.insert("cat"); dict.insert("cats"); dict.insert("and"); dict.insert("sand"); dict.insert("dog");
        string words = "catsanddog";
        for (auto& w : solution.wordBreak(words, dict))
        {
            cout << w << " ";
        }
        cout << endl;
    }
    {
        vector<vector<int> > times = {{1,2,4},{1,8,8},{2,3,8},{2,8,11},{3,4,7},{3,9,2},{3,6,4},{4,5,9},{4,6,14},{5,6,10},{6,7,2},{7,8,1},{7,9,6},{8,9,7}};
        // vector<vector<int> > times = {{2,1,1}, {2,3,1}, {3,4,1}};
        cout << solution.networkDelayTime(times, 9, 1) << endl;
    }

    return 0;
}
