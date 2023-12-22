import psycopg2

def get_database_connection():
    return psycopg2.connect(
    host="localhost",
    dbname='final_project',
    user='root',
    password="5432",
    port=5432
)

def fetch_news_information():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, media_company, news_genre, news_image_path, news_title, news_url, news_summary
        FROM final_project.news_information
    """)
    news_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return news_items