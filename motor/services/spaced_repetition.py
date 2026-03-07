from django.utils import timezone
from analytics.models import MemoriaFundamento


def atualizar_memoria(usuario, questao, acertou):

    fundamentos = questao.fundamentos.all()

    for fundamento in fundamentos:

        memoria, _ = MemoriaFundamento.objects.get_or_create(
            usuario=usuario,
            fundamento=fundamento,
            defaults={
                "proxima_revisao": timezone.now()
            }
        )

        if acertou:

            memoria.repeticoes += 1

            if memoria.repeticoes == 1:
                memoria.intervalo = 1
            elif memoria.repeticoes == 2:
                memoria.intervalo = 3
            else:
                memoria.intervalo *= memoria.facilidade

            memoria.facilidade += 0.1

        else:

            memoria.repeticoes = 0
            memoria.intervalo = 1
            memoria.facilidade -= 0.2

        memoria.proxima_revisao = timezone.now() + timezone.timedelta(days=memoria.intervalo)

        memoria.save()