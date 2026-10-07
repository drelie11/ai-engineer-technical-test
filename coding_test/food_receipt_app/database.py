from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///receipts.db', echo=False)
Base = declarative_base()

class Receipt(Base):
    __tablename__ = 'receipts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    merchant_name = Column(String, nullable=False)
    total_amount = Column(Integer, nullable=False)
    
    items = relationship("ReceiptItem", back_populates="receipt", cascade="all, delete-orphan")

class ReceiptItem(Base):
    __tablename__ = 'receipt_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey('receipts.id'), nullable=False)
    item_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    
    receipt = relationship("Receipt", back_populates="items")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def insert_receipt(receipt_data):
    session = Session()
    try:
        receipt_date = datetime.strptime(receipt_data['date'], '%Y-%m-%d').date()
        
        new_receipt = Receipt(
            date=receipt_date,
            merchant_name=receipt_data['merchant_name'],
            total_amount=receipt_data['total_amount']
        )
        
        for item_data in receipt_data['items']:
            new_item = ReceiptItem(
                item_name=item_data['item_name'],
                price=item_data['price'],
                quantity=item_data.get('quantity', 1)
            )
            new_receipt.items.append(new_item)
            
        session.add(new_receipt)
        session.commit()
        print(f"Successfully inserted receipt from {new_receipt.merchant_name} (ID: {new_receipt.id})")
        return new_receipt.id
        
    except Exception as e:
        session.rollback()
        print(f"Error inserting receipt: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    dummy_data = {
        "date": "2024-06-20", 
        "merchant_name": "Nasi Goreng Kebon Sirih",
        "total_amount": 100000,
        "items": [
            {"item_name": "Nasi Goreng Kambing", "price": 45000, "quantity": 1},
            {"item_name": "Sate Kambing (5 tusuk)", "price": 50000, "quantity": 1},
            {"item_name": "Es Teh Manis", "price": 5000, "quantity": 1}
        ]
    }
    
    receipt_id = insert_receipt(dummy_data)
    
    session = Session()
    saved_receipt = session.query(Receipt).filter_by(id=receipt_id).first()
    if saved_receipt:
        print(f"\nVerification Query:")
        print(f"Merchant: {saved_receipt.merchant_name}")
        print(f"Date: {saved_receipt.date}")
        print("Items:")
        for item in saved_receipt.items:
            print(f" - {item.quantity}x {item.item_name} @ Rp {item.price:,}")
        print(f"Total: Rp {saved_receipt.total_amount:,}")
    session.close()