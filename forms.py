from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField, BooleanField,PasswordField,
                    DateTimeField, RadioField,SelectField, TextField, TextAreaField)
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

class AddNutrientForm(FlaskForm):
    item = StringField("Item", validators=[DataRequired()])
    kcal = IntegerField("Calories")
    fat = IntegerField("Fat")
    carbs = IntegerField("Carbs")
    protein = IntegerField("Protein")
    submit = SubmitField('Submit')

class DelNutrientForm(FlaskForm):
    id = IntegerField("Id of item to delete")
    submit = SubmitField('Delete item')

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords must match.')])
    pass_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField('Submit')

    def check_email(self, field):
        if User.query.filter_by(email=field.data.first()):
            raise ValidationError('That email is already in use.')

    def check_username(self, field):
        if User.query.filter_by(username=field.data.first()):
            raise ValidationError('That username is already taken.')


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    # email = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField('Submit')



class OrganismForm(FlaskForm):
    organism = StringField("Organism", validators=[DataRequired()])
    ref_seq_ann = BooleanField("RefSeq annotation available")
    tot_seq_len = IntegerField("Total sequence length")
    assembly_level = RadioField("Assembly level", choices=[('complete','Complete genome'),
                                        ('chrom','Chromosome'),
                                        ('scaffod','Scaffold'),
                                        ('contig','Contig') ])
    assembly_name = SelectField(u"Select assembly:", choices=[('R64','R64'),
                                          ('ASM105121v1','ASM105121v1'),
                                          ('ASM308665v1','ASM308665v1') ])

    submit = SubmitField('Submit')
