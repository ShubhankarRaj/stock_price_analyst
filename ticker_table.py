from sql_connector import SqlConnection

connection = SqlConnection().get_sql_connection()
my_cursor = connection.cursor()

#Create list (array) of records
records_list = ('Tim','Tim@tim.com',32)
mike_placeholders="INSERT INTO users (name,email,age) VALUES (%s, %s, %s) "
print(type(records_list))
my_cursor.execute(mike_placeholders,records_list)
#Commit the connection to make the change on the database
connection.commit()