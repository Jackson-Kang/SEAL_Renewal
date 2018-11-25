from django import template
from datetime import date, timedelta
from index.models import *
register = template.Library()

@register.filter(name='lookup')
def lookup(d, key):
    return d[key]

register.filter(lookup)

def getTotalCount(d,key):

	return Total_Evaluation.objects.get(id=key).Total_Count
register.filter(getTotalCount)

def calculateData(val,arg):

	if arg==1000:
		if val-1000>=0:
			return 1
	elif arg==100:
		if val%1000 -100 >=0:
			return 1

	elif arg==10:
		if val%100 -10 >=0:
			return 1
	elif arg==1:
		if val%10 -1 >=0:
			return 1
	return 0
register.filter(calculateData)
@register.filter(name='calculateTotal')
def calculateTotal(val,arg):
	try:
		return val/arg
	except:
		return 0
register.filter(calculateTotal)

@register.filter(name='mCalculateTotal')
def mCalculateTotal(val,arg):
	try:
		return "{0:.1f}".format(val/arg)
	except:
		return 0
@register.filter
def filename(value):
	return os.path.basename(value.file.name)

def Mod(val,arg):
	return val%arg
register.filter(Mod)
def Add(val,arg):
	return int(val)+int(arg)
register.filter(Add)

def ChangeName(val):
	return val.split("외")[0] != None and val.split("외")[0]  or val
register.filter(ChangeName)