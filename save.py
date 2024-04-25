import psycopg2
import re
import os

# Connect to the PostgreSQL database
conn = psycopg2.connect(
  my_secret = os.environ['DATABASE']
)
# Create a cursor
cur = conn.cursor()

# Step 3: Create a table to store chat messages (if it doesn't exist)
cur.execute("""
    CREATE TABLE IF NOT EXISTS whatsapp_chats (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP,
        sender VARCHAR(255),
        message TEXT
    )
""")

conn.commit()

# Step 4: Read the chat data from a text file
chat_file_path = "chats.txt"  # Provide the path to your chats.txt file
with open(chat_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Step 5: Extract information from each line and insert into the database
# Regex to extract timestamp, sender, and message
pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} [APM]+) - (.+?): (.+)")

# Iterate through each line to extract information
for line in lines:
    match = pattern.search(line)
    if match:
        timestamp_str = match.group(1)  # Extract timestamp
        sender = match.group(2)        # Extract sender
        message = match.group(3)       # Extract message content

        # Convert timestamp to PostgreSQL-compliant format (e.g., '%m/%d/%y, %I:%M %p')
        import datetime
        timestamp = datetime.datetime.strptime(timestamp_str, '%m/%d/%y, %I:%M %p')

        # Step 6: Insert into the PostgreSQL table
        cur.execute("""
            INSERT INTO whatsapp_chats (timestamp, sender, message)
            VALUES (%s, %s, %s)
        """, (timestamp, sender, message))

conn.commit()
print("Data inserted into the database.")

# Step 7: Close the database connection
cur.close()
conn.close()
