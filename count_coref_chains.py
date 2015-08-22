# The purpose of this script is to count annotations in the xml knowtator files. 

# Assumptions:

# 1) Input files are xml.
# 2) Input file names end with .xml extension.

# Author: Natalya Panteleyeva natalya.panteleyeva@gmail.com

# Imports, carefully arranged in alphabetical order
import nltk
#import nltk.probability.FreqDist
from nltk import probability
from nltk import wordpunct_tokenize
import re
#import nltk.text.Text
#import text
from nltk import text

import argparse, os, shutil
from string import Formatter

# Set this to True for helpful debugging output and to False to
# suppress same.
#DEBUG = True
DEBUG = False

# Set this to True to just work on a single file, or to False
# to read in the contents of a directory.
#DEVEL = True
DEVEL = False

if __name__ == "__main__":
    import argparse, sys, os, re
    from argparse import ArgumentParser


parser = argparse.ArgumentParser(description='Comparing coreference chains.')
parser.add_argument("-k", "--knowtator",
        dest="knowtator", required=True,
        help="input knowtator xml directory", metavar="DIRECTORY")
args = parser.parse_args()

datapath = os.getcwd() + '/' +  args.knowtator
files = os.listdir(datapath)

# Remove files not part of the collection
p = re.compile('\D')
for f in files:
     if p.match(f):
	files.remove(f)

##print 'FileID' + '\t\t' + 'IDs' + '\t' + 'Appos' + '\t' + 'Annotations' + '\t' + 'MeanID' + '\t' + 'MedianID' + '\t' + 'Range'

#Global collection counts
ids = 0
appos = 0
annot = 0
global_chain_length_index = [0 for i in xrange(300)]
max_len=0
fid_maxlen=''
id_maxlen=''
total_chain_length = 0

for f in files: 
# For the contents of the directory...  
     fid = re.findall('[0-9]+', f)
     fl = datapath + '/' + f

     # Read in the file
     knowtator = open(fl,'r')
     kn = knowtator.read()
     knowtator.close()

     identity_chain_count = kn.count('>IDENTITY chain<')
     appos_chain_count = kn.count('>APPOS relation<')
     annotation_count = kn.count('<annotation')
     	
     mc = kn
     idcopy = kn
     ididx = idcopy.find('>IDENTITY chain<')
     chain_length_index = [0 for i in xrange(300)]
     
     while ididx != -1:
	#Find the end of the IDENITTY chain record
	end_ididx = idcopy[ididx:].find('</classMention>')
	#Extract the identifier for this IDENTITY chain
	idref = idcopy[ididx:ididx+end_ididx].find('hasSlotMention id="')
	if idref == -1:
		ref = ''
	else:
		idref = idref + len('hasSlotMention id="')
		idref_end = idcopy[ididx+idref:ididx+end_ididx].find('\" />')
		ref = idcopy[ididx+idref:ididx+idref+idref_end]
	if ref == '':
		idref_end = -1
	#Find the record for this identifier
	else:
		seek = 'complexSlotMention id="' + ref + '"'
		i = mc.find(seek)
		#Extract the chain 
		i1 = mc[i:].find('<mentionSlot id="Coreferring strings" />')
		l1 = len('<mentionSlot id="Coreferring strings" />')
		i2 = mc[i:].find('</complexSlotMention>')
		chain = mc[i+i1+l1:i+i2]
		chain_length = chain.count('<complexSlotMentionValue')
		if chain_length > max_len:
			max_len=chain_length
			fid_maxlen=f
			id_maxlen=ref 
 		chain_length_index[chain_length] = chain_length_index[chain_length]+1
		global_chain_length_index[chain_length] = global_chain_length_index[chain_length]+1
		total_chain_length = total_chain_length+chain_length
	idcopy = idcopy[ididx+end_ididx+len('</classMention>'):] 
	ididx = idcopy.find('>IDENTITY chain<')

     lengths = list()
     for j in xrange(max_len):
	if chain_length_index[j] > 0:
		lengths.append(j)
     if len(lengths) > 0:
		ave = (float)(sum(lengths))/len(lengths)
     if len(lengths) % 2 == 0:
	med = (float)(lengths[len(lengths)/2-1] + lengths [len(lengths)/2])/2
     else:
	med = lengths[(len(lengths)-1)/2]	
     range = lengths[len(lengths)-1]-lengths[0]
     ids = ids + identity_chain_count
     appos = appos + appos_chain_count
     annot = annot + annotation_count
				
print 'Totals:\t\t' + str(ids) + '\t'+ str(appos) + '\t  ' + str(annot)
print str(fid_maxlen) + '\t' + str(id_maxlen) + '\t' + str(max_len)
