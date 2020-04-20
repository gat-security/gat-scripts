# INTRODUÇÃO
Scripts que leem arquivos exportados ou APIs de ferramentas terceiras e fazem o input das informações no GAT.

# COMO USAR
1. Clone o repositório em sua máquina
2. Altere o arquivo ```src/gat_api/config``` adicionando a sua chave de API e o subdomínio do seu GAT
3. Acesse a pasta ```src/``` e rode o comando ```python3 main.py <ferramenta> [arquivo]```
   1. Por exemplo: ```python3 main.py openvas ~/user/openvas.csv```
   2. A lista de ferramentas disponíveis será atualizada constantemente (ela pode ser vista mais abaixo)
4. Veja abaixo detalhes sobre cada integração disponível


# OPENVAS
Para utilizar o script de integração com o OpenVAS, é necessário fazer um scan e exportar os resultados em CSV.
Com o arquivo de resultados do scan em CSV baixado, basta acessar a pasta ```src/``` e rodar o comando ```python3 main.py openvas /caminho/para/o/arquivo.csv```.