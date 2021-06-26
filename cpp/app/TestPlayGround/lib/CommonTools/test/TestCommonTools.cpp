#include "TestCommonTools.h"
#include "StdClassWithThread.h"

TEST_F(TestCommonTools, TestInitClass)
{
    StdClassWithThread cc;
    EXPECT_EQ(true, cc.InitComponent());
}

