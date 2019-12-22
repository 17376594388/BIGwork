# -*- coding: utf-8-*-
import exceptions
def checkemail(email1,email2):
	if email1!=email2:
		raise Exception("301")
def checknumber(checknum1,checknum2):
	if checknum1!=checknum2:
		raise Exception("302")
def checkpwd(pwd,pwdagain):
	if pwd!=pwdagain:
		raise Exception("303")
def checknull(pwd):
	if not pwd:
		raise Exception("308")
