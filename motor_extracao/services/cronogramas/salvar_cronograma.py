from motor_extracao.services.comparador.semantico import encontrar_semelhante
from academico.models import Materia, Topico, Fundamento


def salvar_no_banco(dados):

    materias_db = Materia.objects.all()

    for m in dados:

        materia = encontrar_semelhante(m["nome"], materias_db)

        if not materia:

            materia = Materia.objects.create(
                nome=m["nome"]
            )

        for t in m["topicos"]:

            topico = encontrar_semelhante(
                t["titulo"],
                Topico.objects.filter(materia=materia)
            )

            if not topico:

                topico = Topico.objects.create(
                    materia=materia,
                    nome=t["titulo"]
                )

            for f in t["fundamentos"]:

                fundamento = encontrar_semelhante(
                    f["nome"],
                    Fundamento.objects.filter(topico=topico)
                )

                if not fundamento:

                    Fundamento.objects.create(
                        topico=topico,
                        nome=f["nome"],
                        tipo_cognitivo=f["tipo_cognitivo"],
                        nivel_cognitivo=f["nivel_cognitivo"]
                    )