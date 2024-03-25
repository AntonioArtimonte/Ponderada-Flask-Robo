# db_manager.py

from tinydb import TinyDB, Query
from datetime import datetime

class RobotPositionDB:
    def __init__(self, db_path):
        """
        Inicializa o banco de dados.

        :param db_path: Caminho para o arquivo do banco de dados.
        """
        self.db = TinyDB(db_path)
        self.table = self.db.table('robot_positions')

    def insert_position(self, x, y, z, r, work):
        """
        Insere uma nova posição na tabela.

        :param x: Coordenada X.
        :param y: Coordenada Y.
        :param z: Coordenada Z.
        :param r: Rotação R.
        """
        self.table.insert({
            'date_inserted': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'x': x,
            'y': y,
            'z': z,
            'r': r,
            'work': work
        })

    def get_all_data(self):
        """
        Recupera todas as posições armazenadas.

        :return: Lista de todas as posições.
        """
        return self.table.all()
