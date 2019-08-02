# coding:UTF-8
import configparser

# configparser.ConfigParser
#class MyConfigParser(configparser.ConfigParser): 
#	def init(self, defaults=None): 
#		configparser.ConfigParser.init(self, defaults=defaults)
#	def optionxform(self, optionstr):
#		return optionstr

class MyConfigParser(configparser.ConfigParser):
	def __init__(self, defaults=None):
		configparser.ConfigParser.__init__(self, defaults=defaults)
	def optionxform(self, optionstr):
		return optionstr