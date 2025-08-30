from app import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)  # Added foreign key
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    client_type = db.Column(db.String(50), nullable=True)
    rating = db.Column(db.Integer, nullable=True)  # Added rating field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=False)
    
    def __init__(self, name, email, content, client_type=None, project_id=None, rating=None):
        self.name = name
        self.email = email
        self.content = content
        self.client_type = client_type
        self.project_id = project_id
        self.rating = rating
    
    def save(self):
        """Save the comment to the database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error in Comment.save(): {str(e)}")
            db.session.rollback()
            return False

    def delete(self):
        """Delete the comment from the database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error in Comment.delete(): {str(e)}")
            db.session.rollback()
            return False
    
    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_approved(cls):
        return cls.query.filter_by(is_approved=True).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_id(cls, comment_id):
        return cls.query.get(comment_id)
    
    @classmethod
    def get_by_project(cls, project_id):
        return cls.query.filter_by(project_id=project_id, is_approved=True).order_by(cls.created_at.desc()).all()