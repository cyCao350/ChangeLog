# -*- coding: utf-8 -*-
import os

# hsWriteLog(DEBUG_LEVEL,sSql);
# hsWriteLog(0,tmp);
# hsWriteLog(0,szTmpInstanceIds);
# hsWriteLog(0,sSql);
# hsWriteLog(2,sUndoFund);
#hsWriteLog(0,sErrMsg);

#遍历文件目录
def dirfile(path,allfile):
	filelist=os.listdir(path)
	for filename in filelist:
		filepath=os.path.join(path,filename)
		if os.path.isdir(filepath):
			dirfile(filepath,allfile)
		else:
			allfile.append(filepath)
			#处理 filepath 的数据
			doData(filepath)
	return allfile

def doData(filepath):
	#正则表达式
	import re
	info={}
	sMatch=re.compile('hsWriteLog\([\s\S]*?\);')#处理了换行的问题
	#从文件中读取数据来匹配
	print(filepath)
	fopen=open(filepath,'r+',encoding='iso-8859-15')#  r+ 以读写模式打开  添加 encoding='iso-8859-15'
	#fopen=open(filepath,'r+')#  r+ 以读写模式打开
	fopen.seek(0)
	#print(fopen.readlines())
	cont=fopen.read()
	#print(cont)
	ret=sMatch.findall(cont)
	#print(ret)
	for index in ret:
		#print(index)
		strSrc=index
		#首先处理 hsWriteLog(0, GErrorMessage);  此种情况
		# hsWriteLog\(\s*(1|2|3)((?!")[\s\S])*?\); 根据日志级别来替换不同的日志名称
		sMatchEx=re.compile('hsWriteLog\(((?!")[\s\S])*?\);') # 处理类似 hsWriteLog(0,tmp); 没有引号的日志 (?!")要加在前面
		isMatch = sMatchEx.match(strSrc)
		if isMatch:  # 查找到 hsWriteLog(0, GErrorMessage); 就替换为  HsErrorLog("[%s][%s][%s]" ,sServerName,__func__,GErrorMessage);
			retE = sMatchEx.sub('HsErrorLog("[%s][%s][%s]" ,sServerName,__func__,GErrorMessage);',strSrc)
			info[index]=retE
		else:
			sMatchB=re.compile('hsWriteLog\([\s\S]*?"')#处理了换行的问题
			retB = sMatchB.sub('HsInfoLog("[%s][%s]',strSrc)
			strSrc = retB
			sMatchE=re.compile('("\s*,)|("\s*\);)')#处理了换行的问题
			retE = sMatchE.sub('",sServerName,__func__,',strSrc)
			info[index]=retE
	#替换文件数据
	fopen.seek(0)
	for key in info:
		cont = cont.replace(key, info[key])
	fopen.write(cont)
	fopen.close()

dirfile("F:\\0429D\\Sources\\src",[])
