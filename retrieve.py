import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
  my_secret = os.environ['DATABASE']
)
# Create a cursor
cur = conn.cursor()

# Step 2: Query the "whatsapp_chats" table to retrieve all records
query = "SELECT * FROM whatsapp_chats"  # Modify this query if you need to retrieve specific records
cur.execute(query)

# Step 3: Fetch all rows
rows = cur.fetchall()

# Step 4: Process and display the retrieved data
for row in rows:
    id, timestamp, sender, message = row
    print(f"ID: {id}, Timestamp: {timestamp}, Sender: {sender}, Message: {message}")

# Step 5: Close the cursor and connection
cur.close()
conn.close()