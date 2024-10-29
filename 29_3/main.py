
"""T 29.3 Скласти програму для роботи з базою даних, що містить означення
понять та їх опис. Реалізувати функції додавання поняття та повернення
опису за введеним поняттям."""
import sqlite3
import os

class DBDictionary:
    '''Клас для ведення словника з використанням бази даних.

       База даних містить 1 таблицю з полями:
        term - термін
        definition - опис терміна

       Поля:
       self.filename - ім'я файлу бази даних
    '''
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(filename):
            self.create_db()

    def create_db(self):
        '''Створює словник та записує у нього n термінів.'''
        conn = sqlite3.connect(self.filename)   
        curs = conn.cursor()                   
        curs.execute('''CREATE TABLE dictionary
                        (term text PRIMARY KEY, definition text)''')
        n = int(input('Кількість термінів для додавання: '))
        for i in range(n):
            term = input('Термін: ')
            definition = input('Опис терміна: ').lower()
            curs.execute("INSERT INTO dictionary (term, definition) VALUES (?, ?)", (term, definition))
        conn.commit()                           
        conn.close()                            

    def add_term(self):
        '''Доповнює словник одним терміном.'''
        conn = sqlite3.connect(self.filename)   
        curs = conn.cursor()                    
        term = input('Термін: ').lower()
        definition = input('Опис терміна: ')
        try:
            curs.execute("INSERT INTO dictionary (term, definition) VALUES (?, ?)", (term, definition))
            conn.commit()                     
        except sqlite3.IntegrityError:
            print("Термін вже існує.")
        finally:
            conn.close()                       

    def search_definition(self, term):
        '''Шукає у словнику опис терміна term.

        Якщо не знайдено, повертає порожній рядок.
        '''
        term = term.lower()
        conn = sqlite3.connect(self.filename)  
        curs = conn.cursor()                    
        curs.execute("SELECT definition FROM dictionary WHERE term=?", (term,))
        result = curs.fetchone()
        conn.close()
        return result[0] if result else ""


if __name__ == '__main__':
    filename = 'dictionary.db'  
    db = DBDictionary(filename)

    while True:
        print("\nМеню:")
        print("1 - Додати термін")
        print("2 - Знайти опис терміна")
        print("3 - Вихід")
        choice = int(input('Оберіть дію (1-3): '))
        
        if choice == 1:  
            db.add_term()
        elif choice == 2:  
            term = input('Введіть термін: ')
            definition = db.search_definition(term)
            if definition:
                print('Опис:', definition)
            else:
                print('Термін не знайдено.')
        elif choice == 3:
            print('Вихід з програми.')
            break
        else:
            print('Неправильний вибір. Спробуйте ще раз.')
