import psycopg2
from psycopg2 import OperationalError

psycopg2.extensions.set_wait_callback(None)

HOST = "aws-1-eu-north-1.pooler.supabase.com"
PORT = "5432"
DATABASE = "postgres"
USER = "postgres.ckvrsacvrccumdappoqf"
PASSWORD = "atGoshi9812"

print("Trying to connect...")

try:
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        dbname=DATABASE,
        user=USER,
        password=PASSWORD,
        sslmode="require",
        application_name="ipv4"
    )
    print("Connected successfully!")
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    print("Query result:", cur.fetchone())
    cur.close()
    conn.close()

except OperationalError as e:
    print("\n❌ CONNECTION ERROR:")
    print(e)

except Exception as e:
    print("\n❌ OTHER ERROR:")
    print(e)
