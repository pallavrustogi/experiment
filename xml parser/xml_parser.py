#!/usr/bin/python2.7
__author__ = 'rustogi@usc.edu'
import xml.sax
import sys
import getopt


maxRent = 0
minRent = sys.maxint
oneBedCount = 0
totalOneBedSqFeet = 0
maxPricePerSqFeet = 0
aptCountSF = 0
apt2bhkNY = 0
totalCArent = 0
oneBedCACount = 0
bonCount = 0

 
class ABContentHandler(xml.sax.ContentHandler):
	def __init__(self):
		'''Initallize buffer'''
		xml.sax.ContentHandler.__init__(self)
		self.__buffer = ''
		self.street = ''
		self.state = ''
		self.city = ''
		self.zip = ''
		self.beds = ''
		self.bathrooms = ''
		self.sqFoot = ''
		self.rent = ''
 
	def startElement(self, name, attrs):
		'''Clearing temp buffer for next tag'''
		self.__buffer=''

	def endElement(self, name):
		
		'''Read data of current Apartment into buffer for processing'''
		if name == "Street":
			self.street=self.__buffer
		if name == "City":
			self.city=self.__buffer
		if name == "State":
			self.state=self.__buffer
		if name == "Zip":
			self.zip=self.__buffer
		if name == "Beds":
			self.beds=int(self.__buffer)
		if name == "Bathrooms":
			self.bathrooms=int(self.__buffer)
		if name == "SquareFoot":
			self.sqFoot=int(self.__buffer)
		if name == "Rent":
			self.rent=int(self.__buffer)

		'''Enter Custom Code for various Conditions here'''
		if name =="Apartment":
			'''Heightest Monthly Rent'''
			global maxRent
			maxRent=max(maxRent,self.rent)
			'''Lowest Monthly Rent'''
			global minRent
			minRent=min(minRent,self.rent)
			'''Total 1BR Sq Footage in CA'''
			if self.state=="CA" and self.beds == 1:
				global totalOneBedSqFeet
				totalOneBedSqFeet+=self.sqFoot
				global oneBedCount
				oneBedCount+=1
			'''Heightest price per sqFoot'''
			global maxPricePerSqFeet
			maxPricePerSqFeet=max(float(maxPricePerSqFeet),self.sqFoot/float(self.rent))
			'''Number of Apartment in SF, CA'''
			if self.state=="CA" and self.city=="San Francisco":
				global aptCountSF
				aptCountSF+=1
			'''Number of Apartments with two bathrooms in NYC'''
			if self.state=="NY" and self.city=="New York" and self.beds==2:
				global apt2bhkNY
				apt2bhkNY+=1
			'''Average rent of 1BR in SF and LA'''
			if self.state == "CA" and (self.city=="Los Angeles" or self.city=="San Francisco") and self.beds==1:
				global totalCArent
				totalCArent+=self.rent
				global oneBedCACount
				oneBedCACount+=1
			'''Bonus: Number of BR with bathrooms < beds in CA'''
			if self.state == "CA" and self.bathrooms < self.beds:
				global bonCount
				bonCount+=1

				
		'''End of Apartment, Clear all data'''
		if name=="Apartment":
			self.__buffer = ''
			self.street = ''
			self.state = ''
			self.city = ''
			self.zip = ''
			self.beds = ''
			self.bathrooms = ''
			self.sqFoot = ''
			self.rent = ''
	def characters(self, content):
		self.__buffer +=content

def Usage():
  print 'Usage: %s xmlFileName' % __file__
  print
  print '  This script parses the given xml file and calculates'
  print '  statistics'
  print
  print '  Options:'
  print '    --help -h : print this help'
  print '    --output : statistics'
 
def main():
	try:
		opts, args = getopt.gnu_getopt(sys.argv[1:], 'ho', ['help', 'output='])
	except getopt.GetoptError:
		Usage()
		sys.exit(2)
	try:
		searchStr = args[0]
	except:
		Usage()
		sys.exit(2)
	for o, a in opts:
		if o in ("-h", "--help"):
			Usage()
			sys.exit(2)
		if o in ("-o", "--output"):
			output = a
	source = open(searchStr)
	xml.sax.parse(source, ABContentHandler())
	
	global maxRent
	print "Highest monthly rent: $%s"%maxRent
	global minRent
	print "Lowest monthly rent: $%s"%minRent
	global oneBedCount
	global totalOneBedSqFeet
	if oneBedCount!=0:
		print "Average 1 bedroom square footage in CA:",totalOneBedSqFeet/float(oneBedCount)
	else:
		print "Average 1 bedroom square footage in CA: 0"
	global maxPricePerSqFeet
	print "Highest price per square foot: $%s"%maxPricePerSqFeet
	global aptCountSF
	print "Number of apartments in San Francisco, CA: %s"%aptCountSF
	global apt2bhkNY
	print "Number of apartments with 2 bathrooms in New York, NY: %s"%apt2bhkNY
	global oneBedCACount
	global totalCArent
	if oneBedCACount !=0:
		print "Average rent of 1 bedroom apartments in San Francisco, CA and Los Angeles, CA:",totalCArent/float(oneBedCACount)
	else:
		print "Average rent of 1 bedroom apartments in San Francisco, CA and Los Angeles, CA: 0"
	global bonCount
	print "Number of apartments with number of bathrooms less than beds in CA: %s"%bonCount

if __name__ == "__main__":
	main()