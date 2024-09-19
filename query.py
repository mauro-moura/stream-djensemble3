import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('output/query-results/best_of_all/Q5-2015-best_of_all.db')
cursor = conn.cursor()

# Define the SQL query
#sql_query = """
#SELECT t.iteration, t.configuration, t.window, t.error
#FROM exp t
#JOIN (
#    SELECT iteration, window, MIN(error) AS min_error
#    FROM exp
#    GROUP BY iteration, window
#) sub
#ON t.iteration = sub.iteration AND t.window = sub.window AND t.error = sub.min_error;
#"""

#sql_query = """
#    SELECT iteration, window, MIN(error) AS min_error
#    FROM exp
#    GROUP BY iteration, window
#"""


sql_query = """
SELECT configuration, AVG(error) as avg_error from exp
GROUP BY configuration
"""

#sql_query = """
# SELECT t.configuration, min(t.avg_error) from( SELECT configuration, AVG(error) as avg_error from exp
# GROUP BY configuration) t
#"""

# Execute the query
cursor.execute(sql_query)

# Fetch all rows
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the connection
conn.close()



# For best of all
# conn = sqlite3.connect('output/best_of_all/Q7-2015-best_of_all.db')
# cursor = conn.cursor()

# sql_query = """
# SELECT t.configuration, min(t.avg_error) from( SELECT configuration, AVG(error) as avg_error from exp
# GROUP BY configuration) t
# """

#average dbs
#SELECT iteration, configuration, AVG(error) from exp
