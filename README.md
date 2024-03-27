# Ponderada-Flask-Robo

Este projeto integra um servidor Flask com HTMX para oferecer controle interativo de um robô via web. Destina-se a proporcionar uma interface amigável para comandar ações do robô, como movimentação e operação de atuadores, bem como para visualizar o status e a posição atual do robô, tudo em tempo real e sem a necessidade de recarregar a página.

## Recursos

- **Movimentação do Robô**: Comande o robô para mover-se a posições especificadas.
- **Controle do Atuador**: Ligue e desligue o atuador do robô.
- **Consulta da Posição Atual**: Veja a posição atual do robô em tempo real.
- **Log de Atividades**: Monitore um histórico de ações executadas pelo robô.

## Tecnologias Utilizadas

- **[Flask](https://flask.palletsprojects.com/)**: Framework web para o servidor back-end.
- **[HTMX](https://htmx.org/)**: Permite interações dinâmicas na página web, facilitando a comunicação com o servidor sem recarregar a página.
- **[Bootstrap](https://getbootstrap.com/)**: Framework para desenvolvimento de componentes de interface responsivos.
- **[Bootstrap Icons](https://icons.getbootstrap.com/)**: Conjunto de ícones para enriquecer a interface do usuário.

## Configuração do Ambiente

Para configurar seu ambiente de desenvolvimento e executar o projeto localmente, siga estes passos:

1. Clone o repositório:

    ```bash
    git clone https://github.com/AntonioArtimonte/Ponderada-Flask-Robo.git
    ```

2. Entre no diretório do projeto:

    ```bash
    cd Ponderada-Flask-Robo
    ```

3. Instale as dependências utilizando `pip`:

    ```bash
    pip install -r requirements.txt
    ```

## Execução

Para rodar o servidor Flask e acessar a interface web:

```bash
flask run
