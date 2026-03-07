"""
Formularios de autenticación usando Flask-WTF.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    """Formulario de registro de usuarios."""
    
    username = StringField(
        'Nombre de Usuario',
        validators=[
            DataRequired(message='El nombre de usuario es requerido.'),
            Length(min=3, max=80, message='El nombre de usuario debe tener entre 3 y 80 caracteres.')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nombre de usuario',
            'autofocus': True
        }
    )
    
    email = StringField(
        'Correo Electrónico',
        validators=[
            DataRequired(message='El correo es requerido.'),
            Email(message='Por favor ingresa un correo válido.')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com',
            'type': 'email'
        }
    )
    
    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message='La contraseña es requerida.'),
            Length(min=6, message='La contraseña debe tener al menos 6 caracteres.')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Ingresa una contraseña segura'
        }
    )
    
    confirm_password = PasswordField(
        'Confirmar Contraseña',
        validators=[
            DataRequired(message='Debes confirmar la contraseña.'),
            EqualTo('password', message='Las contraseñas no coinciden.')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña'
        }
    )
    
    submit = SubmitField(
        'Registrarse',
        render_kw={'class': 'btn btn-primary w-100'}
    )
    
    def validate_username(self, field):
        """Valida que el nombre de usuario sea único."""
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Este nombre de usuario ya está registrado.')
    
    def validate_email(self, field):
        """Valida que el email sea único."""
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Este correo ya está registrado.')


class LoginForm(FlaskForm):
    """Formulario de login de usuarios."""
    
    username = StringField(
        'Nombre de Usuario',
        validators=[DataRequired(message='El nombre de usuario es requerido.')],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nombre de usuario',
            'autofocus': True
        }
    )
    
    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(message='La contraseña es requerida.')],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        }
    )
    
    submit = SubmitField(
        'Iniciar Sesión',
        render_kw={'class': 'btn btn-primary w-100'}
    )
