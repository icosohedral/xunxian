# 寻仙
自动扫货脚本stall-scan.py 思路：
cv2模块匹配摊位中的目标货物，如果相似度大于阈值就标记摊位

改名查询 nameChangeHistory.py 思路：
查询接口（末尾加上需要查询的角色名，areaid应该是大区，140是不周山） http://apps.game.qq.com/xx/act/a20120706rename/ActInvite.php?areaid=140&rolename=
遍历查询改名前的名字，一直查询到最初那个为止
