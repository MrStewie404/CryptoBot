import sqlite3
import json

class ORM:
    def __init__(self, db_file: str = 'users.db'):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def add_user(self, user_id) -> str:
        try:
            self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
            self.conn.commit()
            return 'Вы успешно создали профиль!'
        except Exception as e:
            print(e)
            return 'Сожалею, но профиль уже создан.\n\nПиши в лс разрабу, если считаешь, что произошла ошибка ;)'

    def get_user_money(self, user_id) -> float:
        result = self.cursor.execute('SELECT money FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
        return json.loads(result)

    def update_user_money(self, coin, user_id) -> None:
        self.cursor.execute('UPDATE users SET money = ? WHERE user_id = ?', (json.dumps(coin), user_id,))
        return self.conn.commit()
    
    def add_cource(self, coin, amount):
        self.cursor.execute(f'INSERT INTO values (`time`, `amount`) VALUES (?,?)', (coin, amount,))
        return self.conn.commit()
    
    def add_buy(self, amount, user_id):
        self.cursor.execute(f'UPDATE users SET buy = ? WHERE user_id = ?', (json.dumps(amount), user_id,))
        return self.conn.commit()

    def get_buy(self, user_id) -> dict:
        result = self.cursor.execute(f'SELECT buy FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
        return json.loads(result)