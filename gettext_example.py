import gettext
try:
	lan = gettext.translation('nvda', localedir='locale', languages=['zh_TW'])
	lan.install()
except:
	_ = lambda s:s

print(_("Access8Math interaction window"))