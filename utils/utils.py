
def book_to_dict(book):
    return {
        'title': book.title,
        'upc': book.upc,
        'category': book.category,
        'price': book.price,
        'in_stock': book.in_stock,
        'rating': book.rating
    }