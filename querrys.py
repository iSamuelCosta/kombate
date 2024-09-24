def query_datas():
    return '''

SELECT 
    MIN(v.date_time) AS menor_data, 
    MAX(v.date_time) AS maior_data 
FROM 
    visita v
WHERE 
    DATE(v.date_time) >= CURDATE() - INTERVAL 30 day; 
'''


def querry_bairro_tipo_imovel(data_inicial, data_final):
    return f"""
SELECT
    endereco.bairro,
    tipo_imovel.tipo,
    COUNT(visita.id) AS numero_de_visitas
FROM endereco
JOIN imovel ON endereco.id = imovel.endereco_id
JOIN visita ON imovel.id = visita.imovel_id
JOIN tipo_imovel ON imovel.tipo_imovel_id = tipo_imovel.id
WHERE visita.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
GROUP BY endereco.bairro, tipo_imovel.tipo;
"""

def query_metric_teve_larvicida(data_inicial, data_final):
    return f'''
SELECT COUNT(*) AS numero_de_linhas
FROM visita v
JOIN visita_imovel vi ON v.id = vi.id_visita
WHERE vi.larvicida_id <> 1 AND v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
'''
def query_metric_teve_larvicida_7_dias():
    return '''
SELECT COUNT(*) AS numero_de_linhas
FROM visita v
JOIN visita_imovel vi ON v.id = vi.id_visita
WHERE vi.larvicida_id <> 1
  AND v.date_time >= DATE_SUB(NOW(), INTERVAL 7 DAY);
'''

def query_metric_quantidade_visitas(data_inicial, data_final):
    return f"""
SELECT COUNT(*) AS numero_de_linhas
FROM visita
WHERE visita.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
"""

def query_quantidade_visitas_7_dias():
    return """
SELECT COUNT(*) AS numero_de_linhas
FROM visita
WHERE date_time >= DATE_SUB(NOW(), INTERVAL 7 DAY)
"""

def query_visitas_agente(data_inicial, data_final):
    return f'''
SELECT agente.nome, COUNT(visita.id) AS numero_de_visitas FROM agente
JOIN visita ON agente.id = visita.agente_id
WHERE agente.id <> 103 AND agente.id <> 102 AND visita.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
GROUP BY agente.nome
'''

def query_supervisores_agentes(data_inicial, data_final):
    return f'''
SELECT agente.nome, COUNT(visita.id) AS numero_de_visitas FROM agente
JOIN visita ON agente.id = visita.agente_id
WHERE agente.id = 103 OR agente.id = 102 AND visita.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
GROUP BY agente.nome
'''
def query_metric_media_visitas_diaria(data_inicial, data_final):
    return f'''
SELECT AVG(numero_de_linhas) AS media_numero_linhas
FROM (
    SELECT COUNT(*) AS numero_de_linhas
    FROM visita
    WHERE DAYOFWEEK(date_time) NOT IN (1, 7) AND visita.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
    GROUP BY DATE(date_time)
) as subquery;
'''

def query_media_visitas_agente(data_inicial, data_final):
    return f'''
SELECT AVG(numero_de_visitas) AS media_numero_linhas
FROM (
    SELECT agente.nome, COUNT(visita.id) AS numero_de_visitas FROM agente
    JOIN visita ON agente.id = visita.agente_id
    WHERE agente.id <> 2 AND agente.id <> 39 AND agente.id <> 89 AND agente.id <> 62 AND agente.id <> 104 AND visita.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
    GROUP BY agente.nome
) as subquery;
'''
def query_quantidade_focos(data_inicial, data_final):
    return f'''
SELECT COUNT(*) AS numero_de_linhas
FROM visita v
JOIN visita_imovel vi ON v.id = vi.id_visita
JOIN resp_questao rq ON vi.id = rq.id_visita_imovel
WHERE vi.larvicida_id <> 1 
  AND rq.resposta = 'Y' AND v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
'''
def query_visitas_mes():
    return '''
SELECT 
    DATE_FORMAT(date_time, '%Y/%m') AS mes_ano,
    COUNT(*) AS numero_de_linhas
FROM visita
WHERE DAYOFWEEK(date_time) NOT IN (1, 7) -- Exclui domingo (1) e sábado (7)
GROUP BY mes_ano;
'''

def query_visitas_dia(data_inicial, data_final):
    return f'''
SELECT 
    DATE_FORMAT(date_time, '%m/%d') AS data,
    COUNT(*) AS numero_de_linhas
FROM visita
WHERE DAYOFWEEK(date_time) NOT IN (1, 7) AND date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'

GROUP BY data;
'''

def query_situacao_visita(data_inicial, data_final):
    return f'''
SELECT COUNT(v1.id) AS quantidade, sv.situacao as situacao
FROM visita v1
JOIN situacao_visita sv ON v1.situacao_visita_id = sv.id
WHERE v1.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
GROUP BY sv.situacao;
'''

def query_tipo_imovel_visita(data_inicial, data_final):
    return f'''
SELECT tipo_imovel.tipo as tipo, COUNT(v.id) AS numero_de_visitas
FROM tipo_imovel 
JOIN imovel i ON tipo_imovel.id = i.tipo_imovel_id
JOIN visita v ON i.id = v.imovel_id
WHERE v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
GROUP BY tipo;
'''

def query_mapa():
    return '''
SELECT
    imovel_geo.geo as latlong,
   
    COUNT(*) AS quantidade_visitas
FROM
    imovel_geo
JOIN
    imovel ON imovel_geo.imovel_id = imovel.id
JOIN
    visita ON imovel.id = visita.imovel_id
GROUP BY
    latlong;
'''

def querry_bairro(data_inicial, data_final):
    return f"""
SELECT
    endereco.bairro,
    COUNT(visita.id) AS numero_de_visitas
FROM endereco
JOIN imovel ON endereco.id = imovel.endereco_id
JOIN visita ON imovel.id = visita.imovel_id
WHERE visita.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
GROUP BY endereco.bairro
"""

def query_data():
    return '''
    SELECT MIN(data_visita) AS menor_data, MAX(data_visita) AS maior_data FROM visita_imovel
    '''

def query_agentes_unicos():
    return '''
SELECT DISTINCT id, nome FROM agente

'''


####################################################################################################################################

def query_visitas_agentes_bairro(data_inicial, data_final, id):
    return f'''
    SELECT e.bairro as Bairro, COUNT(v.id) as "Quantidade de Visitas"  FROM visita v

INNER JOIN imovel i ON i.id = v.imovel_id
INNER JOIN endereco e ON e.id = i.endereco_id
WHERE v.agente_id = {id} and v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
GROUP BY e.bairro
order by COUNT(v.id) Desc
    '''

def query_visitas_agentes_tipo_imovel(data_inicial, data_final, id):
    return f'''
    SELECT ti.tipo as Tipo, COUNT(v.id) as "Quantidade de Visitas"  FROM visita v

INNER JOIN imovel i ON i.id = v.imovel_id
INNER JOIN tipo_imovel ti ON ti.id = i.tipo_imovel_id
WHERE v.agente_id = {id} and v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
GROUP BY ti.tipo
order by COUNT(v.id) Desc
    '''
def query_visitas_mes_agente(id):
    return f'''
SELECT 
    DATE_FORMAT(v.date_time, '%Y/%m') AS `Mês`,
    COUNT(v.id) AS Quantidade,
    s.situacao
FROM visita v
INNER JOIN situacao_visita s ON s.id = v.situacao_visita_id
WHERE DAYOFWEEK(v.date_time) NOT IN (1, 7) AND v.agente_id = {id}
GROUP BY `Mês`, s.situacao;

'''

def query_visitas_dia_agente(data_inicial, data_final, id):
    return f'''
SELECT 
    DATE_FORMAT(date_time, '%m/%d') AS "Dia",
    COUNT(*) AS "Quantidade"
FROM visita
WHERE DAYOFWEEK(date_time) NOT IN (1, 7) AND date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00' and visita.agente_id = {id}

GROUP BY DATE_FORMAT(date_time, '%m/%d');
'''


def query_geo_foco(data_inicial, data_final):
 
    return f'''
SELECT COUNT(v.id) AS Quantidade, ig.geo FROM visita v

INNER JOIN imovel_geo ig ON ig.imovel_id = v.imovel_id
INNER JOIN visita_imovel vi ON vi.id_visita = v.id
INNER JOIN resp_questao rq ON rq.id_visita_imovel = vi.id
WHERE rq.resposta = "Y" AND v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
GROUP BY ig.geo
ORDER BY COUNT(v.id) DESC 

'''

def query_geo_larvicida(data_inicial, data_final):
 
    return f'''
SELECT COUNT(v.id) AS Quantidade, ig.geo FROM visita v

INNER JOIN imovel_geo ig ON ig.imovel_id = v.imovel_id
INNER JOIN visita_imovel vi ON vi.id_visita = v.id
WHERE vi.larvicida_id <> 1 AND v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
GROUP BY ig.geo
ORDER BY COUNT(v.id) DESC 

'''

def query_bairro_larvecida(data_inicial, data_final):
    return f'''
SELECT e.bairro as Bairro,  COUNT(v.id) AS Quantidade FROM visita v

INNER JOIN imovel i ON i.id = v.imovel_id
INNER JOIN visita_imovel vi ON vi.id_visita = v.id
INNER JOIN endereco e ON e.id = i.endereco_id
WHERE vi.larvicida_id <> 1 AND v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'

GROUP BY e.bairro

ORDER BY COUNT(v.id) DESC 
'''

def query_bairro_focos(data_inicial, data_final):
    return f'''
SELECT e.bairro as Bairro, COUNT(v.id) AS Quantidade FROM visita v

INNER JOIN imovel i ON i.id = v.imovel_id
INNER JOIN visita_imovel vi ON vi.id_visita = v.id
INNER JOIN endereco e ON e.id = i.endereco_id
INNER JOIN resp_questao rq ON rq.id_visita_imovel = vi.id
WHERE rq.resposta = "Y" AND v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'

GROUP BY e.bairro

ORDER BY COUNT(v.id) DESC 
'''

def query_imoveis_fechados(data_inicial, data_final):
    return f'''
SELECT COUNT(v.id) AS "Quantidade", ig.geo FROM visita v
INNER JOIN imovel_geo ig ON ig.imovel_id = v.imovel_id
WHERE v.situacao_visita_id = 6 AND v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
GROUP BY geo 
ORDER BY COUNT(v.id) desc

'''

#############################################################################
def query_bairros_confirmados(data_inicial, data_final):
    return f'''
SELECT s.nome_bairro, count(s.id) as "Quantidade" FROM sinan_dengue s
WHERE s.classi_fin IN (10,11,12) and s.dt_encerra BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
GROUP BY s.nome_bairro 
ORDER BY COUNT(s.id) desc

'''

def query_geo_larvicida_data(data_inicial, data_final):
 
    return f'''
SELECT DATE_FORMAT(v.date_time, '%d/%m/%Y %H:%i:%s') as Data, ig.geo, a.nome FROM visita v

INNER JOIN imovel_geo ig ON ig.imovel_id = v.imovel_id
INNER JOIN visita_imovel vi ON vi.id_visita = v.id
INNER JOIN agente a ON a.id = v.agente_id
WHERE vi.larvicida_id <> 1 AND v.date_time AND v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'



'''

def query_geo_foco_data(data_inicial, data_final):
 
    return f'''
SELECT DATE_FORMAT(v.date_time, '%d/%m/%Y %H:%i:%s') as Data, ig.geo, a.nome FROM visita v

INNER JOIN imovel_geo ig ON ig.imovel_id = v.imovel_id
INNER JOIN visita_imovel vi ON vi.id_visita = v.id
INNER JOIN resp_questao rq ON rq.id_visita_imovel = vi.id
INNER JOIN agente a ON a.id = v.agente_id
WHERE rq.resposta = "Y" AND v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00' AND vi.larvicida_id <> 1


'''

def query_imoveis_fechados_data(data_inicial, data_final):
    return f'''
SELECT DATE_FORMAT(v.date_time, '%d/%m/%Y %H:%i:%s') as Data, ig.geo, a.nome FROM visita v
INNER JOIN imovel_geo ig ON ig.imovel_id = v.imovel_id
INNER JOIN visita_imovel vi ON vi.id_visita = v.id
INNER JOIN agente a ON a.id = v.agente_id
WHERE v.situacao_visita_id = 6 AND v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'


'''

def query_imoveis_recuperados_data(data_inicial, data_final):
    return f'''
SELECT DATE_FORMAT(v.date_time, '%d/%m/%Y %H:%i:%s') as Data, ig.geo, a.nome FROM visita v
INNER JOIN imovel_geo ig ON ig.imovel_id = v.imovel_id
INNER JOIN visita_imovel vi ON vi.id_visita = v.id
INNER JOIN agente a ON a.id = v.agente_id
WHERE v.situacao_visita_id = 7 AND v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'


'''

def query_imoveis_visitados_data(data_inicial, data_final):
    return f'''
SELECT DATE_FORMAT(v.date_time, '%d/%m/%Y %H:%i:%s') as Data, ig.geo, a.nome FROM visita v
INNER JOIN imovel_geo ig ON ig.imovel_id = v.imovel_id
INNER JOIN visita_imovel vi ON vi.id_visita = v.id
INNER JOIN agente a ON a.id = v.agente_id
WHERE v.situacao_visita_id = 4 AND v.date_time BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'


'''


def query_raca_sinan_dengue(data_inicial, data_final):

    return f'''
SELECT COUNT(sd.id) AS "Quantidade", r.nome AS Nome FROM sinan_dengue sd
INNER JOIN raca r ON r.id = sd.raca_id
WHERE sd.dt_encerra BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
GROUP BY r.nome
ORDER BY COUNT(sd.id) DESC

'''

def query_sexo_sinan_dengue(data_inicial, data_final):

    return f'''
SELECT COUNT(sd.id) AS "Quantidade", s.Nome AS Nome FROM sinan_dengue sd
INNER JOIN sexo_sigla s ON s.Sigla = sd.sigla_sexo
WHERE sd.dt_encerra BETWEEN '{data_inicial}' AND '{data_final} 23:59:00'
GROUP BY s.Nome
ORDER BY COUNT(sd.id) DESC

'''

def query_notificacoes_mes_sinan_dengue():
    return f'''
SELECT COUNT(sd.id) AS "Quantidade", DATE_FORMAT(sd.data_notificacao, '%Y/%m') AS "Mês" FROM sinan_dengue sd
WHERE sd.data_notificacao
GROUP BY DATE_FORMAT(sd.data_notificacao, '%Y/%m')
ORDER BY COUNT(sd.id) DESC

'''

    
def query_classificacao_mes_sinan_dengue(data_inicial, data_final):
    return f'''
SELECT COUNT(sd.id) AS "Quantidade", DATE_FORMAT(sd.data_notificacao, '%Y/%m') AS "Mês",  FROM sinan_dengue sd
WHERE sd.data_notificacao
GROUP BY DATE_FORMAT(sd.data_notificacao, '%Y/%m')
ORDER BY COUNT(sd.id) DESC

'''

def query_sisreg():
    return f'''
SELECT ta.unidade_saude_solicitante, ta.profissional, ta.procedimento, ta.solicitacoes_pendentes
FROM tabela_agenda ta

'''

def query_ano_diarreia():
    return f'''
SELECT ano FROM semanas_epidemiologicas s 
'''

def query_diarreia_semana_epidemiologica(ano):
    return f'''
SELECT DISTINCT s.semana 
FROM semanas_epidemiologicas s
JOIN monitorizacao_doencas_diarreicas m ON m.semana_epidemiologica = s.semana
WHERE s.ano = {ano}
ORDER BY s.semana DESC;

'''

def datas_semana_epidemiologica(ano, semana):
    return f'''
SELECT * FROM semanas_epidemiologicas s 
where s.ano = {ano} and s.semana = {semana}
'''

def query_faixa_etaria_diarreia(ano, semana):
    return f'''
SELECT f.faixa_etaria as "Faixa etária", COUNT(m.id) as "Nº de Casos"
FROM faixa_etaria_diarreicas f
LEFT JOIN monitorizacao_doencas_diarreicas m ON f.id = m.faixa_etaria 
AND m.ano = {ano} 
AND m.semana_epidemiologica = {semana}
GROUP BY f.faixa_etaria;

'''
def query_faixa_etaria_diarreia_sangue(ano, semana):
    return f'''
SELECT f.faixa_etaria as "Faixa etária", COUNT(m.id) AS "Nº de Casos"
FROM faixa_etaria_diarreicas f
LEFT JOIN monitorizacao_doencas_diarreicas m ON f.id = m.faixa_etaria 
and m.ano = {ano} 
AND m.semana_epidemiologica = {semana}
AND m.diarreia_com_sangue = 1

GROUP BY f.faixa_etaria;


'''

def query_plano_diarreia(ano, semana):
    return f'''
SELECT p.plano as "Plano de Tratamento", COUNT(m.id) AS "Nº de Casos"
FROM plano_tratamento_diarreia p
LEFT JOIN monitorizacao_doencas_diarreicas m ON p.id = m.plano_tratamento
and m.ano = {ano} 
AND m.semana_epidemiologica = {semana}

GROUP BY p.plano
order by COUNT(m.id) desc
'''


def query_procedencia_diarreia(ano, semana):
    return f'''
SELECT m.bairro as "Bairro", COUNT(m.id) as "Nº de Casos"
FROM  monitorizacao_doencas_diarreicas m

where m.ano = {ano} 
AND m.semana_epidemiologica = {semana}

GROUP BY  m.bairro;

'''

def query_analise_casos(semana, ano):
    return f'''
select * from analise_casos where semana_selecionando = {semana} and ano_selecionando = {ano}
'''

########################################################################################################
def query_faixa_etaria_diarreia_ubs(ano, semana, ubs):
    return f'''
SELECT f.faixa_etaria as "Faixa etária", COUNT(m.id) as "Nº de Casos"
FROM faixa_etaria_diarreicas f
LEFT JOIN monitorizacao_doencas_diarreicas m ON f.id = m.faixa_etaria 
AND m.ano = {ano} 
AND m.semana_epidemiologica = {semana} and m.unidade_saude={ubs}
GROUP BY f.faixa_etaria;

'''

def query_faixa_etaria_diarreia_sangue_ubs(ano, semana, ubs):
    return f'''
SELECT f.faixa_etaria as "Faixa etária", COUNT(m.id) AS "Nº de Casos"
FROM faixa_etaria_diarreicas f
LEFT JOIN monitorizacao_doencas_diarreicas m ON f.id = m.faixa_etaria 
and m.ano = {ano} 
AND m.semana_epidemiologica = {semana} and m.unidade_saude={ubs}
AND m.diarreia_com_sangue = 1

GROUP BY f.faixa_etaria;


'''

def query_plano_diarreia_ubs(ano, semana, ubs):
    return f'''
SELECT p.plano as "Plano de Tratamento", COUNT(m.id) AS "Nº de Casos"
FROM plano_tratamento_diarreia p
LEFT JOIN monitorizacao_doencas_diarreicas m ON p.id = m.plano_tratamento
and m.ano = {ano} 
AND m.semana_epidemiologica = {semana} and m.unidade_saude={ubs}

GROUP BY p.plano
order by COUNT(m.id) desc
'''
def query_procedencia_diarreia_ubs(ano, semana, ubs):
    return f'''
SELECT m.bairro as "Bairro", COUNT(m.id) as "Nº de Casos"
FROM  monitorizacao_doencas_diarreicas m

where m.ano = {ano} 
AND m.semana_epidemiologica = {semana} and m.unidade_saude={ubs}

GROUP BY  m.bairro;    '''


def query_analise_casos_ubs(semana, ano, ubs):
    return f'''
select * from analise_casos where semana_selecionando = {semana} and ano_selecionando = {ano} and ubs = {ubs}
'''

def query_pega_nome_ubs(ubs):
    return f'''
SELECT nome_nudade FROM unidades_saude WHERE id_unidade = {ubs}
'''

def query_pessoas_ubs(ano, semana, ubs):
    return f'''
SELECT m.data_atendimento as "Data", m.nome_paciente as "Nome", f.faixa_etaria as "Faixa etária", m.rua as "Rua", m.bairro as "Bairro", m.numero as "Número"
FROM  monitorizacao_doencas_diarreicas m
join faixa_etaria_diarreicas f on f.id = m.faixa_etaria
where m.ano = {ano} 
AND m.semana_epidemiologica = {semana}
and m.unidade_saude = {ubs}

'''

def query_resumo_producao_diaria():
    return f'''

SELECT 
    sub.nome,
    COALESCE(sub.contar, 0) AS total_contar,
    COALESCE(sub2.contar, 0) AS conta_visitado,
    COALESCE(sub3.contar, 0) AS conta_recuperado,
    COALESCE(sub4.contar, 0) AS conta_fechado,
    COALESCE(sub5.contar, 0) AS conta_recusado,
    COALESCE(sub6.contar, 0) AS conta_residencial,
    COALESCE(sub7.contar, 0) AS conta_comercio,
    COALESCE(sub8.contar, 0) AS conta_terreno_baldio,
    COALESCE(sub9.contar, 0) AS conta_outros,
    COALESCE(sub10.contar, 0) AS conta_ponto_estrategico,
    COALESCE(sub11.contar, 0) AS conta_pp, 
    COALESCE(sub12.contar, 0) AS conta_larvicida, 
    COALESCE(sub13.contar, 0) AS conta_foco
FROM (
    SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id
    WHERE 
        DATE(v.date_time) = '2024-09-10'  
    GROUP BY 
        a.nome
) AS sub
LEFT JOIN (
    SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id
    WHERE 
        v.situacao_visita_id = 4 
        AND DATE(v.date_time) = '2024-09-10' 
    GROUP BY 
        a.nome
) AS sub2 ON sub.nome = sub2.nome
LEFT JOIN (
    SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id
    WHERE 
        v.situacao_visita_id = 7 
        AND DATE(v.date_time) = '2024-09-10'  
    GROUP BY 
        a.nome
) AS sub3 ON sub.nome = sub3.nome
LEFT JOIN (
    SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id
    WHERE 
        v.situacao_visita_id = 6 
        AND DATE(v.date_time) = '2024-09-10'  
    GROUP BY 
        a.nome
) AS sub4 ON sub.nome = sub4.nome
LEFT JOIN (
    SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    WHERE 
        v.situacao_visita_id = 5 
        AND DATE(v.date_time) = '2024-09-10' 
    GROUP BY 
        a.nome
) AS sub5 ON sub.nome = sub5.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id
    WHERE 
        i.tipo_imovel_id = 1
        AND DATE(v.date_time) = '2024-09-10'  
    GROUP BY 
        a.nome
) AS sub6 ON sub.nome = sub6.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id
    WHERE 
        i.tipo_imovel_id = 2
        AND DATE(v.date_time) = '2024-09-10'  
    GROUP BY 
        a.nome
) AS sub7 ON sub.nome = sub7.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id
    WHERE 
        i.tipo_imovel_id = 3
        AND DATE(v.date_time) = '2024-09-10'  
    GROUP BY 
        a.nome
) AS sub8 ON sub.nome = sub8.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id
    WHERE 
        i.tipo_imovel_id = 8
        AND DATE(v.date_time) = '2024-09-10'  
    GROUP BY 
        a.nome
) AS sub9 ON sub.nome = sub9.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id
    WHERE 
        i.tipo_imovel_id = 9
        AND DATE(v.date_time) = '2024-09-10' 
    GROUP BY 
        a.nome
) AS sub10 ON sub.nome = sub10.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id
    WHERE 
        i.tipo_imovel_id = 10
        AND DATE(v.date_time) = '2024-09-10'
    GROUP BY 
        a.nome
) AS sub11 ON sub.nome = sub11.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id 
    JOIN visita_imovel vi ON vi.id_visita = v.id
    WHERE 
        vi.larvicida_id <> 1
        AND DATE(v.date_time) = '2024-09-10' 
    GROUP BY 
        a.nome
) AS sub12 ON sub.nome = sub12.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id
    JOIN visita_imovel vi ON vi.id_visita = v.id
    JOIN resp_questao rq ON rq.id_visita_imovel = vi.id
    WHERE 
        rq.resposta = "Y"
        AND DATE(v.date_time) = '2024-09-10'  
    GROUP BY 
        a.nome
) AS sub13 ON sub.nome = sub13.nome

'''


def query_resumo_producao_semanal(data_inicial, data_final, id_agente):
    return f'''

SELECT 
    sub.nome,
    COALESCE(sub.contar, 0) AS total_contar,
    COALESCE(sub2.contar, 0) AS conta_visitado,
    COALESCE(sub3.contar, 0) AS conta_recuperado,
    COALESCE(sub4.contar, 0) AS conta_fechado,
    COALESCE(sub5.contar, 0) AS conta_recusado,
    COALESCE(sub6.contar, 0) AS conta_residencial,
    COALESCE(sub7.contar, 0) AS conta_comercio,
    COALESCE(sub8.contar, 0) AS conta_terreno_baldio,
    COALESCE(sub9.contar, 0) AS conta_outros,
    COALESCE(sub10.contar, 0) AS conta_ponto_estrategico,
    COALESCE(sub11.contar, 0) AS conta_pp, 
    COALESCE(sub12.contar, 0) AS conta_larvicida, 
    COALESCE(sub13.contar, 0) AS conta_foco
FROM (
    SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id
    WHERE 
        v.date_time BETWEEN '{data_inicial} 00:00:00' AND '{data_final} 23:59:00'
        AND v.agente_id = {id_agente}
    GROUP BY 
        a.nome
) AS sub
LEFT JOIN (
    SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id
    WHERE 
        v.situacao_visita_id = 4 
        AND v.date_time BETWEEN '{data_inicial} 00:00:00' AND '{data_final} 23:59:00'
        AND v.agente_id = {id_agente}
    GROUP BY 
        a.nome
) AS sub2 ON sub.nome = sub2.nome
LEFT JOIN (
    SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id
    WHERE 
        v.situacao_visita_id = 7 
        AND v.date_time BETWEEN '{data_inicial} 00:00:00' AND '{data_final} 23:59:00'
        AND v.agente_id = {id_agente}
    GROUP BY 
        a.nome
) AS sub3 ON sub.nome = sub3.nome
LEFT JOIN (
    SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id
    WHERE 
        v.situacao_visita_id = 6 
        AND v.date_time BETWEEN '{data_inicial} 00:00:00' AND '{data_final} 23:59:00'
        AND v.agente_id = {id_agente}
    GROUP BY 
        a.nome
) AS sub4 ON sub.nome = sub4.nome
LEFT JOIN (
    SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    WHERE 
        v.situacao_visita_id = 5 
        AND v.date_time BETWEEN '{data_inicial} 00:00:00' AND '{data_final} 23:59:00'
        AND v.agente_id = {id_agente}
    GROUP BY 
        a.nome
) AS sub5 ON sub.nome = sub5.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id
    WHERE 
        i.tipo_imovel_id = 1
        AND v.date_time BETWEEN '{data_inicial} 00:00:00' AND '{data_final} 23:59:00'
        AND v.agente_id = {id_agente} and v.situacao_visita_id = 4 
    GROUP BY 
        a.nome
) AS sub6 ON sub.nome = sub6.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id
    WHERE 
        i.tipo_imovel_id = 2
        AND v.date_time BETWEEN '{data_inicial} 00:00:00' AND '{data_final} 23:59:00'
        AND v.agente_id = {id_agente} and v.situacao_visita_id = 4 
    GROUP BY 
        a.nome
) AS sub7 ON sub.nome = sub7.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id
    WHERE 
        i.tipo_imovel_id = 3
        AND v.date_time BETWEEN '{data_inicial} 00:00:00' AND '{data_final} 23:59:00'
        AND v.agente_id = {id_agente} and v.situacao_visita_id = 4 
    GROUP BY 
        a.nome
) AS sub8 ON sub.nome = sub8.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id
    WHERE 
        i.tipo_imovel_id = 8
        AND v.date_time BETWEEN '{data_inicial} 00:00:00' AND '{data_final} 23:59:00'
        AND v.agente_id = {id_agente} and v.situacao_visita_id = 4 
    GROUP BY 
        a.nome
) AS sub9 ON sub.nome = sub9.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id
    WHERE 
        i.tipo_imovel_id = 9
        AND v.date_time BETWEEN '{data_inicial} 00:00:00' AND '{data_final} 23:59:00'
        AND v.agente_id = {id_agente} and v.situacao_visita_id = 4 
    GROUP BY 
        a.nome
) AS sub10 ON sub.nome = sub10.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id
    WHERE 
        i.tipo_imovel_id = 10
        AND v.date_time BETWEEN '{data_inicial} 00:00:00' AND '{data_final} 23:59:00'
        AND v.agente_id = {id_agente} and v.situacao_visita_id = 4 
    GROUP BY 
        a.nome
) AS sub11 ON sub.nome = sub11.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id 
    JOIN visita_imovel vi ON vi.id_visita = v.id
    WHERE 
        vi.larvicida_id <> 1
        AND v.date_time BETWEEN '{data_inicial} 00:00:00' AND '{data_final} 23:59:00'
        AND v.agente_id = {id_agente} and v.situacao_visita_id = 4 
    GROUP BY 
        a.nome
) AS sub12 ON sub.nome = sub12.nome
LEFT JOIN (
     SELECT 
        a.nome,
        COUNT(v.id) AS contar
    FROM 
        visita v
    JOIN 
        agente a ON a.id = v.agente_id  
    JOIN imovel i ON i.id = v.imovel_id
    JOIN visita_imovel vi ON vi.id_visita = v.id
    JOIN resp_questao rq ON rq.id_visita_imovel = vi.id
    WHERE 
        rq.resposta = "Y"
        AND v.date_time BETWEEN '{data_inicial} 00:00:00' AND '{data_final} 23:59:00'
        AND v.agente_id = {id_agente} and v.situacao_visita_id = 4 
    GROUP BY 
        a.nome
) AS sub13 ON sub.nome = sub13.nome

'''

def query_visitas_horario(data_inicial, data_final, id_agente):
    return f'''

SELECT 
    DATE_FORMAT(v.date_time, '%H') AS Hora,
    COUNT(v.id) AS "Numero de Visitas"
FROM 
    visita v
WHERE 
    v.date_time BETWEEN '{data_inicial} 00:00:00' AND '{data_final} 23:59:00'
    AND v.agente_id = {id_agente}
GROUP BY 
    hora

''' 