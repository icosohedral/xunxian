import os, pyautogui, time
from PIL import Image, ImageGrab
import cv2, numpy

class Stall(object):
	def _init__(self):
		self.screen_size = pyautogui.size()
		return

	def mouseMove(self, xy):
		pyautogui.moveTo(xy[0], xy[1])

	def coordinate(self, co_type, co_obj=''):
		stall_dir = {'stall_1': [(40,100), (375,145)], 'stall_1_click': (171, 127), 'stall_1_mark': (347, 127), 
		'stall_2': [(40,100), (375,145+37*1)], 'stall_2_click': (171, 127+37*1), 'stall_2_mark': (347, 127+37*1), 
		'stall_3': [(40,100), (375,145+37*2)], 'stall_3_click': (171, 127+37*2), 'stall_3_mark': (347, 127+37*2), 
		'stall_4': [(40,100), (375,145+37*3)], 'stall_4_click': (171, 127+37*3),'stall_4_mark': (347, 127+37*3), 
		'stall_5': [(40,100), (375,145+37*4)], 'stall_5_click': (171, 127+37*4), 'stall_5_mark': (347, 127+37*4), 
		'stall_6': [(40,100), (375,145+37*5)], 'stall_6_click': (171, 127+37*5), 'stall_6_mark': (347, 127+37*5), 
		'stall_7': [(40,100), (375,145+37*6)], 'stall_7_click': (171, 127+37*6), 'stall_7_mark': (347, 127+37*6), 
		'stall_8': [(40,100), (375,145+37*7)], 'stall_8_click': (171, 127+37*7), 'stall_8_mark': (347, 127+37*7), 
		'stall_9': [(40,100), (375,145+37*8)], 'stall_9_click': (171, 127+37*8), 'stall_9_mark': (347, 127+37*8), 
		'stall_10': [(40,100), (375,145+37*9)], 'stall_10_click': (171, 127+37*9), 'stall_10_mark': (347, 127+37*9), 
		'stall_11': [(40,100), (375,145+37*10)], 'stall_11_click': (171, 127+37*10), 'stall_11_mark': (347, 127+37*10), 
		'stall_12': [(40,100), (375,145+37*11)], 'stall_12_click': (171, 127+37*11),'stall_12_mark': (347, 127+37*11), 
		}
		obj_dir = {'stall_1': [(40,100), (375,145)], #摊位第一条
				   'stall_1_click': (171, 127), #摊位第一条点击
				   'stall_refresh': (126, 573), #刷新摊位
				   'stall_empty_remark': [(312, 573)], #删除标记
				   'stall_goods': [(1548,212), (1880,550)], #货物
				   'mark': [(347, 157), (347, 183), (347, 215)], #标记
				   }
		colour_dir = {'stall_new': [(255, 255, 51), (255, 255, 255)], #gold and white
					  'stall_visited': [(128, 128, 128)], #grey
					}
		if co_type == 'object':
			return obj_dir[co_obj]
		elif co_type == 'stall':
			return stall_dir
		else:
			return colour_dir[co_obj]
	
	def screenshot(self, from_xy, to_xy):
		pic = ImageGrab.grab(bbox=(from_xy[0], from_xy[1], to_xy[0], to_xy[1]))
		return pic
		
	def matchColour(self, image, RGB):
		width, height = image.size[0], image.size[1]
		for y in range(0, height):
			for x in range(0, width):
				r,g,b = image.getpixel((x,y))
				if r == RGB[0] and g == RGB[1] and b == RGB[2]:
					return True
		#print('no found')
		return False
		
	def matchIMG(self, template, target):
		template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
		target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
		theight, twidth = template.shape[::-1]
		#执行模板匹配，采用的匹配方式cv2.TM_CCORR_NORMED
		result = cv2.matchTemplate(target, template,cv2.TM_CCORR_NORMED)
		threshold = 0.99
		print('sim: %s' % str(cv2.minMaxLoc(result)[1])[:4])
		if cv2.minMaxLoc(result)[1] > threshold:
			return True
		return False

	def setMark(self):
		mark = self.coordinate('stall')['stall_%s_mark' % str(self.stall_now)]
		pyautogui.click(x=mark[0],  y=mark[1], button='left')
		time.sleep(0.3)
		pyautogui.click(x=mark[0],  y=mark[1]+30, button='left')
		time.sleep(0.3)
		self.stall_now += 1
		print('set Mark')
		if self.stall_now == 13:
			print('mark 13, exit')
			os._exit(1)

	def scan(self, targets):
		count = 0
		time.sleep(1)
		target_goods = []
		for target in targets:
			target_good = Image.open(target)
			target_good = cv2.cvtColor(numpy.asarray(target_good),cv2.COLOR_RGB2BGR)
			target_goods.append(target_good)
		self.stall_now = 1
		stall_dir = self.coordinate('stall')
		while True:
			print('\n[INFO] COUNT: %s' % str(count))
			#刷新摊位
			refresh_xy = self.coordinate('object', 'stall_refresh')
			pyautogui.click(x=refresh_xy[0],  y=refresh_xy[1], button='left')
			print('refresh')
			#检查是否扫过
			stall_now_now_xy = stall_dir['stall_%s' % str(self.stall_now)]
			stall_now_img = self.screenshot(stall_now_now_xy[0], stall_now_now_xy[1])
			empty = self.matchColour(stall_now_img, self.coordinate('colour', 'stall_visited')[0])
			#print(self.coordinate('colour', 'stall_visited')[0])
			print('check')
			if not empty:
				#点击摊位
				xy = stall_dir['stall_%s_click' % str(self.stall_now)]
				pyautogui.click(x=xy[0],  y=xy[1], button='left')
				time.sleep(0.3)
				print('click')
				#摊位截图
				stall_img = self.screenshot(self.coordinate('object', 'stall_goods')[0], self.coordinate('object', 'stall_goods')[1])
				#stall_img.save('%s.png' % str(count))
				print('get goods')
				# 匹配物品
				stall_img = cv2.cvtColor(numpy.asarray(stall_img), cv2.COLOR_RGB2BGR)
				for target_good in target_goods:
					match = self.matchIMG(target=stall_img, template=target_good)
					if match:
						self.setMark()
						continue
				#if count == 1:
				#	break
				count += 1
			else:
				print('exit')
				break


if __name__ == "__main__":
	path = os.path.split(os.path.realpath(__file__))[0] + '\\targets\\'
	targets = []
	for file in os.listdir(path):
		targets.append(path + file)
	if targets:
		Stall().scan(targets)
		