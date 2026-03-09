from motor_extracao.services.comparador.semantico import encontrar_semelhante
from academico.models import Materia, Topico, Fundamento

def salvar_no_banco(dados):
    if isinstance(dados, str):
        print("ERRO: A extração retornou string, esperava-se uma lista estruturada.")
        return

    materias_db = Materia.objects.all()

    for m in dados:
        materia = encontrar_semelhante(m["nome"], materias_db)

        if not materia:
            materia = Materia.objects.create(nome=m["nome"])

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
                # 1. Normaliza o nome do fundamento (trata se f é string ou dict)
                nome_fundamento = f if isinstance(f, str) else f.get("nome")

                # 2. Busca similaridade (ADICIONADA A VÍRGULA QUE FALTAVA ABAIXO)
                fundamento = encontrar_semelhante(
                    nome_fundamento, # <--- A vírgula faltava aqui
                    Fundamento.objects.filter(topico=topico)
                )

                if not fundamento:
                    # 3. Define valores padrão caso f seja apenas uma string
                    tipo = f.get("tipo_cognitivo", "Factual") if isinstance(f, dict) else "Factual"
                    nivel = f.get("nivel_cognitivo", 1) if isinstance(f, dict) else 1

                    Fundamento.objects.create(
                        topico=topico,
                        nome=nome_fundamento,
                        tipo_cognitivo=tipo,
                        nivel_cognitivo=nivel
                    )