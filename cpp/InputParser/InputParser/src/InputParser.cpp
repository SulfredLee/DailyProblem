#include "InputParser.h"

#include <algorithm>
#include <iostream>
#include <sstream>

InputParser::InputParser()
{
}

InputParser::~InputParser()
{
}

const std::string InputParser::operator[] (const std::string& option) const
{
    auto it = m_options.find(GetLongForm(option));
    if (it == m_options.end())
        return std::string("");
    else
        return it->second; // return option
}

bool InputParser::DoParse(const int& argc, char ** argv, bool isPrintUsage)
{
    m_options.clear();
    m_options = m_defaultValue;

    for (int i = 1; i < argc; i += 2)
    {
        if (i + 1 < argc)
        {
            std::string longForm = GetLongForm(argv[i]);
            if (longForm == "") continue;
            m_options.insert(std::make_pair(longForm, argv[i+1]));
        }
    }

    if (IsOptionsExists())
        return true;
    else
    {
        if (isPrintUsage)
            PrintOptionList();
        return false;
    }
}

void InputParser::AddOption(const std::string& shortForm, const std::string& longForm, bool isRequired, const std::string& defaultValue)
{
    m_short2Long.insert(std::make_pair(shortForm, longForm));
    m_isRequired.insert(std::make_pair(longForm, isRequired));
    if (!isRequired && defaultValue != "")
        m_defaultValue.insert(std::make_pair(longForm, defaultValue));
}

std::string InputParser::GetLongForm(const std::string& inOption) const
{
    if (inOption.length() > 2 && inOption[0] == '-' && inOption[1] == '-')
    {
        return inOption.substr(2);
    }
    else if (inOption.length() > 1 && inOption[0] == '-')
    {
        std::string shortForm = inOption.substr(1);
        auto it = m_short2Long.find(shortForm);
        if (it == m_short2Long.end())
            return std::string("");
        else
            return it->second; // return longForm
    }
    else
    {
        std::string shortForm = inOption;
        auto it = m_short2Long.find(shortForm);
        if (it == m_short2Long.end())
            return inOption;
        else
            return it->second; // return longForm
    }
}

bool InputParser::IsOptionsExists()
{
    for (auto& it : m_isRequired)
    {
        const std::string& longForm = it.first;
        const bool& isRequired = it.second;
        if (isRequired)
        {
            if (!IsOptionExists(longForm))
            {
                std::cout << "ERR: Option is needed --" << longForm << std::endl;
                return false;
            }
        }
    }
    return true;
}

bool InputParser::IsOptionExists(const std::string& longForm)
{
    auto it = m_options.find(longForm);
    if (it == m_options.end())
        return false;
    else
        return true;
}

void InputParser::PrintOptionList()
{
    std::stringstream ss;
    ss << "Usage: YourApp";
    for (auto it : m_short2Long)
    {
        ss << " [-" << it.first << "|--" << it.second << "] " << "<" << it.second << ">" << std::endl;
    }
    std::cout << "ERR: " << ss.str();
}
