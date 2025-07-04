#Modules

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, \
    QVBoxLayout, QHBoxLayout, QTableWidgetItem, QCheckBox
import openpyxl
import os
from odf.opendocument import load
from PyQt5.QtCore import Qt, QDate
from odf.text import P
import pandas as pd

class ExpenseAPP(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1000, 900)
        self.setWindowTitle("SQL Expese")

        self.row_count = 0

        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Food", "Transport", "Utilities", "Entertainment", "Other"])
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.add_button = QPushButton("Add Cost")
        self.add_button.clicked.connect(self.add_expense)  # Συνδέουμε τη μέθοδο εισαγωγής δεδομένων
        self.delete_button = QPushButton("Clear Cost")
        self.delete_button.clicked.connect(self.clear_fields)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Desc"])

        self.table_search = QTableWidget()
        self.table_search.setColumnCount(5)
        self.table_search.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Desc"])

        # Δημιουργία checkboxes για κάθε πεδίο
        self.date_checkbox = QCheckBox()
        self.dropdown_checkbox = QCheckBox()
        self.amount_checkbox = QCheckBox()
        self.description_checkbox = QCheckBox()

        # Δημιουργία πεδίων εισαγωγής
        self.date_box2 = QDateEdit()
        self.date_box2.setDate(QDate.currentDate())

        self.dropdown2 = QComboBox()
        self.dropdown2.addItems(["Food", "Transport", "Utilities", "Entertainment", "Other"])

        self.amount2 = QLineEdit()
        self.description2 = QLineEdit()

        # Αρχικά, τα πεδία είναι απενεργοποιημένα
        self.date_box2.setEnabled(False)
        self.dropdown2.setEnabled(False)
        self.amount2.setEnabled(False)
        self.description2.setEnabled(False)

        # Σύνδεση checkboxes με τα αντίστοιχα πεδία
        self.date_checkbox.stateChanged.connect(lambda state: self.date_box2.setEnabled(state == Qt.Checked))
        self.dropdown_checkbox.stateChanged.connect(lambda state: self.dropdown2.setEnabled(state == Qt.Checked))
        self.amount_checkbox.stateChanged.connect(lambda state: self.amount2.setEnabled(state == Qt.Checked))
        self.description_checkbox.stateChanged.connect(lambda state: self.description2.setEnabled(state == Qt.Checked))

        self.search=QPushButton("search")
        self.search1=QLineEdit()
        self.search.clicked.connect(self.search_item)

        #Design
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()
        self.search_row = QHBoxLayout()  # ΝΕΟ LAYOUT για το Search και το Button
        self.table2=QVBoxLayout()
        self.row4 = QHBoxLayout()

        self.row1.addWidget(QLabel("Date:"))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Category:"))
        self.row1.addWidget(self.dropdown)

        self.row2.addWidget(QLabel("Amount:"))
        self.row2.addWidget(self.amount)

        self.row2.addWidget(QLabel("Desc:"))
        self.row2.addWidget(self.description)

        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.delete_button)

        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)

    # Προσθέτουμε το πρώτο table
        self.master_layout.addWidget(self.table)
        self.master_layout.addSpacing(20)

        self.row4 = QHBoxLayout()

        # Προσθήκη checkboxes + πεδίων στο layout
        self.row4.addWidget(self.date_checkbox)
        self.row4.addWidget(QLabel("Date:"))
        self.row4.addWidget(self.date_box2)

        self.row4.addWidget(self.dropdown_checkbox)
        self.row4.addWidget(QLabel("Category:"))
        self.row4.addWidget(self.dropdown2)

        self.row4.addWidget(self.amount_checkbox)
        self.row4.addWidget(QLabel("Amount:"))
        self.row4.addWidget(self.amount2)

        self.row4.addWidget(self.description_checkbox)
        self.row4.addWidget(QLabel("Desc:"))
        self.row4.addWidget(self.description2)

        self.master_layout.addLayout(self.row4)

        # Προσθήκη του πρώτου πίνακα
        self.master_layout.addWidget(self.table)
        self.master_layout.addSpacing(20)

        # Προσθήκη του search layout

        self.search_row.addWidget(self.search)
        self.master_layout.addLayout(self.search_row)

        # Προσθήκη του δεύτερου πίνακα κάτω από το search
        self.master_layout.addSpacing(20)
        self.master_layout.addWidget(self.table_search)

        # Ορισμός του τελικού layout (ΜΟΝΟ ΜΙΑ ΦΟΡΑ!)
        self.setLayout(self.master_layout)


    def clear_fields(self):
        self.amount.clear()
        self.description.clear()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)

    def add_expense(self):
        path = r"C:\Users\xrist\PycharmProjects\SQL APP\base.ods"

        date = self.date_box.date().toString("yyyy-MM-dd")  # Μετατροπή της ημερομηνίας σε string
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()


        check=0

        df = pd.read_excel(path, engine="odf")
        for row_index, row in df.iterrows():
            if check==0:
                row_index=row_index+2
            else:
                row_index = (row_index + 1)
                print(row_index)


        # Δημιουργία νέας εγγραφής ως DataFrame
        new_data = pd.DataFrame([[row_index,date, category, amount, description]],
                                columns=["id","Ημερομηνία", "Κατηγορία", "Ποσό", "Περιγραφή"])

        if os.path.exists(path):
            try:
                # Διαβάζουμε το υπάρχον αρχείο
                df = pd.read_excel(path, engine="odf")
                # Προσθέτουμε τη νέα γραμμή
                df = pd.concat([df, new_data], ignore_index=True)
            except Exception as e:
                print("Σφάλμα κατά την ανάγνωση του αρχείου:", e)
                return
        else:
            # Αν το αρχείο δεν υπάρχει, δημιουργούμε νέο DataFrame με τα δεδομένα
            df = new_data

        try:
            # Αποθηκεύουμε το αρχείο
            df.to_excel(path, engine="odf", index=False)
            print("Τα δεδομένα αποθηκεύτηκαν επιτυχώς.")
        except Exception as e:
            print("Σφάλμα κατά την αποθήκευση του αρχείου:", e)

        self.load()  # Επαναφόρτωση του πίνακα
        self.clear_fields()  # Καθαρισμός πεδίων εισαγωγής

   # def add_expense(self):
        #date = self.date_box.date().toString("yyyy-MM-dd")  # Μετατροπή της ημερομηνίας σε string
        #category = self.dropdown.currentText()
        #amount = self.amount.text()
        #description = self.description.text()

        #self.load()
        # Προσθέτουμε μια νέα γραμμή στον πίνακα
        #self.table.insertRow(self.row_count)
        #self.table.setItem(self.row_count, 0, QTableWidgetItem(str(self.row_count + 1)))  # ID
        #self.table.setItem(self.row_count, 1, QTableWidgetItem(date))
        #self.table.setItem(self.row_count, 2, QTableWidgetItem(category))
        #self.table.setItem(self.row_count, 3, QTableWidgetItem(amount))
        #self.table.setItem(self.row_count, 4, QTableWidgetItem(description))

        #self.row_count += 1  # Αύξηση του μετρητή ID
        #self.clear_fields()  # Καθαρίζουμε τα πεδία εισαγωγής

    def load(self):
        path = r"C:\Users\xrist\PycharmProjects\SQL APP\base.ods"

        if not os.path.exists(path):
            print(f"Το αρχείο δεν βρέθηκε: {path}")
            return

        try:
            # Διαβάζουμε το αρχείο ODS
            df = pd.read_excel(path, engine="odf")

            self.table.setRowCount(0)  # Καθαρίζει τον πίνακα
            self.table.setColumnCount(len(df.columns))  # Ρύθμιση στηλών

            # Γεμίζουμε τον πίνακα με τα δεδομένα από το ODS
            for row_index, row in df.iterrows():
                self.table.insertRow(row_index)
                for col_index, value in enumerate(row):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        except Exception as e:
            print("Σφάλμα κατά τη φόρτωση του αρχείου:", e)

    def search_item(self):
        path = r"C:\Users\xrist\PycharmProjects\SQL APP\base.ods"

        # Παίρνουμε τα δεδομένα από τα πεδία
        date = self.date_box2.date().toString("yyyy-MM-dd")  # Ημερομηνία σε string
        category = self.dropdown2.currentText()
        amount = self.amount2.text()
        description = self.description2.text()

        # Διαβάζουμε το αρχείο ODS
        df = pd.read_excel(path, engine="odf")

        # Φιλτράρισμα των δεδομένων
        filters = []
        if self.date_checkbox.isChecked() and date:
            filters.append(df["Ημερομηνία"] == date)
        if self.dropdown_checkbox.isChecked() and category:
            filters.append(df["Κατηγορία"] == category)
        if self.amount_checkbox.isChecked() and amount:
            filters.append(df["Ποσό"] == amount)
        if self.description_checkbox.isChecked() and description:
            filters.append(df["Περιγραφή"].str.contains(description, case=False, na=False))

        # Εφαρμόζουμε τα φίλτρα αν υπάρχουν
        if filters:
            filtered_df = df.loc[pd.concat(filters, axis=1).all(axis=1)]
        else:
            filtered_df = df  # Αν δεν έχει επιλεγεί φίλτρο, εμφανίζουμε όλα τα δεδομένα

        # Εκτυπώνουμε το αποτέλεσμα στο terminal
        print(filtered_df)

        # Εμφάνιση των αποτελεσμάτων στον δεύτερο πίνακα
        self.table_search.setRowCount(0)  # Καθαρισμός πίνακα πριν προσθήκη νέων δεδομένων
        for row_index, row_data in filtered_df.iterrows():
            row_position = self.table_search.rowCount()
            self.table_search.insertRow(row_position)
            for col_index, value in enumerate(row_data):
                self.table_search.setItem(row_position, col_index, QTableWidgetItem(str(value)))







if __name__ == "__main__":
    app = QApplication([])
    main = ExpenseAPP()
    main.show()
    app.exec_()
