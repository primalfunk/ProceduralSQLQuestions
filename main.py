import sys
from ui import SQLAppUI
from database import DatabaseManager
from challenge import ChallengeManager
from PyQt6.QtWidgets import QApplication, QTableWidgetItem


class SQLApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ui = SQLAppUI()
        self.db = DatabaseManager('localhost', 'root', 'RowanDaniel1011!', 'challenger')
        self.ui.runButtonClicked.connect(self.execute_query)
        self.ui.submitButtonClicked.connect(self.submit_answer)
        self.db.connect()
        self.challenge = ChallengeManager(self.db)
        self.ui.parent = self

    def execute_query(self):
        query = self.ui.codeEditor.toPlainText()
        print(f"Executing query: {query}")  # Debugging print
        result = self.db.execute_query(query)
        print(f"Query result: {result}")  # Debugging print
        self.ui.queryResultsTable.setRowCount(0)
        self.ui.queryResultsTable.setColumnCount(0)
        if result and isinstance(result, list):
            headers = [description[0] for description in self.db.cursor.description]
            self.ui.queryResultsTable.setColumnCount(len(headers))
            self.ui.queryResultsTable.setHorizontalHeaderLabels(headers)
            for row_data in result:
                row = self.ui.queryResultsTable.rowCount()
                self.ui.queryResultsTable.insertRow(row)
                for column, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    self.ui.queryResultsTable.setItem(row, column, item)
        self.ui.queryResultsTable.resizeColumnsToContents()

    def submit_answer(self):
        user_query = self.ui.codeEditor.toPlainText()
        is_correct = self.challenge.validate_answer(user_query)
        message = "Correct!" if is_correct else "Incorrect. Try again."
        self.ui.queryResults.setText(message)

    def run(self):
        challenge_question, _ = self.challenge.load_challenge()  # Load challenge and get the question
        schema_ascii_art = self.challenge.get_ascii_representation(self.challenge.current_schema)
        self.ui.infoPanel.setText('Challenge Question\n\n' + challenge_question + '\n\n' + schema_ascii_art)
        self.ui.show()
        sys.exit(self.app.exec())


if __name__ == '__main__':
    app = SQLApp()
    app.run()