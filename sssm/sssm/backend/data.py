COLLECTIONS = set(["stocks", "transactions", "traders",
                   "portfolio", "shares_trading"]) # 

SYMBOLS = set(["TEA", "POP", "ALE", "GIN", "JOE"])

STOCKS = {
    "TEA":
    {"Symbol": "TEA", "Type": "Common",
     "Last_Dividend": 0, "Fixed_Dividend": "NA",
     "Par_Value": 100, "Price": -1.0
    },
    "POP": 
    {"Symbol": "POP", "Type": "Common",
     "Last_Dividend": 8, "Fixed_Dividend": "NA",
     "Par_Value": 100, "Price": -1.0
    },
    "ALE": 
    {"Symbol": "ALE", "Type": "Common",
     "Last_Dividend": 23, "Fixed_Dividend": "NA",
     "Par_Value": 60, "Price": -1.0
    },
    "GIN":                 
    {"Symbol": "GIN", "Type": "Preferred",
     "Last_Dividend": 8, "Fixed_Dividend": 2,
     "Par_Value": 100, "Price": -1.0
    }, 
    "JOE":                 
    {"Symbol": "JOE", "Type": "Common",
     "Last_Dividend": 14, "Fixed_Dividend": 2,
     "Par_Value": 250, "Price": -1.0
    } 
}

SHARES_TRADING = {
    "TEA": 12000000,
    "POP": 10000000,
    "ALE": 9000000,
    "GIN": 8000000,
    "JOE": 6000000
}