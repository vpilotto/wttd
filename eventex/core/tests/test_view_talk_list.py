from django.shortcuts import resolve_url as r
from django.test import TestCase

from eventex.core.models import Talk, Speaker, Course


class TalkListGet(TestCase):
    def setUp(self) -> None:
        t1 = Talk.objects.create(title='Título da Palestra', start='10:00',
                            description='Descricão da palestra')
        t2 = Talk.objects.create(title='Título da Palestra', start='13:00',
                            description='Descricão da palestra')
        c1 = Course.objects.create(title='Título do Curso', start='09:00',
                                      description='Descricão do curso', slots=20)

        speaker = Speaker.objects.create(name='Henrique Bastos',
                                         slug='henrique-bastos',
                                         website='http://henriquebastos.net')

        t1.speakers.add(speaker)
        t2.speakers.add(speaker)
        c1.speakers.add(speaker)

        self.response = self.client.get(r('talk_list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/talk_list.html')

    def test_html(self):
        contents = [
            (2, 'Título da Palestra'),
            (1, '10:00'),
            (1, '13:00'),
            (3, '/palestrantes/henrique-bastos'),
            (3, 'Henrique Bastos'),
            (2, 'Descricão da palestra'),
            (1, 'Título do Curso'),
            (1, '09:00'),
            (1, 'Descricão do curso')
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)

    def test_contexts(self):
        variables = ['talk_list']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)


class TalkListGetEmpty(TestCase):
    def test_get_empty(self):
        response = self.client.get(r('talk_list'))

        self.assertContains(response, 'Ainda não existem palestras de manhã')
        self.assertContains(response, 'Ainda não existem palestras de tarde')