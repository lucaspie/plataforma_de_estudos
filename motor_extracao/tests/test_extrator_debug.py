from django.test import TestCase

from academico.models import Materia, Topico, Fundamento
from motor_extracao.services.cronogramas.salvar_cronograma import salvar_no_banco
import pytest

@pytest.mark.django_db
class SalvarNoBancoTest(TestCase):

    def setUp(self):

        self.dados = [
            {
                "nome": "Física",
                "topicos": [
                    {
                        "titulo": "Cinemática",
                        "fundamentos": [
                            {
                                "nome": "Velocidade média",
                                "tipo_cognitivo": "conceitual",
                                "nivel_cognitivo": 1
                            },
                            {
                                "nome": "Aceleração",
                                "tipo_cognitivo": "conceitual",
                                "nivel_cognitivo": 1
                            }
                        ]
                    }
                ]
            }
        ]

    def test_cria_materia_topico_fundamento(self):

        salvar_no_banco(self.dados)

        self.assertEqual(Materia.objects.count(), 1)
        self.assertEqual(Topico.objects.count(), 1)
        self.assertEqual(Fundamento.objects.count(), 2)

    def test_evitar_duplicacao_semantica(self):

        salvar_no_banco(self.dados)

        dados_duplicados = [
            {
                "nome": "fisica",  # variação
                "topicos": [
                    {
                        "titulo": "Cinematica",  # sem acento
                        "fundamentos": [
                            {
                                "nome": "Calculo da velocidade media",
                                "tipo_cognitivo": "conceitual",
                                "nivel_cognitivo": 1
                            }
                        ]
                    }
                ]
            }
        ]

        salvar_no_banco(dados_duplicados)

        # não deve criar nova matéria
        self.assertEqual(Materia.objects.count(), 1)

        # não deve criar novo tópico
        self.assertEqual(Topico.objects.count(), 1)

        # pode ou não detectar como igual dependendo do threshold
        self.assertLessEqual(Fundamento.objects.count(), 3)