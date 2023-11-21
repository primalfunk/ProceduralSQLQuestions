from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QSplitter, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import pyqtSignal, Qt

class SQLAppUI(QMainWindow):
    runButtonClicked = pyqtSignal(str)
    submitButtonClicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Initialize the UI components and layout
        self.setWindowTitle('SQL Challenge App')
        self.setGeometry(100, 100, 800, 600)

        # Create a horizontal splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Info Panel with Label
        infoPanelContainer = QVBoxLayout()
        infoPanelLabel = QLabel("Challenge Information")
        self.infoPanel = QTextEdit()
        self.infoPanel.setReadOnly(True)
        infoPanelContainer.addWidget(infoPanelLabel)
        infoPanelContainer.addWidget(self.infoPanel)

        infoPanelWidget = QWidget()
        infoPanelWidget.setLayout(infoPanelContainer)
        splitter.addWidget(infoPanelWidget)

        # Right side container (for codeEditor, queryResults, and their labels)
        rightSideContainer = QWidget()
        rightSideLayout = QVBoxLayout()

        # Code Editor with Label
        codeEditorLabel = QLabel("Enter Your SQL Query Here")
        self.codeEditor = QTextEdit()
        rightSideLayout.addWidget(codeEditorLabel)
        rightSideLayout.addWidget(self.codeEditor)

        # Query Results with Label
        queryResultsLabel = QLabel("Query Results")
        self.queryResultsTable = QTableWidget()
        rightSideLayout.addWidget(queryResultsLabel)
        rightSideLayout.addWidget(self.queryResultsTable)

        # Run and Submit Buttons
        self.runButton = QPushButton('Run')
        self.submitButton = QPushButton('Submit')
        rightSideLayout.addWidget(self.runButton)
        rightSideLayout.addWidget(self.submitButton)

        rightSideContainer.setLayout(rightSideLayout)
        splitter.addWidget(rightSideContainer)

        # Set initial sizes to achieve a 30%-70% split
        splitter.setSizes([240, 560])

        # Set splitter as central widget
        self.setCentralWidget(splitter)

        # Connect button signals
        self.runButton.clicked.connect(self.onRunClicked)
        self.submitButton.clicked.connect(self.onSubmitClicked)

    def onRunClicked(self):
        query = self.codeEditor.toPlainText()
        self.runButtonClicked.emit(query)  # Emit the signal with the query

    def onSubmitClicked(self):
        user_query = self.codeEditor.toPlainText()
        self.submitButtonClicked.emit(user_query)  # Emit the signal with the query
    
    def closeEvent(self, event):
        self.parent.db.close()
        super().closeEvent(event)