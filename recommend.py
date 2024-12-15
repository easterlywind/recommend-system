import pandas as pd
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity
import joblib

def create_db_connection():
    database_name = "cplibrary"
    database_user = "root"
    database_password = "123456"
    url = f"mysql+pymysql://{database_user}:{database_password}@localhost/{database_name}"

    try:
        engine = create_engine(url)
        return engine
    except Exception as e:
        print(f"Error: {e}")
        exit()

def load_data():
    engine = create_db_connection()

    books = pd.read_sql('SELECT * FROM Books', con=engine)
    loans = pd.read_sql('SELECT * FROM Loans', con=engine)

    return books, loans

def get_default_books(books, top_n = 3):
   
    return books.sample(top_n)['book_id'].tolist() 

def build_recommendation_model(books, loans):

    user_book_matrix = loans.pivot_table(index='user_id', columns='book_id', aggfunc='size', fill_value=0)

    book_similarity = cosine_similarity(user_book_matrix.T)
    book_similarity_df = pd.DataFrame(book_similarity, index=user_book_matrix.columns, columns=user_book_matrix.columns)

    try:
        joblib.dump(book_similarity_df, 'models/book_similarity.pkl')
        print("successfully.")
    except Exception as e:
        print(f"Error: {e}")

def recommend_books(user_id, books, loans, top_n):
    engine = create_db_connection()

    loans = pd.read_sql('SELECT * FROM Loans', con=engine)

    try:
        book_similarity_df = joblib.load('models/book_similarity.pkl')
    except FileNotFoundError:
        print("Model not found")
        return []
    except Exception as e:
        print(f"Error : {e}")
        return []

    try:
        user_book_matrix = loans.pivot_table(index='user_id', columns='book_id', aggfunc='size', fill_value=0)
    except Exception as e:
        print(f"Error: {e}")
        return []

    if user_id not in user_book_matrix.index:
        # print(f"nulll")
        return get_default_books(books) 


    user_books = user_book_matrix.loc[user_id]
    user_books = user_books[user_books > 0].index  

    # print(f"{user_id}: {user_books.tolist()}")


    scores = book_similarity_df[user_books].sum(axis=1)
    scores = scores[~scores.index.isin(user_books)]  

    return scores.nlargest(top_n).index.tolist()


if __name__ == "__main__":
    books, loans = load_data()
    
    build_recommendation_model(books, loans)
    
    recommendations = recommend_books(user_id=2, books=books, loans=loans, top_n=1)
    print("Recommended books:", recommendations)
