

import time, urllib.request
import requests
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from datetime import datetime

### PALAVRAS A SEREM BUSCADAS NA PETLOVE

searchwords = [
'Petisco Natural Caẽs',
'Petisco natural'
,'Petisco calmante'
,'Hipoalergenico'
,'Gastro'
,'Mordedor natural'
,'mordedor'
,'Brinquedo natural'
,'Alimentação natural fresca'
,'Bifinho'
,'Bifinho Natural'
,'Bifinho Super Premium' 
,'petisco Super Premium'
,'Petisco hipoalergenico'
,'Bifinho hipoalergenico'
,'tenebrio'
,'insect'
,'inseto'
,'petisco suplementoso'
,'suplemento animal']


### JUNTANDO TUDO NUMA CÉLULA SÓ
## INICIO
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
links_lista = []
url_scrape = 'https://www.petlove.com.br'
init_ops = str(datetime.now())
driver.get(url_scrape)
print(f'Acessando a Petlove: {init_ops}')
driver.set_window_size(1920, 1080)
time.sleep(5)

### AQUI VAMOS ITERAR POR CADA PALAVRA DE BUSCA, PEGAR OS LINKS E COMEÇAR A SCRAPAR

lista_consol = []

#searchwords  = searchwords[19:20] ## PARA TESTES, COMENTE DEPOIS

for word in searchwords:
    search = driver.find_element(By.CLASS_NAME, "search__input-petlove")
    search.click()
    search.send_keys(f"{word}" + Keys.ENTER)
    p = 1
    print(f'{datetime.now()}: Iniciando procura por {word}')


    time.sleep(5)


    while True:
        try:
            i = 0
            while i < 10:
                actions = ActionChains(driver)    ## SCROLL
                actions.scroll_by_amount(0,500)
                actions.perform()
                time.sleep(1)
                i +=1


            links = driver.find_elements(By.TAG_NAME, 'a')     ## ARMAZENANDO OS LINKS DE CADA PRODUTO
            for link in links:
                produto = link.get_attribute('href')
                if '/p?sku' in produto:       
                    links_lista.append(produto)
            try:
                next = driver.find_element(By.CSS_SELECTOR, "svg.link__icon.ml-3")
                next.click()
                p +=1
                print(f'{datetime.now()}: Indo para a pagina de indice {p}')
            except:
                print(f"Não tem mais paginas para produtos associados à {word}")
                break
        except:
            break
    links_lista = pd.DataFrame(links_lista, columns=['Links'])     ### COLOCANDO OS LINKS EM CADA PALAVRA DE BUSCA EM UMA LISTA
    links_lista['Palavra_Busca'] = word       
    lista_consol.append(links_lista)                     

links_lista = pd.concat(lista_consol, ignore_index=True)

#links_lista =  links_lista[0:1] ### PARA TESTES, COMENTE DEPOIS
print(f'Iniciando webscraping de produtos, {len(links_lista)} links estão na nossa lista')



#### DECLARAÇÃO DE VARIAVEIS, LISTAS, URL

nome_produto = []    
nota_produto = []
resumo_produto = []
preco_produto = []
tamanho_produto = []
comentarios_produtos = []
titulo_comentario = []
qtde_aval = []
qtde_perg = []
qtde_resp = []
marca_produto = []

perguntas_produto = []
nome_interrogador = []
data_pergunta = []


review_nota = []
nome_comentarista = []
data_comentario = []


lista_comentarios = []
lista_perguntas = []
lista_prod_consol = []

j = 0
erros = 0
acertos = 0

while j < len(links_lista['Links']):
    link_produto = links_lista['Links'][j]
    i = 0   
    driver.get(link_produto)     ### SCRAPING DO PRODUTO POR SUA PAGINA
    driver.set_window_size(1920, 1080)
    try:    ### PULAR PRA PROXIMA PAGINA EM CASO DE ERRO
        name = driver.find_element(By.CSS_SELECTOR, 'h1.mt-5.font-title-xs.font-medium.color-neutral-darkest')
        continue_click = driver.find_element(By.CSS_SELECTOR, 'div.align-self-end.cursor-pointer.color-primary.font-body-s.font-bold')
        continue_click.click()
        summary = driver.find_element(By.CSS_SELECTOR, 'div.product__summary__info')
        aval = driver.find_element(By.CSS_SELECTOR, "strong.pr-3.ml-2.mr-3.font-body-s.color-neutral-dark.ratings-shortcut")
        price = driver.find_elements(By.CSS_SELECTOR, "span.font-body-s")
        size = driver.find_element(By.CSS_SELECTOR, "span.font-bold.font-body.mb-2")
        qty_rev = driver.find_element(By.CSS_SELECTOR, "span.ml-3.font-body-s.font-bold.ml-3")
        qty_ans = driver.find_elements(By.CSS_SELECTOR, "span.ml-3.font-body-s.font-bold.ml-3")
        href_links = driver.find_elements(By.CSS_SELECTOR, 'a.mx-2.color-primary')

        ## APENDICE DE LISTAS
        for href_link in href_links:
            brand_link = href_link.get_attribute('href')
            if '/marcas/' in brand_link:
                marca_produto.append(brand_link[34:])
        resumo_produto.append(summary.text)   
        nome_produto.append(name.text)
        nota_produto.append(aval.text)
        preco_produto.append(price[2].text.strip('R$'))
        tamanho_produto.append(size.text)
        qtde_aval.append(qty_rev.text)
        qtde_resp.append(qty_ans[1].text)
        ## SCROLLAR A PAGINA ATE O FIM
        while i < 7: 
            actions = ActionChains(driver)
            actions.scroll_by_amount(0,800)
            actions.perform()
            time.sleep(1)
            i +=1
        ### SCROLLAR AS AVALIAÇÕES    
        time.sleep(3)
        cards = driver.find_elements(By.CSS_SELECTOR, 'div.card.card-accordion.card--shadow.card-accordion--padding7')
        for card in cards: 
            if card.text == 'Avaliações':    ### CLICANDO NO CARD CERTO
                card.click()
                i = 0
                while i < (int(qty_rev.text)/2):
                    actions.scroll_by_amount(0,300)   ## SCROLL DO CARD PELA METADE DE QUANTIDADE DE COMENTARIOS, GERALMENTE CONSIGO
                    actions.perform()                 ## TODOS OS COMENTARIOS DESSA FORMA
                    time.sleep(1)
                    try:
                        more = driver.find_element(By.CSS_SELECTOR, "button.button.col-12.col-xl-4.button--secondary.button--small.button--full")
                        more.click()       ## AQUI, SE CLICA NO CARD DE MOSTRAR MAIS AVALIAÇÕES
                    except: 
                        pass
                    i +=1
        ratings = driver.find_elements(By.CSS_SELECTOR, "div.rating__stars")    ### ITERANDO POR HEADER DE COMENTARIO, PARA CONSEGUIR SOMAR CADA ESTRELA DE AVALIAÇÃO
        for rating in ratings:                                                  ### EXISTE UM IDENTIFICADOR PATH PARA AS ESTRTELAS PREENCHIDAS, DESSA FORMA EU TENTO SOMAR QUANTAS ESTRELAS FORAM PREENCHIDAS E CONSEGUIR ESTIMAR A NOTA
            lista_path = []
            rev_stars = rating.find_elements(By.CSS_SELECTOR, "svg.fill-alert.svg-16")
            k=0
            for rev_star in rev_stars:
                star_condition = rev_star.find_elements(By.TAG_NAME, 'path')
                for condition in star_condition:
                    path = condition.get_attribute('d')
                    if 'M12' in path:                           ### O IDENTIFICADOR EM QUESTÃO
                        k +=1
            review_nota.append(k)
        header_pet = driver.find_elements(By.CSS_SELECTOR, "header.mb-5")   ### NOME DO COMENTARISTA E DATA DO COMENTARIO
        for header in header_pet:
            name_cmmt = header.find_element(By.CSS_SELECTOR,"span.font-bold")
            data_cmmt = header.find_element(By.CSS_SELECTOR, "div.font-body-s.color-neutral")
            data_comentario.append(data_cmmt.text.split('em')[1])
            nome_comentarista.append(name_cmmt.text)
        comments = driver.find_elements(By.CSS_SELECTOR, "p.font-body-s.font-regular.color-neutral.mb-5")   ## COMENTARIOS E TITULO DO COMENTARIO
        for comment in comments:
            comentarios_produtos.append(comment.text)
        title_comment = driver.find_elements(By.CSS_SELECTOR, "div.font-body.font-bold.color-neutral-dark.mb-3")
        for title in title_comment:
            titulo_comentario.append(title.text)
        ### SCROLLAR AS PERGUNTAS
        #cards = driver.find_elements(By.CSS_SELECTOR, 'div.card.card-accordion.card--shadow.card-accordion--padding7')
        #for card in cards:
        #    try:
        #        if card.text == 'Perguntas':
        #            card.click()
        #            i = 0
        #            while i < 10:
        #                actions.scroll_by_amount(0,300)
        #                actions.perform()
        #                time.sleep(1)
        #                try:
        #                    more = driver.find_element(By.CSS_SELECTOR, "button.button.col-12.col-xl-3.button--secondary.button--small.button--full")
        #                    more.click()
        #                except: 
        #                    pass
        #                i +=1
        #    except:
        #        pass
        #questions = driver.find_elements(By.CSS_SELECTOR, "div.chat__message.chat__message--received")
        #for question in questions:
        #    perguntas_produto.append(question.text)
        #### AQUI, PEGAMOS AS PERGUNTAS
        #cards = driver.find_elements(By.CSS_SELECTOR, 'div.card.card-accordion.card--shadow.card-accordion--padding7')
        #for card in cards: 
        #    if card.text == 'Perguntas':
        #        card.click()
        #        i = 0
        #        while i < 10:
        #            actions.scroll_by_amount(0,300)
        #            actions.perform()
        #            time.sleep(1)
        #            try:
        #                more = driver.find_element(By.CSS_SELECTOR, "button.button.col-12.col-xl-3.button--secondary.button--small.button--full")
        #                more.click()
        #            except: 
        #                pass
        #            i +=1
        #questions = driver.find_elements(By.CSS_SELECTOR, "div.chat__message.chat__message--received")
        #for question in questions:
        #    perguntas_produto.append(question.text)
        #question_name_box = driver.find_elements(By.CSS_SELECTOR, "div.mt-5.font-body-s")
        #for name_box in question_name_box:
        #    nome_interrogador.append(name_box.text.split('em')[0])
        #    data_pergunta.append(name_box.text.split('em')[1])
        #qtde_perg.append((len(perguntas_produto)))
        ## AQUI, SALVAMOS OS DATAFRAMES
        max_length = max(len(titulo_comentario), len(review_nota), len(nome_comentarista), len(comentarios_produtos), len(data_comentario)) 
        titulo_comentario += [''] * (max_length - len(titulo_comentario))
        review_nota += [0] * (max_length - len(review_nota))
        nome_comentarista += [''] * (max_length - len(nome_comentarista))
        comentarios_produtos += [''] * (max_length - len(comentarios_produtos))
        data_comentario += [''] * (max_length - len(data_comentario))
        df_cmmt = pd.DataFrame({'Título': titulo_comentario, 'Nota_Avaliação': review_nota, 'Nome_Comentario': nome_comentarista,
                                 'Comentários': comentarios_produtos, 'Data_Comentario': data_comentario}).fillna('NA')
        df_cmmt['Marca'] = brand_link[34:]
        df_cmmt['Produto'] = name.text
        df_cmmt['Link'] = link_produto
        df_cmmt['Palavra_Chave'] = links_lista['Palavra_Busca'][j]
        #df_perg = pd.DataFrame({'Perguntas': perguntas_produto})
        #df_perg['Marca'] = brand_link[34:]
        #df_perg['Produto'] = name.text
        #df_perg['Link'] = link_produto
        #df_perg['Palavra_Chave'] = links_lista['Palavra_Busca'][j]
        lista_comentarios.append(df_cmmt)
        #lista_perguntas.append(df_perg)
        prd_dict = {'Nome_Produto': nome_produto,'Marca_Produto': marca_produto,  'Nota_Produto': nota_produto, 'Resumo_Descrição': resumo_produto, 
                'Preço': preco_produto, 'Tamanho': tamanho_produto, 'Qtde_Aval': qtde_aval
                ,'Qtde_Resp': qtde_resp
                , 'Link': link_produto, 'Palavra_Chave': links_lista['Palavra_Busca'][j]}
        df_prod = pd.DataFrame(prd_dict)
        print(f'{datetime.now()}:link de índice {j} foi scrapado com sucesso, indo para o próximo link de índice {j+1}')
        acertos += 1
        j += 1
    except Exception as e:
        print(e)
        print(f'{datetime.now()}:link de índice {j} incidiu em erro, pulando para o próximo link de índice {j+1}')
        erros += 1
        j +=1
driver.close()


cmmt_consolidado = pd.concat(lista_comentarios, ignore_index=True)
#perg_consolidado = pd.concat(lista_perguntas, ignore_index=True)

print(f'{datetime.now(): Salvando os dados em csv}')

df_prod.to_csv(f'ProdutosPetloveScrape{datetime.now()}')
cmmt_consolidado.to_csv(f'ComentariosPetlove{datetime.now()}')
#perg_consolidado.to_csv(f'PerguntasPetlove{datetime.now()}')



print(f'finalização do processo às {datetime.now()}, houveram {acertos} links bem-sucedidos, e {erros} links que falharam')