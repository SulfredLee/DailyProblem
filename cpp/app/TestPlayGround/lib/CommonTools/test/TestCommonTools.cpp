#include "TestCommonTools.h"
#include "StdClassWithThread.h"
#include "StdCond.h"
#include "CountTimer.h"

/*
EXPECT_EQ(val1,val2);, val1 == val2
EXPECT_NE(val1,val2);, val1 != val2
EXPECT_LT(val1,val2);, val1 < val2
EXPECT_LE(val1,val2);, val1 <= val2
EXPECT_GT(val1,val2);, val1 > val2
EXPECT_GE(val1,val2);, val1 >= val2
*/

using namespace std::chrono_literals;

TEST_F(TestCommonTools, ClassWithThread_Create_Test)
{
    {
        StdClassWithThread cc;
        EXPECT_EQ(true, cc.InitComponent());
    }
    EXPECT_EQ("Reach Here", "Reach Here");
}

TEST_F(TestCommonTools, StdCond_WaitWithTime_Test)
{
    StdCond cond;
    CountTimer timer;

    timer.Start();
    cond.WaitWithTime(10);
    timer.Stop();
    EXPECT_LE(0.01, timer.GetSecondDouble());
}

TEST_F(TestCommonTools, StdCond_WaitAndSignal_Test)
{
    StdCond cond;
    CountTimer timer;

    timer.Start();
    std::thread tt([&]
                   {
                       std::this_thread::sleep_for(10ms);
                       cond.Signal();
                   });
    tt.detach();

    cond.Wait();
    timer.Stop();
    EXPECT_LE(0.01, timer.GetSecondDouble());
}

TEST_F(TestCommonTools, CountTimer_SimpleSleep_Test)
{
    CountTimer timer;

    timer.Start();
    std::this_thread::sleep_for(10ms);
    timer.Stop();
    EXPECT_LE(0.01, timer.GetSecondDouble());
}

TEST_F(TestCommonTools, CountTimer_MovingSleep_Test)
{
    CountTimer timer;

    timer.Start();
    for (int i = 0; i < 10; i++)
    {
        std::this_thread::sleep_for(10ms);
        timer.MovingStop();
        EXPECT_LE(0.01 * (i + 1), timer.GetSecondDouble()); // the time is accumulated
    }
}
