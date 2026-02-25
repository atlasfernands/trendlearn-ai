import os
import json
import logging
from pytrends.request import TrendReq
from openai import OpenAI

# Configuração de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurações de API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def buscar_tendencia():
    logger.info("Buscando tendência de tecnologia no Brasil...")
    try:
        pytrends = TrendReq(hl='pt-BR', tz=360, timeout=(10,25))
        trending_searches_df = pytrends.trending_searches(pn='brazil')
        top_topic = trending_searches_df[0][0]
        logger.info(f"Tendência encontrada: {top_topic}")
        return top_topic
    except Exception as e:
        logger.error(f"Erro ao buscar tendências: {e}")
        # Fallback topic in case pytrends fails
        return "Inteligência Artificial Generativa"

def gerar_conteudo_ia(topico):
    logger.info(f"Gerando curso para o tópico: {topico}...")
    prompt = f"""
    Crie um mini-curso instrutivo altamente engajador sobre o seguinte tópico tecnológico em alta: '{topico}'.
    O conteúdo deve ser formatado estritamente como um objeto JSON plano (sem objetos aninhados) com as seguintes chaves (keys):
    - "titulo": Título chamativo do curso (string)
    - "subtitulo": Subtítulo ou slogan (string)
    - "introducao": Parágrafo introdutório sobre a importância do tema (string)
    - "mod1_tit": Título do módulo 1 (string)
    - "mod1_cont": Conteúdo explicativo contendo algumas dicas práticas para o módulo 1 (string)
    - "mod2_tit": Título do módulo 2 (string)
    - "mod2_cont": Conteúdo explicativo com um exemplo real para o módulo 2 (string)
    - "mod3_tit": Título do módulo 3 (string)
    - "mod3_cont": Próximos passos e como se aprofundar no módulo 3 (string)
    - "conclusao": Mensagem final inspiradora (string)
    
    Responda APENAS com o JSON válido, sem markdown adicional ao redor dele, aspas extras ou texto introdutório.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" },
            temperature=0.7
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar a resposta JSON da OpenAI: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro ao comunicar com a OpenAI: {e}")
        raise

def montar_site(dados):
    logger.info("Montando o site final a partir do template HTML...")
    try:
        with open("index_template.html", "r", encoding="utf-8") as f:
            template = f.read()
            
        for chave, valor in dados.items():
            template = template.replace(f"{{{{{chave}}}}}", str(valor))
            
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(template)
        logger.info("Site montado e salvo como 'index.html' com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao processar template HTML: {e}")
        raise

if __name__ == "__main__":
    try:
        tema = buscar_tendencia()
        conteudo = gerar_conteudo_ia(tema)
        montar_site(conteudo)
        logger.info("Processo concluído! O site atualizado está disponível em index.html")
    except Exception as e:
        logger.error(f"Falha catastrófica no processo principal: {e}")

