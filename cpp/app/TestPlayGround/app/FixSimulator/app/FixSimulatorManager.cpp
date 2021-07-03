#include "FixSimulatorManager.h"

FixSimulatorManager::FixSimulatorManager()
{
}

FixSimulatorManager::~FixSimulatorManager()
{
}

bool FixSimulatorManager::InitComponent()
{
    return true;
}

// override Fix::Application
void FixSimulatorManager::onCreate( const FIX::SessionID& )
{

}

// override Fix::Application
void FixSimulatorManager::onLogon( const FIX::SessionID& )
{

}

// override Fix::Application
void FixSimulatorManager::onLogout( const FIX::SessionID& )
{

}

// override Fix::Application
void FixSimulatorManager::toAdmin( FIX::Message&, const FIX::SessionID& )
{

}
// override Fix::Application
void FixSimulatorManager::toApp( FIX::Message&, const FIX::SessionID& )
    noexcept(false)
// throw ( FIX::DoNotSend )
{

}

// override Fix::Application
void FixSimulatorManager::fromAdmin( const FIX::Message&, const FIX::SessionID& )
    noexcept(false)
// throw ( FIX::FieldNotFound, FIX::IncorrectDataFormat, FIX::IncorrectTagValue, FIX::RejectLogon )
{

}

// override Fix::Application
void FixSimulatorManager::fromApp( const FIX::Message&, const FIX::SessionID& )
    noexcept(false)
// throw ( FIX::FieldNotFound, FIX::IncorrectDataFormat, FIX::IncorrectTagValue, FIX::UnsupportedMessageType )
{

}
