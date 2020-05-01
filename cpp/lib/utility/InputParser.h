#ifndef INPUTPARSER_H
#define INPUTPARSER_H
#include <vector>
#include <string>
#include <unordered_map>

class InputParser
{
 public:
    InputParser();
    ~InputParser();

    const std::string operator[] (const std::string& option) const;
    bool DoParse(const int& argc, char ** argv, bool isPrintUsage = false);
    void AddOption(const std::string& shortForm, const std::string& longForm, bool isRequired = false, const std::string& defaultValue = "");
 private:
    std::string GetLongForm(const std::string& inOption) const;
    bool IsOptionsExists();
    bool IsOptionExists(const std::string& longForm);
    void PrintOptionList();
 private:
    std::unordered_map<std::string, std::string> m_short2Long; // key: shortForm option, value: longForm option
    std::unordered_map<std::string, bool> m_isRequired; // key: longForm option
    std::unordered_map<std::string, std::string> m_defaultValue; // key: longForm option, value: defaultValue
    std::unordered_map<std::string, std::string> m_options; // key: longForm option, value: option content
};
#endif
