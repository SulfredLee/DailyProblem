#include "TestCommonTools.h"
#include "StdClassWithThread.h"
#include "StdCond.h"

TEST_F(TestCommonTools, ClassWithThreadTest)
{
    StdClassWithThread cc;
    EXPECT_EQ(true, cc.InitComponent());
    EXPECT_EQ("Reach Here", "Reach Here");
}
