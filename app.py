from flask import Flask, request, jsonify
from recommend import recommend_books, load_data, build_recommendation_model
import json

app = Flask(__name__)

# @app.route('/build_model', methods=['GET'])
# def build_model():
#     books, loans = load_data() 
#     build_recommendation_model(books, loans)  
#     return jsonify({'message': 'successfully.'})

@app.route('/recommend', methods=['GET'])
def recommend():

    user_id = request.args.get('userId', type=int)  

    if user_id is None:
        return jsonify({'error': 'user_id is required'}), 400

    books, loans = load_data()

    build_recommendation_model(books, loans) 

    books_dict = books.to_dict(orient='records')

    recommendations = recommend_books(user_id, books, loans, top_n=5)

    recommended_books = []
    for book_id in recommendations:
        book = next((b for b in books_dict if b['book_id'] == book_id), None)
        if book:
            recommended_books.append({
                'book_id': book['book_id'],
                'quantity':book['quantity'],
                'isbn':book['isbn'],
                'title': book['title'],
                'author': book['author'],
                'subject': book['subject'],
                'publisher': book['publisher'],
                'shelf_location': book['shelf_location'],
                'review':book['review'],
                'imageUrl':book['image_url']
            })

    return jsonify({'recommendations': recommended_books})


if __name__ == '__main__':
    app.run(debug=True)
