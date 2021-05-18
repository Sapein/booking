# Formats

## Journal Format (.jnl/.journal)
```
JOURNAL_NAME - ABBREVIATION
Page PAGE_NUMBER

JOURNAL_REFERENCE DATE ACCOUNT (Cr/Dr) AMOUNT CURRENCY (Pr:POST_REF, Description:DESC)
```

### Journal Reference
```
JOURNAL_ABBREVIATION-PAGE_NUMBER-TRANASCTION_ID
```

### Chart of Accounts (.chart/cht)
```
MAJOR_TYPE (RANGE):
    Account Name: ACCOUNT_NAME
    Account Number: ACCOUNT_ID
    File: FILENAME
    Descroption: DESC
```

### Account Format (.acc/.accrual | .csh/.cash)
```
ACCOUNT_ID NAME
BASIS Basis
MAJOR_TYPE - (Cr/Dr) Normal

JOURNAL_REFERENCE DATE (Cr/Dr) AMOUNT CURRENCY (DESCRIPTION)
````
