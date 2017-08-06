# Super Simple Stocks
Super Simple Stock Market and Trading Platform

## Version
Version 1

# Setup Environment
## Python 2.7+ and 3+

## Installation and Unit Tests
1. Clone this repository
2. Change to the project root folder
3. Install dependencies: ``pip install -r requirements.txt``
4. Run ``pytest``
5. Outcome: All tests should be passing

## Installation & App Setup
Installation steps:
1. Change to sssm/ directory
2. Execute ``python api.py``

See execution examples below:

Please note: Starting the SSSM as a service (as advised above using ``python api.py``) simulates around 30mins of trade.
So all operations should be available.

####Permitted Operations 
Note: Run after starting application as a service (see above).

1. Compute dividend yield & PEratio
    Examples: http://<baseurl>/stock/ALE?operation=dividend&price=12
              http://<baseurl>/stock/JOE?operation=peratio&price=14

2. Compute Weighted Volume

    GET /platform/volume_weighted_stock_price?interval=[interval (in mins, default 15)]
        
3. Compute All Share Index

    GET /platform/index
    
    Example call: http://<baseurl>/platform/index
    
4. Weighted Volume and All Share index

    GET /platform
    
    Example call : http://<baseurl>/platform

5. Trade: Endpoint not implemented in API service

6. User creation: Endpoint not implemented in API service
