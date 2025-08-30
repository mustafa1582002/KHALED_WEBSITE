from app import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)  # or db.Column(db.String(5000)), but db.Text is better
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def image_path(self):
        """Get the full image path"""
        if self.image_url and self.image_url.startswith('/static'):
            return self.image_url
        return None

    def __init__(self, title, description, image_url, category='general'):
        self.title = title
        self.description = description
        self.image_url = image_url
        self.category = category

    def save(self):
        """Save the project to the database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error in Project.save(): {str(e)}")
            db.session.rollback()
            raise

    def update(self, title=None, description=None, image_url=None, category=None):
        """Update project details"""
        try:
            if title:
                self.title = title
            if description:
                self.description = description
            if image_url:
                self.image_url = image_url
            if category:
                self.category = category
            self.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error in Project.update(): {str(e)}")
            db.session.rollback()
            raise

    def delete(self):
        """Delete the project from the database"""
        from app import db
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        """Get all projects ordered by creation date"""
        try:
            return cls.query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error in Project.get_all(): {str(e)}")
            return []

    @classmethod
    def get_by_id(cls, project_id):
        """Get project by ID"""
        try:
            return cls.query.get(project_id)
        except Exception as e:
            print(f"Error in Project.get_by_id(): {str(e)}")
            return None

    @classmethod
    def count(cls):
        """Count total number of projects"""
        try:
            return cls.query.count()
        except Exception as e:
            print(f"Error in Project.count(): {str(e)}")
            return 0

    @classmethod
    def delete_by_id(cls, project_id):
        """Delete a project by its ID"""
        try:
            project = cls.query.get(project_id)
            if project:
                db.session.delete(project)
                db.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Error in Project.delete_by_id(): {str(e)}")
            db.session.rollback()
            return False

    @classmethod
    def get_by_category(cls, category):
        """Get projects by category"""
        try:
            return cls.query.filter_by(category=category).order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error in Project.get_by_category(): {str(e)}")
            return []
    
    def get_comments(self):
        """Get comments for this project"""
        from app.models.comment import Comment
        return Comment.get_by_project(self.id)

    def to_dict(self):
        """Convert project to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Project {self.title}>'