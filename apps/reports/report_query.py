DAILY_SALES_QUERY = """
    SELECT DATE(created), item, SUM(quantity) as "Amount Sold", SUM(amount) AS "Total Sales" FROM reports_salesreport
    GROUP BY item
    HAVING sold_or_spoiled = 'Sold'
"""