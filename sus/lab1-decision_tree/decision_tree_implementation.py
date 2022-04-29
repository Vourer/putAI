import numpy as np


class Node(object):
	def __init__(self):
		self.left = None  # Typ: Node, wierzchołek znajdujący się po lewej stornie
		self.right = None  # Typ: Node, wierzchołek znajdujący się po prawej stornie
		self.split_attr = None  # atrybut do dokonania podziału
		self.split_value = None  # wartość graniczna do podziału
		self.prediction = None  # wynik (tylko w liściu)
		self.improvement_rate = 0.05  # procent, o który musi poprawić się błąd po podziale

	def find_best_split(self, data):
		current_var = (1-self.improvement_rate) * self.calc_var(data)
		best_var = current_var
		best_attr = None
		best_value = None

		for xi in range(nAttr):  # dla każdego artybutu
			# stwórz listę unikalnych wartości dla atrybutu xi
			values = np.unique(data[:, xi])
			for value in values:
				# podziel 'data' na dwa podzbiory względem unikalnej wartości atrybutu 'xi'
				d1 = data[data[:, xi] <= value]
				d2 = data[data[:, xi] > value]
				# sprawdź czy podzbiory nie są puste - jeśli nie są, oblicz zmianę wariancji
				if (len(d1) > 0) and (len(d2) > 0):
					var_change = len(d1)/len(data)*self.calc_var(d1) + len(d2)/len(data)*self.calc_var(d2)
					if var_change < best_var:
						best_var = var_change
						best_attr = xi
						best_value = value

		return best_attr, best_value

	def perform_split(self, data, level):
		attr, value = self.find_best_split(data)

		# if uzyskano poprawę funkcji celu (bądź inny, zaproponowany przez Ciebie warunek):
		if attr is not None and level < 5:
			# podziel dane na dwie części d1 i d2, zgodnie z warunkiem
			d1 = data[data[:, attr] <= value]
			d2 = data[data[:, attr] > value]
			# zapisz sposób podziału
			self.split_attr = attr
			self.split_value = value
			# rozbuduj drzewo
			self.left = Node()
			self.right = Node()
			self.left.perform_split(d1, level+1)
			self.right.perform_split(d2, level+1)
		else:
			# obecny Node jest liściem, zapisz jego odpowiedź
			self.prediction = np.mean(data[:, nAttr])

	def predict(self, example):
		# if zdefiniowano sposób podziału
		if self.split_attr is not None:
			if example[self.split_attr] > self.split_value:
				return self.right.predict(example)
			else:
				return self.left.predict(example)
		# Node jest liściem
		return self.prediction

	@staticmethod
	def calc_var(data):
		y = data[:, nAttr]
		variance = np.var(y)
		return variance

	@staticmethod
	def calc_rmse(data):
		y = data[:, nAttr]
		pred = np.mean(y)
		rmse = 0
		for actual in y:
			rmse += pow((pred - actual), 2)
		rmse = rmse / len(y)
		return pow(rmse, 0.5)


# Najprostsze wczytywanie i zapisywanie danych, a także wywołanie obiektu Node
# Szczególnie przydatne dla osób nie znających numpy
# Zbiór danych jest reprezentowany jako "lista list".
# tj. data[0] zwróci listę z wartościami cech pierwszego przykładu

for file_id in range(1, 14):
	id = f"./data/{file_id}"  # podaj id zbioru danych który chcesz przetworzyć np. 1
	data = []
	y = [line.strip() for line in open(id + '-Y.csv')]
	for i, line in enumerate(open(id + '-X.csv')):
		if i == 0:
			continue
		x = [float(j) for j in line.strip().split(',')]
		nAttr = len(x)
		x.append(float(y[i]))
		data.append(x)

	data = np.array(data, dtype=np.float64)
	print(f'Data {file_id} load complete!')
	tree = Node()
	tree.perform_split(data, 0)
	print(f'Training {file_id} complete!')

	with open(id+'.csv', 'w') as f:
		for i, line in enumerate(open(id + '-test.csv')):
			if i == 0:
				continue
			x = [float(j) for j in line.strip().split(',')]
			y = tree.predict(x)
			f.write(str(y))
			f.write('\n')
