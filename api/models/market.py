from api import db

class Data(db.Model):
    __tablename__ = 'market_data'
    id = db.Column('id', db.Integer, primary_key=True)
    low = db.Column('low', db.Float, nullable=True)
    high = db.Column('high', db.Float, nullable=True)
    close = db.Column('close', db.Float, nullable=True)
    volume = db.Column('volume', db.Float, nullable=True)

    def __init__(self, id, low=None, high=None, close=None, volume=None):
        self.id = id
        self.low = low
        self.high = high
        self.close = close
        self.volume = volume
