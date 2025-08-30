from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100))
    full_name = db.Column(db.String(100))
    last_login = db.Column(db.DateTime)
    login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    def authenticate(cls, username, password):
        """Authenticate admin user"""
        user = cls.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if user.is_locked():
                return None, "Account is temporarily locked"
            
            # Reset login attempts on successful login
            user.login_attempts = 0
            user.last_login = datetime.utcnow()
            user.locked_until = None
            db.session.commit()
            return user, "Success"
        else:
            if user:
                user.increment_login_attempts()
            return None, "Invalid credentials"
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def increment_login_attempts(self):
        """Increment failed login attempts"""
        self.login_attempts += 1
        if self.login_attempts >= 5:
            # Lock account for 15 minutes
            from datetime import timedelta
            self.locked_until = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()
    
    def is_locked(self):
        """Check if account is locked"""
        if self.locked_until and datetime.utcnow() < self.locked_until:
            return True
        return False
    
    @classmethod
    def create_admin(cls, username, password, email=None, full_name=None):
        """Create new admin user"""
        admin = cls(
            username=username,
            email=email,
            full_name=full_name
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        return admin