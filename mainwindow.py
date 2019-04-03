from PySide2.QtCore import * 
from PySide2.QtWidgets import * 
from PySide2.QtGui import * 
import csv

class CentralWidget(QWidget):
	def __init__(self):
		super().__init__()

		self.label = QLabel()
		self.view = QTreeWidget()
		self.label.setAlignment(Qt.AlignCenter|Qt.AlignVCenter)
		font = QFont()
		font.setBold(True)
		self.label.setFont(font)


		layout = QVBoxLayout()
		layout.addWidget(self.label)
		layout.addWidget(self.view)
		self.setLayout(layout)

	def set_filename(self, filename):
		self.filename = filename
		header = None
		self.view.clear()
		genotype = []
		with open(self.filename, 'r') as file:
			reader = csv.reader(file, delimiter='\t', quotechar='|')
			for row in reader:
				if not row[0].startswith("#"):
					if header is None:
						header = row
						self.view.setColumnCount(len(header))
						continue
					else:
						genotype.append(row[5])

						item = QTreeWidgetItem()
						for index, element in enumerate(row):
							item.setText(index, element)
						self.view.addTopLevelItem(item)
		self.set_genotype(genotype)

	def set_genotype(self, genotype):

		mapping = {
			"AA" : "A",
			"CC" : "C",
			"TT" : "T",
			"GG" : "G",
			"AG" : "R",
			"CT" : "Y",
			"CG" : "S",
			"AT" : "W",
			"GT" : "K",
			"AC" : "M"
		}

		final_genotype = str()
		for gt in genotype:
			gt = "".join(sorted(list(gt)))
			final_genotype += mapping.get(gt,"?")

		self.label.setText(final_genotype)




class MainWindow(QMainWindow):
	def __init__(self, parent = None):
		super().__init__(parent)

		self.fileview = QListView()
		self.view = CentralWidget()
		self.filemodel = QFileSystemModel()
		self.fileview.setModel(self.filemodel)
		dock = QDockWidget()
		dock.setWidget(self.fileview)
		self.addDockWidget(Qt.LeftDockWidgetArea, dock)

		self.setCentralWidget(self.view)

		self.toolbar = QToolBar()
		self.addToolBar(self.toolbar)

		self.toolbar.addAction("open folder").triggered.connect(self.open_folder)


		self.fileview.clicked.connect(self.file_clicked)

	def file_clicked(self):
		filename = self.filemodel.filePath(self.fileview.currentIndex())
		self.view.set_filename(filename)


	def open_folder(self):

		path = QFileDialog.getExistingDirectory(self)

		self.fileview.setRootIndex(self.filemodel.setRootPath(path))
		self.filemodel.setFilter(QDir.Files)
		self.filemodel.setNameFilters(["*.txt"])


