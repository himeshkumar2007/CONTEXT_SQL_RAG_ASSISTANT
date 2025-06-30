import mysql.connector

def extract_schema(host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        lines = []

        for (table_name,) in tables:
            lines.append(f"Table: {table_name}")
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            for col in columns:
                lines.append(f"  - {col[0]}")
            lines.append("")  # blank line between tables

        cursor.close()
        conn.close()

        with open("db_schema.txt", "w") as f:
            f.write("\n".join(lines))

        print("Schema saved to db_schema.txt ✅")

    except mysql.connector.Error as err:
        print("Error:", err)

if __name__ == "__main__":
    # Fill in your DB credentials
    extract_schema(
        host="127.0.0.1",
        user="root",
        password="",
        database="demo1"
    )
