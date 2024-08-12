from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from . import db

class Media(db.Model):
    __tablename__ = 'media'
    
    media_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    media_url = db.Column(db.String(255), nullable=False)  # URL or path to the media file
    media_type = db.Column(Enum('image', 'video', name='media_types'), nullable=False)  # Type of media
    chef_id = db.Column(db.Integer, ForeignKey('chefs.chef_id'), nullable=False)
    
    chef = db.relationship('Chef', back_populates='media')

    def __repr__(self):
        return f"<Media(media_id={self.media_id}, media_url={self.media_url}, media_type={self.media_type}, chef_id={self.chef_id})>"

