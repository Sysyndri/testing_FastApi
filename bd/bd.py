import sqlite3
from typing import Dict, List
from uuid import UUID


class BD:
    def __init__(self, db_path: str = 'wallet.bd'):
        self._conn = sqlite3.connect(db_path)
        self._cur = self._conn.cursor()

        self.create_table()

    def create_table(self) -> None:
        self._cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS wallet (
            id BLOB PRIMARY KEY,
            wallet_balance INTEGER NOT NULL)
            ''')

        self._conn.commit()

    def add_date(self, date: List[Dict[str, UUID | int]]) -> None:
        for line in date:
            id = line['id'].bytes
            balance = line['wallet_balance']

            self._cur.execute(
                '''
                INSERT INTO wallet (id, wallet_balance) VALUES (?, ?)
                ''',
                (id, balance, )
            )

        self._conn.commit()

    def get_wallet(self, id_wallet: UUID) -> Dict[str, bytes | int] | None:
        id_wallet = id_wallet.bytes

        cursor = self._conn.cursor()
        cursor.execute(
            '''
            SELECT * FROM wallet WHERE id = ?
            ''',
            (id_wallet, )
        )

        return cursor.fetchone()

    def change_wallet(self, id_wallet: UUID, wallet_balance: int, operation: bool):
        cursor = self._conn.cursor()

        if operation:
            cursor.execute(
                '''
                UPDATE wallet SET wallet_balance = wallet_balance + ? WHERE id = ?
                ''',
                (wallet_balance, id_wallet.bytes, )
            )
        else:
            balance = cursor.execute(
                '''
                SELECT wallet_balance FROM wallet WHERE id = ?
                ''',
                (id_wallet.bytes, )
            ).fetchone()[0]

            if balance >= wallet_balance:
                cursor.execute(
                    '''
                    UPDATE wallet SET wallet_balance = wallet_balance - ? WHERE id = ?
                    ''',
                    (wallet_balance, id_wallet.bytes, )
                )
            else:
                return f'Недостаточно средств на балансе кошелька - {id_wallet}'

    def close_connection(self) -> None:
        self._conn.close()
        self._cur.close()

