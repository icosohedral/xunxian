import requests, os, urllib, json, sys
# urllib.parse.quote(text)
# urllib.parse.unquote(text, 'utf-8')

class XX(object):
	def __init__(self):
		return
	
	def rename(self, rolename):
		checkList, nameInfo, count = [], {}, 0
		name = rolename
		def check(name):
			url = 'http://apps.game.qq.com/xx/act/a20120706rename/ActInvite.php?areaid=140&rolename=%s' % urllib.parse.quote(name)
			res = json.loads(requests.get(url).text.split('=')[1])
			code = res['ret_code']
			if code == '0':
				info = urllib.parse.unquote(json.loads(res['msg'])['body']['1'], 'utf-8').split()
				result = {'name_before': info[0], 'modify_date': '%s %s' % (info[1], info[2]), 'name_after': info[3]}
				#result = {info[3]: '%s %s' % (info[1], info[2])}
				return result
			else:
				return False
		while True:
			result = check(name)
			if not result:
				print('[INFO] No name modifying record found.')
				return
			if result['name_before'] not in checkList:
				checkList.append(result['name_before'])
				nameInfo[count] = result
				name = result['name_before']
				count += 1
			else:
				#initialName = result['name_before']
				#print('[INFO] Every name has checked.')
				break
		for i in range(count-1, -1, -1):
			if i == count-1:
				print('[Initial Name] %s' % nameInfo[i]['name_before'])
				print('[%s] %s' % (nameInfo[i]['modify_date'], nameInfo[i]['name_after']))
			else:
				print('[%s] %s' % (nameInfo[i]['modify_date'], nameInfo[i]['name_after']))
			
		
if __name__ == '__main__':
	try:
		rolename = sys.argv[1]
	except:
		rolename = '今夜雪糕'
	XX().rename(rolename)