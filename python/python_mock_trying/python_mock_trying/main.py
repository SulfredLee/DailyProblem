from python_mock_trying.NewOfficeManager.FundManager import FundManager

def quick_fun(fund_manager: FundManager) -> str:
    fund_manager.add_member(10)
    fund_manager.tell_total_members()
    fund_manager.set_office_size(3)
    office_size: int = fund_manager.get_office_size()

    if fund_manager.tell_total_members() > office_size:
        return f"Not enough office size"
    else:
        return f"Enough office size"

def main():
    quick_fun(FundManager())

if __name__ == "__main__":
    main()
