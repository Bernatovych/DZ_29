""" routes.py """
from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, request
from book import app, db
from book.forms import RecordForm, EditRecordForm, EditPhoneForm, EditEmailForm, \
    EditAddressForm, EditNoteForm, AddTagForm, DeleteForm
from book.models import Record, Phone, Email, Address, Note, Tag


@app.route('/')
@app.route('/index')
def index():
    """ index """
    page = request.args.get('page', 1, type=int)
    records = Record.query.paginate(page=page, per_page=8)
    return render_template('index.html', title='Home', records=records)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """ search """
    if request.method == "POST":
        contact = request.form['contact']
        if not contact:
            flash('Enter the name of contact')
            return redirect(url_for('index'))
        records = Record.query.filter(Record.name == contact.capitalize())
        return render_template('search.html', records=records)
    return render_template('search.html')


def days_to_birthday(birthday):
    """ days_to_birthday """
    current_date = datetime.today().date()
    birthday = datetime.strptime(birthday, "%Y-%m-%d").replace(year=current_date.year).date()
    if birthday < current_date:
        birthday = birthday.replace(year=birthday.year + 1)
    days = (birthday - current_date).days
    return f"{days} days left till next birthday"


@app.route('/holidays_period', methods=['GET', 'POST'])
def holidays_period():
    """ holidays_period """
    if request.method == "POST":
        period = request.form['period']
        if not period.isdigit():
            flash('Invalid data(only numbers allowed).')
            return redirect(url_for('index'))
        if int(period) > 365:
            flash('Period cannot be more than 365')
            return redirect(url_for('index'))
        records = Record.query.all()
        day_today = datetime.now()
        day_today_year = day_today.year
        end_period = day_today + timedelta(days=int(period)+1)
        result = []
        for i in records:
            date = datetime.strptime(str(i.birthday), '%Y-%m-%d').replace(year=end_period.year)
            if day_today_year < end_period.year:
                if day_today <= date.replace(year=day_today_year) or date <= end_period:
                    result.append(f"{i.name} {i.birthday} | {days_to_birthday(str(i.birthday))}")
            else:
                if day_today <= date.replace(year=day_today_year) <= end_period:
                    result.append(f"{i.name} {i.birthday} | {days_to_birthday(str(i.birthday))}")
        if not result:
            result.append('No contacts with birthdays for this period.')
        return render_template('holidays_period.html', result=result)
    return render_template('holidays_period.html')


@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    """ add_record """
    form = RecordForm()
    if form.validate_on_submit():
        record = Record(name=form.name.data.capitalize(), birthday=form.birthday.data,
                        phones=[Phone(number=form.phone.data)],
                        emails=[Email(title=form.email.data)],
                        addresses=[Address(title=form.address.data)],
                        notes=[Note(title=form.note.data)])
        db.session.add(record)
        db.session.commit()
        flash('Record have been saved! {}'.format(record.name))
        return redirect(url_for('index'))
    return render_template('add.html', title='record', form=form)


@app.route('/edit_record/<id_record>', methods=['GET', 'POST'])
def edit_record(id_record):
    """ edit_record """
    record = Record.query.get(id_record)
    form = EditRecordForm(obj=record)
    if form.validate_on_submit():
        record.name = form.name.data
        record.birthday = form.birthday.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    return render_template('edit.html', title='Edit record', form=form)


@app.route('/edit_phone/<id_phone>', methods=['GET', 'POST'])
def edit_phone(id_phone):
    """ edit_phone """
    phone = Phone.query.get(id_phone)
    form = EditPhoneForm(obj=phone)
    if form.validate_on_submit():
        phone.number = form.number.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    return render_template('edit.html', title='Edit phone', form=form)


@app.route('/edit_email/<id_email>', methods=['GET', 'POST'])
def edit_email(id_email):
    """ edit_email """
    email = Email.query.get(id_email)
    form = EditEmailForm(obj=email)
    if form.validate_on_submit():
        email.title = form.title.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    return render_template('edit.html', title='Edit email', form=form)


@app.route('/edit_address/<id_address>', methods=['GET', 'POST'])
def edit_address(id_address):
    """ edit_address """
    address = Address.query.get(id_address)
    form = EditAddressForm(obj=address)
    if form.validate_on_submit():
        address.title = form.title.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    return render_template('edit.html', title='Edit address', form=form)


@app.route('/edit_note/<id_note>', methods=['GET', 'POST'])
def edit_note(id_note):
    """ edit_note """
    note = Note.query.get(id_note)
    form = EditNoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    return render_template('edit.html', title='Edit note', form=form)


@app.route('/add_tag/<id_note>', methods=['GET', 'POST'])
def add_tag(id_note):
    """ add_tag """
    note = Note.query.get(id_note)
    form = AddTagForm()
    if form.validate_on_submit():
        tag = Tag(title=form.title.data, notes_id=note.id)
        db.session.add(tag)
        db.session.commit()
        flash('Record have been saved!')
        return redirect(url_for('index'))
    return render_template('add.html', title='record', form=form)


@app.route('/edit_tag/<id_tag>', methods=['GET', 'POST'])
def edit_tag(id_tag):
    """ edit_tag """
    tag = Tag.query.get(id_tag)
    form = AddTagForm(obj=tag)
    if form.validate_on_submit():
        tag.title = form.title.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    return render_template('edit.html', title='Edit tag', form=form)


@app.route('/delete_record/<id_record>', methods=['GET', 'POST'])
def delete_record(id_record):
    """ delete_record """
    record = Record.query.get(id_record)
    form = DeleteForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            db.session.delete(record)
            db.session.commit()
            flash(f'Your delete contact: {record.name}')
            return redirect(url_for('index'))
    return render_template('delete.html', title='Delete record', form=form, record=record)
