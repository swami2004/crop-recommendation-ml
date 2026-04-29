import sqlite3

conn = sqlite3.connect('cropDB.db')
cur = conn.cursor()

# Insert 5 new sample users with different data
users = [
    ('Rajesh Kumar', 'rajesh@gmail.com', '9876543210', 'Bangalore', 'rajesh', 'pass123'),
    ('Priya Singh', 'priya.singh@email.com', '8765432109', 'Delhi', 'priya', 'priya789'),
    ('Arjun Patel', 'arjun.patel@outlook.com', '7654321098', 'Mumbai', 'arjun', 'arjun456'),
    ('Neha Sharma', 'neha.sharma@yahoo.com', '6543210987', 'Hyderabad', 'neha', 'neha321'),
    ('Vikram Gupta', 'vikram.gupta@gmail.com', '5432109876', 'Chennai', 'vikram', 'vikram654')
]

for user in users:
    cur.execute("INSERT INTO users VALUES(null, ?, ?, ?, ?, ?, ?)", user)

conn.commit()
print('✓ 5 sample users inserted successfully!\n')

# Display all users
print('=' * 100)
print(f"{'ID':<5} {'Name':<25} {'Username':<15} {'Password':<15} {'Email':<30} {'Mobile':<12}")
print('=' * 100)

cur.execute('SELECT id, name, username, password, email, mobile FROM users')
for row in cur.fetchall():
    print(f"{row[0]:<5} {row[1]:<25} {row[2]:<15} {row[3]:<15} {row[4]:<30} {row[5]:<12}")

print('=' * 100)
conn.close()
