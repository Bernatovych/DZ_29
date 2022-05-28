""" tests.py """
import os
import unittest
from datetime import datetime
from book import app, db
from book.models import Record, Phone, Email, Address, Note
from config import basedir


TEST_DB = 'test.db'


def add_record():
    """ add record """
    datetime_rec_1 = datetime.strptime('2022-06-29', '%Y-%m-%d')
    datetime_rec_2 = datetime.strptime('1987-04-10', '%Y-%m-%d')
    rec = Record(name='Test', birthday=datetime_rec_1, phones=[Phone(number='380686543423')],
                 emails=[Email(title='test@test.ua')],
                 addresses=[Address(title='st. Test 123')],
                 notes=[Note(title='test note')], )
    rec_2 = Record(name='Test1', birthday=datetime_rec_2, phones=[Phone(number='380686543400')],
                   emails=[Email(title='test1@test.ua')],
                   addresses=[Address(title='st. Test1 123')],
                   notes=[Note(title='test1 note')], )
    db.session.add(rec)
    db.session.add(rec_2)
    db.session.commit()


class BasicTests(unittest.TestCase):

    """ tests """

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def test_home_page(self):
        """ test home page """
        add_record()
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test', response.data)
        self.assertIn(b'2022-06-29', response.data)
        self.assertIn(b'380686543423', response.data)
        self.assertIn(b'test@test.ua', response.data)
        self.assertIn(b'st. Test 123', response.data)
        self.assertIn(b'test note', response.data)

    def test_search_page(self):
        """ test search page """
        response = self.app.get('/search', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search contact', response.data)

    def test_search_record(self):
        """ test search record """
        add_record()
        response = self.app.post('/search', buffered=True,
                                   content_type='multipart/form-data',
                                   data={'contact': 'Test'}, follow_redirects=True)
        self.assertIn(b'Test', response.data)
        response = self.app.post('/search', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'contact': ''}, follow_redirects=True)
        self.assertIn(b'Enter the name of contact', response.data)

    def test_search_empty(self):
        """ test search with empty contact field """
        add_record()
        response = self.app.post('/search', buffered=True,
                                   content_type='multipart/form-data',
                                   data={'contact': ''}, follow_redirects=True)
        self.assertIn(b'Enter the name of contact', response.data)

    def test_add_record_page(self):
        """ test add record page """
        response = self.app.get('/add_record', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add', response.data)

    def test_add_record(self):
        """ test add record """
        response = self.app.post('/add_record', buffered=True,
                                   content_type='multipart/form-data',
                                   data={'name': 'Test',
                                         'birthday': '2022-06-29',
                                         'phone': '380686543423',
                                         'email': 'test@test.ua',
                                         'address': 'st. Test 123',
                                         'note': 'test note'}, follow_redirects=True)
        self.assertIn(b'Record have been saved! Test', response.data)

    def test_record_add_invalid_phone(self):
        """ test record add with invalid phone data least 12 digits """
        response = self.app.post('/add_record', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'name': 'Test',
                                       'birthday': '2022-06-29',
                                       'phone': '0686543423',
                                       'email': 'test@test.ua',
                                       'address': 'st. Test 123',
                                       'note': 'test note'}, follow_redirects=True)
        self.assertIn(b'Invalid phone number(at least 12 digits).', response.data)

    def test_record_add_invalid_phone_digits(self):
        """ test record add with invalid phone data with letters """
        response = self.app.post('/add_record', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'name': 'Test',
                                       'birthday': '2022-06-29',
                                       'phone': 'qaswedrftgyh',
                                       'email': 'test@test.ua',
                                       'address': 'st. Test 123',
                                       'note': 'test note'}, follow_redirects=True)
        self.assertIn(b'Invalid phone number(only numbers allowed).', response.data)

    def test_record_add_exist_name(self):
        """ test record add with exist name """
        add_record()
        response = self.app.post('/add_record', buffered=True,
                                   content_type='multipart/form-data',
                                   data={'name': 'Test',
                                         'birthday': '2022-06-29',
                                         'phone': '380686543423',
                                         'email': 'test@test.ua',
                                         'address': 'st. Test 123',
                                         'note': 'test note'}, follow_redirects=True)
        self.assertIn(b'Please use a different name.', response.data)

    def test_edit_record_page(self):
        """ test edit record page """
        add_record()
        response = self.app.get('/edit_record/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test', response.data)
        self.assertIn(b'2022-06-29', response.data)

    def test_edit_record(self):
        """ test edit record """
        add_record()
        response = self.app.post('/edit_record/1', buffered=True,
                                   content_type='multipart/form-data',
                                   data={'name': 'Test1',
                                         'birthday': '2022-06-28',
                                         }, follow_redirects=True)
        self.assertIn(b'Your changes have been saved.', response.data)

    def test_edit_phone_page(self):
        """ test edit phone page """
        add_record()
        response = self.app.get('/edit_phone/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'380686543423', response.data)

    def test_edit_phone(self):
        """ test edit phone """
        add_record()
        response = self.app.post('/edit_phone/1', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'number': '380686543420'}, follow_redirects=True)
        self.assertIn(b'Your changes have been saved.', response.data)

    def test_edit_phone_add_invalid_phone(self):
        """ test edit phone with add invalid phone least 12 digits """
        add_record()
        response = self.app.post('/edit_phone/1', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'number': '1212121'}, follow_redirects=True)
        self.assertIn(b'Invalid phone number(at least 12 digits).', response.data)

    def test_edit_phone_add_invalid_phone_digits(self):
        """ test edit phone with add invalid phone with letters """
        add_record()
        response = self.app.post('/edit_phone/1', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'number': 'sasaqeqeqweq'}, follow_redirects=True)
        self.assertIn(b'Invalid phone number(only numbers allowed).', response.data)

    def test_edit_email_page(self):
        """ test edit email page """
        add_record()
        response = self.app.get('/edit_email/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test@test.ua', response.data)

    def test_edit_email(self):
        """ test edit email """
        add_record()
        response = self.app.post('/edit_email/1', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'email': 'test1@test.ua'}, follow_redirects=True)
        self.assertIn(b'Your changes have been saved.', response.data)

    def test_edit_address_page(self):
        """ test edit address page """
        add_record()
        response = self.app.get('/edit_address/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'st. Test 123', response.data)

    def test_edit_address(self):
        """ test edit address """
        add_record()
        response = self.app.post('/edit_address/1', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'address': 'st. Test 1233'}, follow_redirects=True)
        self.assertIn(b'Your changes have been saved.', response.data)

    def test_edit_note_page(self):
        """ test edit note page """
        add_record()
        response = self.app.get('/edit_note/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test note', response.data)

    def test_edit_note(self):
        """ test edit note """
        add_record()
        response = self.app.post('/edit_note/1', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'note': 'test note1'}, follow_redirects=True)
        self.assertIn(b'Your changes have been saved.', response.data)

    def test_add_tag_page(self):
        """ test add tag page """
        response = self.app.get('/add_tag/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add', response.data)

    def test_add_tag(self):
        """ test add tag """
        add_record()
        response = self.app.post('/add_tag/1', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'title': 'Test tag',
                                       'notes_id': '1'}, follow_redirects=True)
        self.assertIn(b'Record have been saved!', response.data)

    def test_edit_tag_page(self):
        """ test edit tag page """
        add_record()
        self.app.post('/add_tag/1', buffered=True,
                            content_type='multipart/form-data',
                            data={'title': 'Test tag',
                                    'notes_id': '1'})
        response = self.app.get('/edit_tag/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test tag', response.data)

    def test_edit_tag(self):
        """ test edit tag """
        add_record()
        self.app.post('/add_tag/1', buffered=True,
                      content_type='multipart/form-data',
                      data={'title': 'Test tag',
                            'notes_id': '1'})
        response = self.app.post('/edit_tag/1', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'title': 'test note1'}, follow_redirects=True)
        self.assertIn(b'Your changes have been saved.', response.data)

    def test_delete_record_page(self):
        """ test delete record page """
        add_record()
        response = self.app.get('/delete_record/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Delete record: Test?', response.data)

    def test_delete_record(self):
        """ test delete record """
        add_record()
        response = self.app.post('/delete_record/1', buffered=True,
                                 content_type='multipart/form-data',
                                 follow_redirects=True)
        self.assertIn(b'Your delete contact: Test', response.data)

    def test_holidays_period_page(self):
        """ test holidays period page """
        response = self.app.get('/holidays_period', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Period', response.data)

    def test_holidays_period(self):
        """ test holidays period """
        add_record()
        response = self.app.post('/holidays_period', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'period': '100'}, follow_redirects=True)
        self.assertIn(b'Test 2022-06-29 | 32 days left till next birthday', response.data)

    def test_holidays_period_365(self):
        """ test holidays period 365 days"""
        add_record()
        response = self.app.post('/holidays_period', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'period': '365'}, follow_redirects=True)
        self.assertIn(b'Test 2022-06-29 | 32 days left till next birthday', response.data)
        self.assertIn(b'Test1 1987-04-10 | 317 days left till next birthday', response.data)

    def test_holidays_period_no_holidays(self):
        """ test holidays period with no holidays in period """
        add_record()
        response = self.app.post('/holidays_period', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'period': '10'}, follow_redirects=True)
        self.assertIn(b'No contacts with birthdays for this period.', response.data)

    def test_holidays_period_invalid_digits(self):
        """ test holidays period with letters input """
        add_record()
        response = self.app.post('/holidays_period', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'period': 'sdadad'}, follow_redirects=True)
        self.assertIn(b'Invalid data(only numbers allowed).', response.data)

    def test_holidays_period_invalid_period(self):
        """ test holidays period with input more than 365 days """
        add_record()
        response = self.app.post('/holidays_period', buffered=True,
                                 content_type='multipart/form-data',
                                 data={'period': '380'}, follow_redirects=True)
        self.assertIn(b'Period cannot be more than 365', response.data)


if __name__ == "__main__":
    unittest.main()
