from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Henrique Bastos',
            slug='henrique-bastos',
            photo='http://hbn.link/hb-link'
        )

    def test_email(self):
        contact = Contact.objects.create(
            speaker=self.speaker,
            kind=Contact.EMAIL,
            value='teste@teste.com.br'
        )

        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        contact = Contact.objects.create(
            speaker=self.speaker,
            kind=Contact.PHONE,
            value='19988880000'
        )

        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """Contact kind should be limited to E or P"""
        contact = Contact.objects.create(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker=self.speaker, kind=Contact.EMAIL, value='teste@teste.com.br')
        self.assertEqual('teste@teste.com.br', str(contact))


class ContactManagerTest(TestCase):
    def setUp(self) -> None:
        s = Speaker.objects.create(
            name='Henrique Bastos',
            slug='henrique-bastos',
            photo='http://hbn.link/hb-pic'
        )

        s.contact_set.create(kind=Contact.EMAIL, value='henrique@bastos.net')
        s.contact_set.create(kind=Contact.PHONE, value='19888880000')

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['henrique@bastos.net']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_phone(self):
        qs = Contact.objects.phones()
        expected = ['19888880000']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)