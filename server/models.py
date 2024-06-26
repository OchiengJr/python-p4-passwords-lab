from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt  # Assuming you import SQLAlchemy instance `db` and `bcrypt` setup

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password_hash = db.Column(db.String)  # Store hashed password in a separate column

    @hybrid_property
    def password_hash(self):
        # Raise an exception or handle differently based on application security needs
        raise Exception('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        # Hash the password using bcrypt and store it in _password_hash
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        # Check if the provided password matches the stored hashed password
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'User {self.username}, ID: {self.id}'

# Example of usage:
if __name__ == '__main__':
    # Create a new user
    new_user = User(username='example_user')
    new_user.password_hash = 'password123'  # Hash and store the password
    db.session.add(new_user)
    db.session.commit()

    # Authenticate a user
    user = User.query.filter_by(username='example_user').first()
    if user.authenticate('password123'):
        print('Authentication successful!')
    else:
        print('Authentication failed!')
