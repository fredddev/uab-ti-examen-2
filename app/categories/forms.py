from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CategoryForm(FlaskForm):
    name = StringField('Nombre de la Categoría', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Descripción', validators=[Length(max=255)])
    submit = SubmitField('Guardar')

class EmptyForm(FlaskForm):
    pass