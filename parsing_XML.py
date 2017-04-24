import xml.etree.ElementTree as ET
import re
tree = ET.parse('Sample1.xml')
root = tree.getroot()

# Initial examination with XML file (topmost layer)

'''
print root # PubmedArticleSet
print root[0] #PubmedArticle

#print root[1] # gives you index error - remember, this is just like a list

print type(root) # this is xml.etree.ElementTree.Element
print type(root.tag) # this is a string

# Let's take a look at the contents

print root[0][0] # MedlineCitation
print root[0][0][0] #PMID
print root[0][0][1] #DateCreated
print root[0][0][4][3][0].text # shows the abstract texts

# Iteration

for node in tree.iter():
	print node.tag, node.attrib # Prints all the nodes tags and attributes
	# Note that attrib is actually empty... {}

# Using iteration, you can now get all the texts.

for node in tree.iter():
	if node.tag == 'AbstractText':
		print node.text
'''
# Save it to the memory

abstractTexts = []

abstractPMID = []

for node in tree.iter():
	if node.tag == 'AbstractText':
		abstractTexts.append(node.text)
	if node.tag == 'PMID':
		abstractPMID.append(node.text)

#print abstractTexts
#print abstractPMID

abstractText_and_PMIDs = zip(abstractPMID,abstractTexts)

PMIDs, abstractText = zip(*abstractText_and_PMIDs)

#print abstractText_and_PMIDs

splitaT = []

for j in abstractText:
	#splitaT.append(j.split(" "))
	#splitaT.append(re.sub(r'[^a-zA-Z ]', '', j).split())
	splitaT.append(re.sub(r'[().,]', '', j).split())
	
#print splitaT[1]
#print len(splitaT)

from collections import Counter

#termlist = [] 
#freqlist = []

termandfreq = []
termandfreqtemp = []

for k, l in enumerate(splitaT):
	uniques = sorted(set(splitaT[k])) #sorts alphabetically + removes repeats
	for term in uniques:
		#print splitaT[k].count(term), term
		#freqlist[k].append(splitaT[k].count(term))
		#termlist[k].append(term)
		val = (term, splitaT[k].count(term))
		termandfreqtemp.append(val)
	#termlist.append(Counter(splitaT[k]).most_common(10))
	termandfreq.append(sorted(termandfreqtemp, key=lambda x: x[1], reverse=True))
	termandfreqtemp = []

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
 
#tenterm = []
#tenfreq = []

for m, n in enumerate(termandfreq):
	tenterm, tenfreq = zip(*termandfreq[m])
	tenterm = tenterm[:9]
	tenfreq = tenfreq[:9]
	y_pos = np.arange(len(tenterm))

	plt.bar(y_pos, tenfreq, align='center', alpha=0.7)
	plt.xticks(y_pos, tenterm, rotation = 'vertical')
	plt.subplots_adjust(bottom=.28)
	plt.xlabel('Most Frequent Terms')
	plt.ylabel('Frequency')
	plt.title('PMID: '+ PMIDs[m]+' Abstract Term Frequencies')
	plt.show()

# Now, save this in SQLite3 file so you can visualize it.

import sqlite3
conn = sqlite3.connect('Pub_Exercise.db') # Create a connection to the database

cur = conn.cursor() # Get a cursor on the database. Allows using SQL

cur.execute('DROP TABLE IF EXISTS Pub_Table')
cur.execute('CREATE TABLE Pub_Table (ID INTEGER PRIMARY KEY AUTOINCREMENT,PMID INTEGER,Abstract TEXT)')
cur.executemany('INSERT INTO Pub_Table (PMID,Abstract) VALUES(?,?)', abstractText_and_PMIDs) # Putting in data using SQL query

conn.commit() # Commit changes to the database

cur.close() # Close the cursor

conn.close() # Close the database connection
