# webscraper-petlove
Bot de WebScraping feito para raspar dados da PetLove


O bot foi criado em Março de 2025, mas apenas agora foi cirado seu Repositório no Github

Seu modo de funcionamento: Ele joga as palavras na lista searchwords na barra de pesquisa, coleciona os links de produtos que foi consultado. Apos colecionar todos os links, raspa os dados gerais como nome, marca, preço, tamanho, descrição, avaliações e notas de avaliações. 

Volumetria de dados bem grande, é recomendado rodar menos searchwords de cada vez ou rodar o bot em paralelo em varias instancias com pares diferentes de searchwords.

Algumas vezes o bot não ira paginar na pagina de pesquisa, colecionando os links apenas da primeira pagina de consulta, rodar o bot em paralelo em multiplas instancias com menos searchwords funcionou.
