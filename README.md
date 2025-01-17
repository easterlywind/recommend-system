# Library Recommendation System

## Mô tả
Hệ thống gợi ý sách dựa trên lịch sử mượn sách của người dùng. Hệ thống sử dụng Flask để xây dựng API và tính toán độ tương đồng giữa các sách bằng phương pháp cosine similarity. 

## Các yêu cầu cài đặt

Để chạy dự án này, bạn cần cài đặt các thư viện Python sau:

```bash
pip install flask pandas sqlalchemy scikit-learn pymysql joblib
```

## Cách sử dụng
### 1. Chạy ứng dụng Flask

 Sau khi đã cài đặt các thư viện và cấu hình cơ sở dữ liệu, bạn có thể chạy ứng dụng Flask bằng cách:

```bash
python app.py
```
Ứng dụng sẽ chạy ở cổng 5000. Bạn có thể truy cập API qua URL: http://127.0.0.1:5000.

### 2. Các API có sẵn
-  **/recommend**
- Phương thức: **GET**
- Mô tả: Trả về danh sách các sách gợi ý cho một người dùng dựa - trên lịch sử mượn sách của họ.
- Tham số: **userId**( bắt buộc ): ID của người dùng cần nhận gợi ý sách.
- Ví dụ:
URL: http://127.0.0.1:5000/recommend?userId=2
- Kết quả trả về: 
```
{
  "recommendations": [
    {
      "book_id": 1,
      "isbn": "978-3-16-148410-0",
      "title": "Book Title 1",
      "author": "Author 1",
      "subject": "Subject 1",
      "publisher": "Publisher 1",
      "shelf_location": "Shelf A",
      "review": "Great book!",
      "imageUrl": "http://example.com/book1.jpg"
    },
    {
      "book_id": 2,
      "isbn": "978-3-16-148410-1",
      "title": "Book Title 2",
      "author": "Author 2",
      "subject": "Subject 2",
      "publisher": "Publisher 2",
      "shelf_location": "Shelf B",
      "review": "Interesting read!",
      "imageUrl": "http://example.com/book2.jpg"
    }
  ]
}

```