#ifndef FIX_SIMULATOR_MANAGER_H
#define FIX_SIMULATOR_MANAGER_H

#include "quickfix/Application.h"
#include "quickfix/MessageCracker.h"
#include "quickfix/Values.h"
#include "quickfix/Mutex.h"

#include "quickfix/fix40/NewOrderSingle.h"
#include "quickfix/fix40/ExecutionReport.h"
#include "quickfix/fix40/OrderCancelRequest.h"
#include "quickfix/fix40/OrderCancelReject.h"
#include "quickfix/fix40/OrderCancelReplaceRequest.h"

#include "quickfix/fix41/NewOrderSingle.h"
#include "quickfix/fix41/ExecutionReport.h"
#include "quickfix/fix41/OrderCancelRequest.h"
#include "quickfix/fix41/OrderCancelReject.h"
#include "quickfix/fix41/OrderCancelReplaceRequest.h"

#include "quickfix/fix42/NewOrderSingle.h"
#include "quickfix/fix42/ExecutionReport.h"
#include "quickfix/fix42/OrderCancelRequest.h"
#include "quickfix/fix42/OrderCancelReject.h"
#include "quickfix/fix42/OrderCancelReplaceRequest.h"

#include "quickfix/fix43/NewOrderSingle.h"
#include "quickfix/fix43/ExecutionReport.h"
#include "quickfix/fix43/OrderCancelRequest.h"
#include "quickfix/fix43/OrderCancelReject.h"
#include "quickfix/fix43/OrderCancelReplaceRequest.h"
#include "quickfix/fix43/MarketDataRequest.h"

#include "quickfix/fix44/NewOrderSingle.h"
#include "quickfix/fix44/ExecutionReport.h"
#include "quickfix/fix44/OrderCancelRequest.h"
#include "quickfix/fix44/OrderCancelReject.h"
#include "quickfix/fix44/OrderCancelReplaceRequest.h"
#include "quickfix/fix44/MarketDataRequest.h"

#include "quickfix/fix50/NewOrderSingle.h"
#include "quickfix/fix50/ExecutionReport.h"
#include "quickfix/fix50/OrderCancelRequest.h"
#include "quickfix/fix50/OrderCancelReject.h"
#include "quickfix/fix50/OrderCancelReplaceRequest.h"
#include "quickfix/fix50/MarketDataRequest.h"

#include <queue>

class FixSimulatorManager :
    public FIX::Application,
    public FIX::MessageCracker
{
 public:
    FixSimulatorManager();
    ~FixSimulatorManager();

    bool InitComponent();
 private:
    // override Fix::Application
    void onCreate( const FIX::SessionID& );
    // override Fix::Application
    void onLogon( const FIX::SessionID& );
    // override Fix::Application
    void onLogout( const FIX::SessionID& );
    // override Fix::Application
    void toAdmin( FIX::Message&, const FIX::SessionID& );
    // override Fix::Application
    void toApp( FIX::Message&, const FIX::SessionID& )
        noexcept(false);
    // throw ( FIX::DoNotSend );
    // override Fix::Application
    void fromAdmin( const FIX::Message&, const FIX::SessionID& )
        noexcept(false);
    // throw ( FIX::FieldNotFound, FIX::IncorrectDataFormat, FIX::IncorrectTagValue, FIX::RejectLogon );
    // override Fix::Application
    void fromApp( const FIX::Message&, const FIX::SessionID& )
        noexcept(false);
    // throw ( FIX::FieldNotFound, FIX::IncorrectDataFormat, FIX::IncorrectTagValue, FIX::UnsupportedMessageType );
};

#endif
