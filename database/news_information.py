import psycopg2

def get_database_connection():
    return psycopg2.connect(
    host="yourhost",
    dbname='yousrdbname',
    user='youruser',
    password="yourpassword",
    port="yourport"
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

def get_total_news_count(genre):
    connection = get_database_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM final_project.news_information WHERE news_genre = %s"
    cursor.execute(query, (genre,))
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count



# def get_news_by_genre(genre, page=1, per_page=20):
#     offset = (page - 1) * per_page
#     connection = get_database_connection() # 데이터베이스 연결 설정
#     cursor = connection.cursor()
#     query = """
#         SELECT * FROM final_project.news_information
#         WHERE news_genre = %s
#         ORDER BY create_dt DESC
#         LIMIT %s OFFSET %s
#     """
#     cursor.execute(query, (genre, per_page, offset))
#     news_items = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return news_items

def get_news_by_genre(genre, page=1, per_page=20, search_query=''):
    offset = (page - 1) * per_page
    connection = get_database_connection()
    cursor = connection.cursor()

    # 검색어가 있을 때만 검색 조건을 추가
    if search_query:
        search_terms = search_query.split()
        search_conditions = ["news_title LIKE %s" for _ in search_terms]
        search_query_part = " AND (" + " OR ".join(search_conditions) + ")"
        search_patterns = [f"%{term}%" for term in search_terms]
        query_parameters = [genre] + search_patterns + [per_page, offset]
    else:
        search_query_part = ""
        query_parameters = [genre, per_page, offset]

    query = f"""
        SELECT * FROM final_project.news_information
        WHERE news_genre = %s
        {search_query_part}
        ORDER BY create_dt DESC
        LIMIT %s OFFSET %s
    """

    cursor.execute(query, query_parameters)
    news_items = cursor.fetchall()
    cursor.close()
    connection.close()
    return news_items
