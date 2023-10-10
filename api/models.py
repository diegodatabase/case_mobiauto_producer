from dataclasses import dataclass

@dataclass
class Book:
    
    title: str
    upc: str
    category: str
    price: str
    in_stock: str
    rating: str