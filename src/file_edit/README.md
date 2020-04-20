# INTRODUÇÃO
Scripts utilizados para editar arquivos exportados de ferramentas terceiras (Nessus, Acunetix, Veracode, etc) a fim de facilitar sua importação no GAT.

# COMO USAR
1. Clone o repositório em sua máquina
2. Altere o arquivo ```src/gat_api/config``` adicionando a sua chave de API e o subdomínio do seu GAT
3. Acesse a pasta ```src/file_edit/``` e rode o comando ```python3 <ferramenta>.py <arquivo>```
   1. Por exemplo: ```python3 openvas.py ~/user/openvas.csv```
   2. A lista de ferramentas disponíveis será atualizada constantemente (ela pode ser vista mais abaixo)
4. Veja abaixo detalhes sobre cada script disponível


# OPENVAS
Para utilizar o script de integração com o OpenVAS, é necessário fazer um scan e exportar os resultados em CSV.
Com o arquivo de resultados do scan em CSV baixado, basta acessar a pasta ```src/``` e rodar o comando ```python3 openvas.py /caminho/para/o/arquivo.csv```.
O script irá alterar o arquivo para que seja possível fazer a importação do mesmo utilizando a funcionalidade de Custom Parser do GAT.
Seguindo [esse guia](https://helpgat.zendesk.com/hc/pt/articles/360045826014-Como-configurar-e-usar-o-OpenVAS-junto-com-o-GAT), o script automatiza a seção **"Ajuste do arquivo CSV para importar no GAT"**.