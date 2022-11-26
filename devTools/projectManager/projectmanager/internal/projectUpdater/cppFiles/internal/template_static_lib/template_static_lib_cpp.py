content_st = """
#include "{{ module_name }}.h"

{{ module_name }}::{{ module_name }}()
{
}

{{ module_name }}::~{{ module_name }}()
{
}

double {{ module_name }}::GetLength(const double& xx)
{
    return 10;
}

"""
