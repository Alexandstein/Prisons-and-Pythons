import re

class Modifier(object):
	'''Modifiers to the character's stats.
	Members:
		name (string)
			Name if applicable
		description (string)
			Description of the modifier
		stats (dictionary of string:string)
			Stat changes
	'''
	def __init__(self, name = '', description = '', statList = []):
		self.name = name
		self.description = description
		self.stats = {}
		for stat in statList:
			self.stats.update({stat: 0})
	
	def __str__(self):
		output = '%s|%s|' % (self.name, self.description)
		for stat in self.stats:
			output += '%s:%s|' % (stat, self.stats[stat])
		return output.strip('|')
	__repr__ = __str__

class AbstractCharacter(object):
	'''Character class used to hold data about a character's stats. Does calculations as well.
	Members:
		charData (dictionary of lists or dicts)
			Carries lists of data about the character:
			
			attributes
				Carries string characteristics of the character.
			stats (dictionary of string:ints)
				Carries base stat-value pairs.
			modifiers (list of Modifiers)
				Equipment which modifies stats.
	'''
	def __str__(self):
		'''Tostring function
		'''
		output = ''
		
		for section in self.charData:
			output += section + '\n'
			#Use try/catch to detect whether dictionary or list attributes
			try:
				for name in self.charData[section].keys():
					output += '\t%s|%s\n' % (name, self.charData[section][name])
			except AttributeError:
				for item in self.charData[section]:
					output += '\t%s\n' % str(item)
#		output += 'Attribute\n'
#		for attr in self.charData['attributes']:
#			output += '\t%s|%s\n' % (attr, self.charData['attributes'][attr])
#		output += 'Stat\n'
#		for stat in self.charData['stats']:
#			output += '\t%s|%s\n' % (stat, self.charData['stats'][stat])
#		output += 'Modifier\n'
#		for mod in self.charData['modifiers']:
#			output += '\t%s\n' % mod
		return output.strip()
	__repr__ = __str__
	
	def __init__(self, name):
		'''Constructor creates an empty character
		Args:
			name (string)
				Name to initialize the character with.
		'''
		self.charData = {}
		self.charData['attributes'] = {'name':name}
		self.charData['stats'] = {}
		self.charData['modifiers'] = []
	
	def addToStats(self, stat, init = 0, fromSerialized = False):
		''' Adds a stat to the character
		Args:
			stat (string)
				Name or serialized string of the stat to be added.
			init (Number) (optional)
				Initial value for stat. 0 if not set.
			fromSerialized (bool)
				Parses a serialized string.
		Return:
			(void)
		'''
		if not (stat or fromSerialized):
			#No input given. Think of better way to handle this?
			raise ValueError
		#Detect serialized string to parse
		if fromSerialized:
			stat = stat.split('|')
			stat, init = stat[0], int(stat[1])
		self.charData['stats'].update({stat:init})

	def addToAttributes(self, attr, init = '', fromSerialized = False):
		''' Adds a attribute to the character
		Args:
			attr (string)
				Name of the attribute or serialized string to be added.
			init (string) (optional)
				Initial value. None if not set.
			fromSerialized (bool)
				Parses a serialized string.		
		Return:
			(void)
		'''
		
		if fromSerialized:
			attr = attr.split('|')
			attr, init = attr[0], attr[1]
		self.charData['attributes'].update({attr:init})
	
	def addToModifiers(self, mod, fromSerialized = False):
		''' Adds a attribute to the character
		Args:
			mod (Modifier) (string)
				Name or serialized string of the modifier to be added.
			fromSerialized (bool)
				Parses a serialized string.		
		Return:
			(void)
		'''
		if fromSerialized:
			return
			#TODO
			modData = fromSerialized.split('|')
			mod = Modifier()
			#TODO
		self.charData['modifiers'].append(mod)
	
	def dropModifier(self, mod):
		''' Drops a attribute from the character
		Args:
			mod (string)
				Name of the stat to be dropped.
		Return:
			(void)
		'''
		raise NotImplementedError
		self.charData['modifiers'].append(mod)

	def getAttribute(self, attr):
		'''Fetches an attribute of the character and returns it.
		Args:
			attr (string)
				Name of attribute to fetch.
		Return:
			(string) Value of the attribute being fetched.
		Throws:
			KeyError
				On attempting to access nonexistent attribute.
		
		'''
		return self.charData['attributes'][attr]
	
	def getStat(self, stat):
		'''Fetches a stat of the character and returns it.
		Args:
			stat (string)
				Name of attribute to fetch.
		Return:
			(Number) Value of the stat being fetched.
		Throws:
			KeyError
				On attempting to access nonexistent stat.
		
		'''	
		return self.charData['stats'][stat]
	
	def getModifier(self, modifier):
		'''Fetches a modifier of the character and returns it. If there are multiple mods
		with the same name, then the first one encountered is removed.
		Args:
			modifier (string)
				Name of attribute to fetch.
		Return:
			(Modifier) Value of the stat being fetched.
		Throws:
			KeyError
				On attempting to access nonexistent Modifier.
		'''	
		raise NotImplementedError
			
	def save(self, filename=None, printout=False):
		'''Write out the character to a file
		Args:
			filename (string)
				Name of the .char file to be created. Defaults to the name given to the
				character if no argument is given.
			printout (boolean)
				Optional arg prints out file output when set to True.			
		'''
		output = self.__str__()
		if not filename:
			filename = self.charData['attributes']['name']
		outFile = open(filename + ".char", 'w+')
		outFile.write(output)
		outFile.close()
		
		if printout:
			print output

def save(character):
	'''Saves inputed character as a .char file.
	Args:
		character (AbstractCharacter)
			Character to be saved as a file.
	'''
	character.save()

def load(charFile):
	'''Load a character from *.char file.
	Args:
		charFile (string)
			Path to a *.char file to read from.
	Return:
		Returns an AbstractCharacter object.
	Throws:
		IOError
			If file is not found.
	'''
	file = open(charFile, 'r')
	#Dummy name. If problem happens but character is still returned it will 
	#be named 'Error'. Handle this better in the future. TODO
	char = AbstractCharacter('Error')
	
	#Variable to hold active function for loading character attributes and stats.
	setterFunction = None
	for line in file:
		line = line.strip('\n')
		#Tabbed lines are individual elements under a category of attributes
		if re.match('^\\t', line):
			setterFunction(line.strip(), fromSerialized = True)
		else:
			setterFunction = getattr(char, 'addTo' + line.strip().capitalize())
	return char