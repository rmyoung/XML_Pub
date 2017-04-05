import xml.etree.ElementTree as ET
tree = ET.parse('Sample1.xml')
root = tree.getroot()

# Initial examination with XML file (topmost layer)

print root # PubmedArticleSet
print root[0] #PubmedArticle

#print root[1] # gives you index error - remember, this is just like a list

print type(root) # this is xml.etree.ElementTree.Element
print type(root.tag) # this is a string

# Let's take a look at the contents

print root[0][0] # MedlineCitation
print root[0][0][0] #PMID
print root[0][0][1] #DateCreated

