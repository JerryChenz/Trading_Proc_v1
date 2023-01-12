Investment Management
=========================
Public equity Investment Management tool for potential opportunities and current holdings.

Feature
=========================
1. Stock screener
   - To screen stock based on more powerful and flexible custom criteria;
   - Unique custom screening criteria using custom variables
   - Ex: EV = capitalization_report + total_debt + MinorityInterest - CashAndCashEquivalents - total_nonop_assets * 0.5

2. Stock model management
   - To automate the boring tasks of getting information in the company financial statements and market price information;
   - To manage and update all the financial models;

3. Opportunities and current holdings Monitor
   - To visualizes and compare all the investments opportunities (including cross-assets comparison);
   - To visualizes and monitors the current holdings given key marco-economic risk factors including central bank rates and inflation data;

Stock idea Generation and Analysis Methodology
=========================
1. Use Custom Screening tool to narrow down the search to ~100 stocks and sorted by specific parameter
2. Use Financial model to analyze the stock Individually and find <50 stocks
3. Use Monitor to track and act on the opportunities
![](https://github.com/JerryChenz/InvestmentManagementOpen/blob/main/screenshoots/idea_funnel_1.PNG)

Workflow
=========================
![](https://github.com/JerryChenz/InvestmentManagementOpen/blob/main/screenshoots/Investment_Analysis_Workflow.jpg)

Preview
=========================
1. Stock screener
![](https://github.com/JerryChenz/InvestmentManagementOpen/blob/main/screenshoots/Screenshot_screener_1.PNG)
![](https://github.com/JerryChenz/InvestmentManagementOpen/blob/main/screenshoots/Screenshot_screener_2.PNG)
2. Stock model management
![](https://github.com/JerryChenz/InvestmentManagementOpen/blob/main/screenshoots/ModelManagement_1.PNG)
3. Opportunities monitor
![](https://github.com/JerryChenz/InvestmentManagementOpen/blob/main/screenshoots/Monitor_1.PNG)

Data sources
=========================
- Yahoo finance (yfinance)
- SEC API (WIP)
- Bloomberg API (WIP)
- Wind (WIP)

Installation
=========================
TBA

Roadmap
=========================
- [x] **Preview Version**  2023-01-05
    - Stock Screener available for use

Possible extensions for multi-assets management
=========================
Public:
- Bonds
- REITs
Private:
- Private equity
- Private credit
- Real estate
