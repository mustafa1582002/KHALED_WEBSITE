from app import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    service_type = db.Column(db.String(50), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='pending')  # pending, in-progress, completed, cancelled
    
    def __init__(self, name, email, message, phone=None, service_type=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.service_type = service_type
        self.message = message
    
    def save(self):
        """Save the message to the database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error in Message.save(): {str(e)}")
            db.session.rollback()
            raise
    
    def delete(self):
        """Delete the message from the database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error in Message.delete(): {str(e)}")
            db.session.rollback()
            raise
    
    def mark_as_read(self):
        """Mark the message as read"""
        try:
            self.is_read = True
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error in Message.mark_as_read(): {str(e)}")
            db.session.rollback()
            raise

    def update_status(self, status):
        """Update message status"""
        try:
            if status in ['pending', 'in-progress', 'completed', 'cancelled']:
                self.status = status
                db.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Error in Message.update_status(): {str(e)}")
            db.session.rollback()
            raise

    @staticmethod
    def get_all():
        """Get all messages"""
        try:
            return Message.query.order_by(Message.created_at.desc()).all()
        except Exception as e:
            print(f"Error in Message.get_all(): {str(e)}")
            return []

    @staticmethod
    def get_by_id(message_id):
        """Get message by ID"""
        try:
            return Message.query.get(message_id)
        except Exception as e:
            print(f"Error in Message.get_by_id(): {str(e)}")
            return None

    @staticmethod
    def get_unread():
        """Get all unread messages"""
        try:
            return Message.query.filter_by(is_read=False).all()
        except Exception as e:
            print(f"Error in Message.get_unread(): {str(e)}")
            return []

    @staticmethod
    def count():
        """Count total messages"""
        try:
            return Message.query.count()
        except Exception as e:
            print(f"Error in Message.count(): {str(e)}")
            return 0

    def to_dict(self):
        """Convert message to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'service_type': self.service_type,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_read': self.is_read,
            'status': self.status
        }

    def __repr__(self):
        return f'<Message from {self.name}>'