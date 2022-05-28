""" forms.py """
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, EmailField
from wtforms.validators import ValidationError, DataRequired
from book.models import Record


class RecordForm(FlaskForm):
    """ RecordForm """
    name = StringField('Name', validators=[DataRequired()])
    birthday = DateField('Birthday', default=date.today)
    phone = StringField('Phone', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    address = StringField('Address')
    note = StringField('Note')
    submit = SubmitField('Submit')

    def validate_name(self, name):
        """ validate name """
        user = Record.query.filter_by(name=name.data).first()
        if user is not None:
            raise ValidationError('Please use a different name.')

    def validate_phone(self, phone):
        """ validate phone """
        if len(phone.data) != 12:
            raise ValidationError('Invalid phone number(at least 12 digits).')
        if not phone.data.isdigit():
            raise ValidationError('Invalid phone number(only numbers allowed).')


class EditRecordForm(FlaskForm):
    """ EditRecordForm """
    name = StringField('Name')
    birthday = DateField('Birthday')
    submit = SubmitField('Edit')


class EditPhoneForm(FlaskForm):
    """ EditPhoneForm """
    number = StringField('Number')
    submit = SubmitField('Edit')

    def validate_number(self, number):
        """ validate number """
        if len(number.data) != 12:
            raise ValidationError('Invalid phone number(at least 12 digits).')
        if not number.data.isdigit():
            raise ValidationError('Invalid phone number(only numbers allowed).')


class EditEmailForm(FlaskForm):
    """ EditEmailForm """
    title = EmailField('Email')
    submit = SubmitField('Edit')


class EditAddressForm(FlaskForm):
    """ EditAddressForm """
    title = StringField('Address')
    submit = SubmitField('Edit')


class EditNoteForm(FlaskForm):
    """ EditNoteForm """
    title = StringField('Note')
    submit = SubmitField('Edit')


class AddTagForm(FlaskForm):
    """ AddTagForm """
    title = StringField('Tag')
    submit = SubmitField('Submit')


class DeleteForm(FlaskForm):
    """ DeleteForm """
    submit = SubmitField('Yes')
