content_st = """
#include "{{ project_name }}_Test.h"

TEST_F({{ project_name }}_Test, Test001)
{
    EXPECT_EQ(true, true);
}
"""
