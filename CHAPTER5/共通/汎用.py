#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃共通モジュール
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅱ.定数
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅲ．クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class class汎用:
	#┬
	#□└┐シーン
		#□タイトル画面
		#□プレイ画面
		#□ゲームオーバー画面
	定数_シーン_タイトル	= 0
	定数_シーン_プレイ		= 1 
	定数_シーン_終了		= 2
	#┴　┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃発射有無の判定
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def Funワンキー入力():
		#┬
		#◇┐ワンキーが押されているかどうかを調べる
		if pyxel.btn(pyxel.KEY_SPACE)				: return 1
		elif pyxel.btn(pyxel.GAMEPAD1_BUTTON_Y)		: return 1
		#　├→（押された場合）
			#○『押されている』を返す
			#┴
		#│
		#◇┐ワンキーが離されたかどうかを調べる
		if pyxel.btnr(pyxel.KEY_SPACE)				: return -1
		elif pyxel.btnr(pyxel.GAMEPAD1_BUTTON_Y)	: return -1
		#　├→（離された場合）
			#○『離された』を返す
			#┴
		#　└┐（その他）
			#┴
		#│
		#○『なにもなし』を返す
		return 0
		#┴　┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃移動入力
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def Fun移動入力():
		if pyxel.btn(pyxel.KEY_LEFT ) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT  ) :
			return 1
		elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT ):
			return 2
		elif pyxel.btn(pyxel.KEY_UP   ) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP    ):
			return 3
		elif pyxel.btn(pyxel.KEY_DOWN ) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN  ):
			return 4
		else:
			return 0

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃プレイヤーから一定距離離れた位置を得る 
	#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【引き数】最低の離す距離
	#┃【戻り値】リスト(X座標,Y座標)
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def Fun座標取得(argDist, argX, argY):
		#┬
		#◎└┐座標が決まるまで繰り返す
		while True:
			#○ランダムに座標を求める
			x = pyxel.rndi(0, pyxel.width  - 8)
			y = pyxel.rndi(0, pyxel.height - 8)
			#│
			#○プレイヤーとの差を求める
			diff_x = x - argX
			diff_y = y - argY
			#│
			#◇┐プレイヤーとの差によって、座標を確定する
			if diff_x**2 + diff_y**2 > argDist**2:
			#　├→（指定の距離以上に離れている場合）
				#▼座標を返す
				return (x, y)
				#┴
			#　└┐（その他）
		#┴　┴　┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃衝突の有無を得る
	#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【引き数】① OBJ型 ：対象物（1つ目）
	#┃　　　　　② OBJ型 ：対象物（2つ目）
	#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【戻り値】① 論理型：衝突あり：True／衝突なし：False
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def Fn衝突処理(
		argObj1,    #① 対象物１
		argObj2     #② 対象物２
		):
		#┬
		#○対象物１の座標範囲を求める
		tmpObj1_X1 = argObj1.座標_X軸 + argObj1.衝突範囲[0]
		tmpObj1_Y1 = argObj1.座標_Y軸 + argObj1.衝突範囲[1]
		tmpObj1_X2 = argObj1.座標_X軸 + argObj1.衝突範囲[2]
		tmpObj1_Y2 = argObj1.座標_Y軸 + argObj1.衝突範囲[3]
		#│
		#○対象物２の座標範囲を求める
		tmpObj2_x1 = argObj2.座標_X軸 + argObj2.衝突範囲[0]
		tmpObj2_y1 = argObj2.座標_Y軸 + argObj2.衝突範囲[1]
		tmpObj2_x2 = argObj2.座標_X軸 + argObj2.衝突範囲[2]
		tmpObj2_y2 = argObj2.座標_Y軸 + argObj2.衝突範囲[3]
		#│
		#◇┐衝突の有無を返す
		if (
			tmpObj1_X1 > tmpObj2_x2 or
			tmpObj1_X2 < tmpObj2_x1 or
			tmpObj1_Y1 > tmpObj2_y2 or
			tmpObj1_Y2 < tmpObj2_y1
		):
		#　├→（座標範囲が重なっていない場合）
			#▼『衝突なし』を返す
			return False
		#　│
		#　└┐（その他）
		else:
			#▼『衝突あり』を返す
			return True
		#┴　┴