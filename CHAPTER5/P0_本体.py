#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃技術評論社 ゲームで学ぶPython！ CHAPTER5
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel
import P0_共通		as		Common
from P1_背景		import 	classScreen
from P2_プレイヤー	import 	classPlayer
from P3_ザコキャラ	import 	classZako
from P4_ボスキャラ	import 	classBoss

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅱ.定数
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅲ．クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Game:
    #┬
    #□ゲームオーバー表示待ち(単位：フレーム)
	WAIT_GAMEOVER   = 300
	#│
	#□└┐出現カウント(30で１秒)
		#□ボスキャラ用
		#□ザコキャラ用
	INTERVAL_ZAKO		= 400
	INTERVAL_BOSS		= 200
    #┴ ┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃０．初期化
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def __init__(self):
		#┬
        #○Pyxelを初期化する
		self.Init_Resouce()
        #│
        #○└┐制御データを初期化する
            #○スコアを初期化する
            #○シーンを初期化する
		self.Score      	= 0
		self.Scene      	= None
		self.TimeGameover 	= 0
            #┴
		#│
        #○└┐インスタンスを初期化する
            #○背景を初期化する
            #○自機を初期化する
            #○ザコキャラを初期化する
            #○ボスキャラを初期化する
            #○爆発を初期化する
		self.objScreen	= None
		self.objPlayer	= None
		self.objZako	= []
		self.objBoss	= []
		self.objCrush	= [] 
            #┴
        #│
        #○└┐最終準備
            #●背景を生成する(背景はシーンによらず常に存在する)
            #●タイトル画面を準備する
            #○ゲームの実行を開始する
		classScreen(self)
		self.Sub_Scene(Common.SCENE_TITLE)
		pyxel.run(self.update, self.draw)
		#┴　┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃リソースを初期化する
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def Init_Resouce(self):
		#┬
		#○画面を初期化する
		pyxel.init(300, 200, "SPACE ATACK")
		#│
		#○リソースファイルを読み込む
		#pyxel.load("res-org.pyxres")		# 最初のリソース
		pyxel.load("res-kureha.pyxres")		# 呉羽のリソース
		#pyxel.load("res-sumin.pyxres")		# スー民のリソース
		#│
		#○Soundデータを登録する
		pyxel.sounds[50].mml(
			"t100 @1 o2 q7 v7 l4" +
			"l8d4a4g2.fed4c<b->c<a>e4d1.a4>" +
			"c4<b2.gfe4fga1&a1d4a4g2.fed4c<b->c<a>e4d1."
			)
		pyxel.sounds[51].mml(
			"t100 @0 o1 q7 v4 l2" +
			"l8dafadbgbd>c<a>c<db-fb-e>c<a>c" +
			"<daf+adaf+agb-a>c" +
			"<dafadbgbdbgbdb-g+b-c" +
			"+aeadaeac+aea<b>ac+adafadbgbd>c" +
			"<a>c<db-fb-e>c<a>c<daf+adaf+adaf+a"
			)
		#│
		#○Musicデータを登録する
		pyxel.musics[7].set([50],[51])
		#┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．アプリを更新
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def update(self):
		#┬
        #●背景を更新する
		self.objScreen.update()
		#│
        #○└┐キャラクタを更新する
			#●プレイヤーを更新する
			#●敵キャラを更新する
		self.update_player()
		self.update_Zako()
		self.update_Boss()
		#│
        #○└┐その他を更新する
            #●破壊を更新する
            #●画面を更新する
		self.update_Crush()
		self.update_Scene()
        #┴　┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃プレイヤーを更新
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def update_player(self):
		#┬
        #◇┐自機を更新する
		if self.objPlayer is not None:
        #　├→（自機が存在する場合）
            #●自機を更新する
			self.objPlayer.update()
			#┴
		#　└┐（その他）
        #┴　┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃ザコキャラを更新
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def update_Zako(self):
		#┬
		#◎└┐すべてのザコキャラとの接触を判定する
		for tmpObj in self.objZako.copy():
			#│＼（すべてのザコキャラを処理し終えた場合）
			#│ ▼繰り返し処理を抜ける
			#●ザコキャラを更新する
			tmpObj.update()
			#│
			#◇┐ザコキャラを更新する
			if self.objPlayer is not None:
			#　├→（自機が存在する場合）
                #●自機との接触を調べる
				if Common.Fun_Collision(tmpObj, self.objPlayer):
                #　 ＼（接触している場合）
                    #●ザコキャラを消滅する
					tmpObj.Sub_Collision()
			#┴　┴　┴
		#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		#┃ボスキャラを更新
		#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def update_Boss(self):
		#┬
		#◎└┐すべてのボスキャラとの接触を判定する
		for tmpObj in self.objBoss:
			#│＼（すべてのスキャラを処理し終えた）
			#│ ▼繰り返し処理を抜ける
			#●ボスキャラを更新する
			tmpObj.update()
			#│
			#◇┐ザコキャラを更新する
			if self.objPlayer is not None:
			#　├→（自機が存在する場合）
                #●自機との接触を調べる
				if Common.Fun_Collision(tmpObj, self.objPlayer):
				#　 ＼（接触している場合）
					#●自機を爆破する
					self.objPlayer.Sub_Collision()
				#┴　┴
			#　└┐（その他）
		#┴　┴　┴
        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃破壊を更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def update_Crush(self):
		#┬
        #◎└┐すべての爆発を更新する
		for tmpObj in self.objCrush.copy():
            #│＼（すべての爆発を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #●当該の爆発を更新
			tmpObj.update()
        #┴　┴
        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃画面を更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def update_Scene(self):
		#┬
        #◇┐シーンを更新する
		if self.Scene == Common.SCENE_TITLE: 
        #　├→（シーンが『タイトル』の場合）
			#◇┐が押されている場合：
			if Common.Fun_FireOn():
			#　├→（ジェット噴射の指示が『ある』場合）
                #○BGMの再生を止める
                #●プレー画面を準備する
				pyxel.stop()
				self.Sub_Scene(Common.SCENE_PLAY)
                #┴
            #　└┐（その他）
                #┴

		elif self.Scene == Common.SCENE_PLAY:
        #　├→（シーンが『プレイ中』の場合）
			#◇┐ザコキャラを追加する
			if self.timer_zako == 0:
			#　├→（タイマーがゼロの場合）
				#●プレイヤーから距離を30以上離す
				#○ザコキャラのリストに追加する
				#○タイマーをリセットする
				position = Common.Fun_Position(
					30,
					self.objPlayer.X,
					self.objPlayer.Y
					)
				classZako(self, position[0], position[1])
				self.timer_zako = self.INTERVAL_ZAKO
				#┴

			else:
			#　└┐（その他）
				#○タイマーを減らす
				self.timer_zako -= 1
				#┴
			#│
			#◇┐ボスキャラを追加する
			if self.timer_boss == 0:
			#　├→（タイマーがゼロの場合）
				#●プレイヤーから距離を60以上離す
				#○ボスキャラのリストに追加する
				#○タイマーをリセットする
				position = Common.Fun_Position(
					60,
					self.objPlayer.X,
					self.objPlayer.Y
					)
				classBoss(self, position[0], position[1])
				self.timer_boss = self.INTERVAL_BOSS
				#┴

			else:
			#　└┐（その他）
				#○タイマーを減らす
				self.timer_boss -= 1
			#┴　┴

		elif self.Scene == Common.SCENE_GAMEOVER:
        #　├→（シーンが『ゲームオーバー』の場合）
            #◇┐待ち時間を減らす
			if self.TimeGameover > 0:
            #　├→（画面表示時間が残っている場合）
                #●待ち時間をカウントダウンする
				self.TimeGameover -= 1
                #┴

			else:
            #　└┐（その他）
                #●タイトル画面を準備する
				self.Sub_Scene(Common.SCENE_TITLE)
            #┴　┴
		#　└┐（その他）
        #┴　┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃２．描画処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def draw(self):
		#┬
        #○画面をクリアする
        #●背景を描画する
		pyxel.cls(0)
		self.objScreen.draw()
        #│
        #◇┐自機を描画する
		if self.objPlayer is not None:
        #　├→（自機が存在する場合）
            #●描画する
			self.objPlayer.draw()
			#┴
		#　└┐（その他）
			#┴
        #│
        #◎└┐ザコキャラを描画する
		for tmpObj in self.objZako:
            #│＼（すべてのザコキャラを処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #●描画する
			tmpObj.draw()
			#┴
        #│
        #◎└┐ボスキャラを描画する
		for tmpObj in self.objBoss:
            #│＼（すべてのボスキャラを処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #●描画する
			tmpObj.draw()
			#┴
        #│
        #◎└┐爆発エフェクトを描画する
		for tmpObj in self.objCrush:
            #│＼（すべての爆発を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #●描画する
			tmpObj.draw()
			#┴
        #│
        #○スコアを描画する
		pyxel.text(3, 3, f"SCORE {self.Score:3}", 7)
        #│
        #◇┐シーンを描画する
		if self.Scene == Common.SCENE_TITLE:
        #　├→（シーンが『タイトル』の場合）
            #〇タイトル画面を表示する
			pyxel.text(90, 70, "- Press SPACE Key or Button -", 6)
			#┴

		elif self.Scene == Common.SCENE_GAMEOVER:
        #　├→（シーンが『ゲームオーバー』の場合）
            #〇ゲームオーバー画面を表示する
			pyxel.text(120, 70, "- GAME OVER -", 8)
			#┴
        #　└┐（その他）
        #┴　┴
		
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃シーンを準備する
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃【引き数】① 整数型：シーン
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	def Sub_Scene(self,
        argScene    #① シーン
        ):
		#┬
        #○引数を退避する
		self.Scene = argScene
        #│
        #◇┐画面を表示する
		if self.Scene == Common.SCENE_TITLE:
        #　├→（シーンが『タイトル』の場合）
			#□└┐タイマー
				#□ザコキャラの出現（初期値：ゼロ）
				#□ボスキャラの出現（初期値：ゼロ）
				#□ゲームオーバー
			self.timer_zako		= 0
			self.timer_boss		= 0
			self.timer_GameOver	= self.WAIT_GAMEOVER
				#┴
			#│
			#□└┐プレイヤーの位置
				#□X座標（初期値：画面の2分の1から8ドット左）
				#□Y座標（初期値：画面の4分の1）
			self.player_x 		= (pyxel.width - 8) / 2
			self.player_y 		= pyxel.height      / 4
				#┴
			#│
            #〇自機を抹消する
			self.objPlayer = None
            #│
            #○BGMを鳴らす
			pyxel.playm(0, loop=True)
            #┴

		elif self.Scene == Common.SCENE_PLAY:
        #　├→（シーンが『プレイ中』の場合）
            #〇ザコキャラを抹消(リスト全体をクリア)する
            #〇ボスキャラを抹消(リスト全体をクリア)する
			self.objZako.clear()
			self.objBoss.clear()
            #│
            #○スコアをリセットする
            #○BGMを鳴らす
			self.Score      = 0
			pyxel.playm(1, loop=True)
            #│
            #●プレイヤーを生成する
			classPlayer(self, 120, 50)
            #┴

		elif self.Scene == Common.SCENE_GAMEOVER:
        #　├→（シーンが『ゲームオーバー』の場合）
            #○待ち時間をセットする
			self.TimeGameover = self.WAIT_GAMEOVER
            #│
            #●レイヤーを抹消する
			self.objPlayer = None
            #┴
		#　└┐（その他）
        #┴　┴