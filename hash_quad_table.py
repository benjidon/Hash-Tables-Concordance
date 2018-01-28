import string
from string import maketrans

class HashTableQuadPr:
	"Creates the HashTableLinPr class and initializes values"

	def __init__(self,size):
		self.hash_table = [None] * size
		self.capacity = size
		self.num_items = 0
		self.num = 0

	def read_stop(self,filename):
		"Reads a stop words file and adds the words to a hash table"

		f = open(filename,'r')

		for line in f:
			if self.get_load_fact() >= 0.5:
				newcap = (self.capacity * 2) + 1
				old_hash = self.hash_table
				self.hash_table = [None] * newcap
				self.capacity = newcap
				self.num_items = 0

				for item in old_hash:
					if item != None:
						self.hash(item)
			else:
				self.hash(line[:-2])
		f.close()


	def read_file(self,filename,stop_table):
		"Reads a read word file and hashes the words along with their line numbers, excluding some characters"

		linenum = 1
		lst = open(filename).read().splitlines()
		lst2 = []
		lst3 = []

		for word in lst:
			low = word.lower()
			new = low.replace("'","")
			trans = maketrans(string.punctuation, " "*len(string.punctuation))
			new2 = new.translate(trans)
			lst2.append(new2)

		for i in range(len(lst2)):
			word = lst2[i]
			wordlist = word.split(" ")
			for word in wordlist:
				if word not in string.whitespace:
					wordtup = (word,[linenum])
					lst3.append(wordtup)
			linenum += 1

		for tup in lst3:
			if not self.is_number(tup[0]) and not tup[0] in stop_table.hash_table:
				if self.get_load_fact() >= 0.5:
					newcap = (self.capacity * 2) + 1
					old_hash = self.hash_table
					self.hash_table = [None] * newcap
					self.capacity = newcap
					self.num_items = 0

					for item in old_hash:
						if item != None:
							self.hash(item)
				else:
					self.read_hash(tup)


	def is_number(self,str):
		"Tests if a string contains a number"
		try:
			float(str)
			return True
		except ValueError:
			return False


	def hash(self,word):
		"Helper function to hash values for the read_stop function"

		index = self.myhash(word,self.capacity)


		if self.hash_table[index] == None:
			self.hash_table[index] = word
		else:
			k = 1
			i = 3
			while self.hash_table[index] != None:
				index = (index + k) % self.capacity
				k = k + i
				i = i + 2
			self.hash_table[index] = word
		self.num_items += 1

	def read_hash(self,tup):
		"Helper function to hash values for the read_file"

		index = self.myhash(tup[0],self.capacity)


		if self.hash_table[index] == None:
			self.hash_table[index] = tup
		elif self.hash_table[index][0] == tup[0]:
			if tup[1][0] not in self.hash_table[index][1]:
				self.hash_table[index][1].append(tup[1][0])
			else:
				return False
		else:
			k = 1
			i = 3
			while self.hash_table[index] != None:
				index = (index + k) % self.capacity
				k = k + i
				i = i + 2
			self.hash_table[index] = tup
		self.num_items += 1

	def save_concordance(self,outputfilename):
		"Ouputs the contents of the hash table to a text file following specified format"

		lst = []

		for tup in self.hash_table:
			if tup != None:
				lst.append(tup)

		sort_lst = sorted(lst,key = lambda tup: tup[0])
		
		f = open(outputfilename,'w')

		for item in sort_lst:
			f.write(item[0])
			f.write(":\t")
			for i in range(len(item[1])):
				if i < len(item[1]) - 1:
					f.write(str(item[1][i]))
					f.write(",")
				else:
					f.write(str(item[1][i]))
			f.write('\n')


	def myhash(self,key,table_size):
		"Function to determine the hash location of a string"
		n = None
		hashval = 0
		if len(key) <= 8:
			n = len(key)
		else:
			n = 8

		for i in range(n):
			hashval += (ord(key[i]) * (31**(n - 1 - i)))

		return hashval % table_size


	def get_load_fact(self):
		"Returns the load factor of the table"
		return float(self.num_items) / self.capacity

	def get_tablesize(self):
		"Returns the size of the table"
		return self.capacity


# test = HashTableQuadPr(251)
# test.read_stop('stop_words.txt')
# #print(test.hash_table)
# #print(test.capacity)
# test2 = HashTableQuadPr(251)
# test2.read_file('input2.txt',test.hash_table)
# #print test2.hash_table
# #print test2.capacity
# #print test.is_number('ss')
# test2.save_concordance('tester.txt')











