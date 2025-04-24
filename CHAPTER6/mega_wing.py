#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel
import time

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅱ．ゲームクラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Game:
    #┬
    #□タイトル画面
    #□プレイ画面
    #□ゲームオーバー画面
    SCENE_TITLE     = 0
    SCENE_PLAY      = 1 
    SCENE_GAMEOVER  = 2
    #│
    #□ゲームオーバー表示待ち(単位：フレーム)
    WAIT_GAMEOVER   = 180
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【公　開】０．初期化処理 
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(self):
		#┬
        #○└┐Pyxelを初期化する
            #○画面を初期化する
            #○リソースファイルを読み込む
            #┴
        pyxel.init(120, 160, title="Mega Wing")
        pyxel.load("mega_wing.pyxres")
        #│
        #○└┐制御データを初期化する
            #○スコアを初期化する
            #○シーンを初期化する
            #○プレイ時間を初期化する
            #○難易度を初期化する
        self.Score      = 0
        self.Scene      = None
        self.TimePlay   = 0
        self.Level      = 0
            #┴
        #│
        #○└┐インスタンスを初期化する
            #○背景を初期化する
            #○自機を初期化する
            #○敵機を初期化する
            #○弾(自機)を初期化する
            #○弾(敵機)を初期化する
            #○爆発を初期化する
        self.objScreen          = None
        self.objPlayer          = None
        self.objEnemie          = []
        self.objBullet_Player   = [] 
        self.objBullet_Enemy    = [] 
        self.objCrush           = [] 
            #┴
        #│
        #○└┐最終準備
            #●背景を生成する(背景はシーンによらず常に存在する)
            #●タイトル画面を準備する
            #○ゲームの実行を開始する
            #┴
        classScreen(self)
        self.Sub_Scene(self.SCENE_TITLE)
        pyxel.run(self.update, self.draw)
        #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【非公開】１．更新処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #●背景を更新する
        self.objScreen.update()
        #│
        #○└┐1.キャラクタを更新する
            #○1.1.自機を更新する
            #○1.2.敵機を更新する
        self.update_Player()
        self.update_Enemie()
            #┴
		#│
        #○└┐2.弾を更新する
            #○2.1.弾(自機)を更新する
            #○2.2.弾(敵機)を更新する
        self.update_BulletPlayer()
        self.update_BulletEnemy()
            #┴
		#│
        #○└┐3.その他を更新する
            #●3.1.破壊を更新する
            #●3.2.画面を更新する
        self.update_Crush()
        self.update_Scene()
        #┴　┴
        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃【非公開】1-1.1.弾(自機)を更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update_Player(self):
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
        #┃【非公開】1-1.2.敵機を更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update_Enemie(self):
		#┬
		#◎└┐敵機を更新する
        for tmpObj in self.objEnemie.copy():
			#│＼（すべての敵機を処理し終えた）
			#│ ▼繰り返し処理を抜ける
            #●敵機を更新する
            tmpObj.update()
            #│
            #◇┐自機と衝突する
            if self.objPlayer is not None:
            #　├→（自機が存在し、衝突している場合）
                #●自機との衝突を調べる
                if Fun_Collision(self.objPlayer, tmpObj):
                #　 ＼（衝突している場合）
                    #●自機を衝突させる
                    self.objPlayer.Sub_Collision()
                #┴　┴
            #　└┐（その他）
        #┴　┴　┴
        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃【非公開】1-2.1.弾(自機)を更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update_BulletPlayer(self):
		#┬
		#◎└┐弾(自機)を更新する
        for tmpObj in self.objBullet_Player.copy():
			#│＼（すべての弾を処理し終えた）
			#│ ▼繰り返し処理を抜ける
            #│
            #●弾(自機)を更新する
            tmpObj.update()
            #│
            #◎└┐すべての敵機との衝突判定を行う
            for tmpObjEnemy in self.objEnemie.copy():
                #│＼（すべての敵機を処理し終えた場合）
                #│ ▼繰り返し処理を抜ける
                #│
                #●敵機との衝突を調べる
                if Fun_Collision(tmpObjEnemy, tmpObj):
                #　 ＼（衝突している場合）
                    #●弾(自機)を命中させる
                    #●敵機を被弾させる
                    tmpObj.Sub_Collision()
                    tmpObjEnemy.Sub_Collision() 
        #┴　┴　┴　┴
        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃【非公開】1-2.2.弾(敵機)を更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update_BulletEnemy(self):
		#┬
        #◎└┐すべての弾(敵機)を更新する
        for tmpObj in self.objBullet_Enemy.copy():
            #│＼（すべての弾(敵機)を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #│
            #●弾(敵機)を更新する
            tmpObj.update()
            #│
            #◇┐プレイヤーとの衝突を処理する
            if self.objPlayer is not None:
            #　├→（）
                #●自機との位置関係を調べる
                if Fun_Collision(self.objPlayer, tmpObj):
                #　 ＼（衝突している場合）
                    #●弾(敵機)を命中させる
                    #●自機を被弾させる
                    tmpObj.Sub_Collision()
                    self.objPlayer.Sub_Collision()
        #┴　┴　┴　┴
        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃【非公開】1-3.1.破壊を更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update_Crush(self):
		#┬
        #◎└┐すべての爆発を更新する
        for tmpObj in self.objCrush.copy():
            #│＼（すべての爆発を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #│
            #●当該の爆発を更新
            tmpObj.update()
        #┴　┴
        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃【非公開】1-3.2.更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update_Scene(self):
        #◇┐シーンを更新する
        if self.Scene == self.SCENE_TITLE: 
        #　├→（シーンが『タイトル』の場合）
            #◇┐
            if pyxel.btnp(pyxel.KEY_RETURN):
            #　├→（リターンキーが押された場合）
                #○BGMの再生を止める
                #●プレー画面を準備する
                pyxel.stop()
                self.Sub_Scene(self.SCENE_PLAY)
                #┴
            #　└┐（その他）
                #┴
        #　│
        elif self.Scene == self.SCENE_PLAY:
        #　├→（シーンが『プレイ中』の場合）
            #○プレイ時間をカウントアップする
            #○15秒毎に難易度を上げる
            self.TimePlay += 1
            self.Level = self.TimePlay // 450 + 1
            #│
            #◇┐敵機を出現させる
            tmpInterval = max(60 - self.Level * 10, 10)
            if self.TimePlay % tmpInterval == 0:
            #　├→（出現タイミングの場合）
                #○機種をランダムに求める
                #●求めた機種で、敵機を生成する
                tmpKind  = pyxel.rndi(classEnemy.TYPE_A, classEnemy.TYPE_C)
                classEnemy(self, tmpKind, self.Level, pyxel.rndi(0, 112), -8)
                #┴
            #　└┐（その他）
            #┴　┴
        #　│
        elif self.Scene == self.SCENE_GAMEOVER:
        #　├→（シーンが『ゲームオーバー』の場合）
            #◇┐待ち時間を減らす
            if self.TimeGameover > 0:
            #　├→（画面表示時間が残っている場合）
                #●待ち時間をカウントダウンする
                self.TimeGameover -= 1
                #┴
            #　│
            else:
            #　└┐（その他）
                #●タイトル画面を準備する
                self.Sub_Scene(self.SCENE_TITLE)
            #┴　┴
		#　└┐（その他）
        #┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【非公開】２．描画処理
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
        #◎└┐敵機を描画する
        for tmpObj in self.objEnemie:
            #│＼（すべての敵機を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #│
            #●描画する
            tmpObj.draw()
			#┴
        #│
        #◎└┐弾(自機)を描画する
        for tmpObj in self.objBullet_Player:
            #│＼（すべての弾を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #│
            #●描画する
            tmpObj.draw()
			#┴
        #│
        #◎└┐弾(敵機)を描画する
        for tmpObj in self.objBullet_Enemy: 
            #│＼（すべての弾を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #│
            #●描画する
            tmpObj.draw()
			#┴
        #│
        #◎└┐爆発エフェクトを描画する
        for tmpObj in self.objCrush:
            #│＼（すべての爆発を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #│
            #●描画する
            tmpObj.draw()
			#┴
        #│
        #○スコアを描画する
        #○レベルを描画する
        pyxel.text(10, 4, f"SCORE {self.Score:5}", 7)
        pyxel.text(80, 4, f"LEVEL {self.Level:1}", 7)
        #│
        #◇┐シーンを描画する
        if self.Scene == self.SCENE_TITLE:
        #　├→（シーンが『タイトル』の場合）
            #〇タイトル画面を表示する
            pyxel.blt(0, 18, 2, 0, 0, 120, 120, 15)
            pyxel.text(31, 148, "- PRESS ENTER -", 6)
			#┴
        #　│
        elif self.Scene == self.SCENE_GAMEOVER:
        #　├→（シーンが『ゲームオーバー』の場合）
            #〇ゲームオーバー画面を表示する
            pyxel.text(43, 78, "GAME OVER", 8)
			#┴
        #　└┐（その他）
        #┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【公　型】シーンを準備する
    #┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #┃【引き数】① 整数型：シーン
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def Sub_Scene(
        self,
        argScene    #① シーン
        ):
		#┬
        #○引数を退避する
        self.Scene = argScene
        #│
        #◇┐画面を表示する
        if self.Scene == self.SCENE_TITLE:
        #　├→（シーンが『タイトル』の場合）
            #●自機を抹消する
            self.objPlayer = None
            #│
            #●敵機をクリアする
            #●弾(自分)と敵機を削除する
            #●弾(敵機)と敵機を削除する
            self.objEnemie.clear()
            self.objBullet_Player.clear()
            self.objBullet_Enemy.clear()
            #│
            #○BGMを鳴らす ※繰り返し鳴らす
            pyxel.playm(0, loop=True)
            #┴
        #　│
        elif self.Scene == self.SCENE_PLAY:
        #　├→（シーンが『プレイ中』の場合）
            #○スコアをリセットする
            #○プレイ時間をリセットする
            #○難易度レベルをリセットする
            self.Score      = 0
            self.TimePlay   = 0
            self.Level      = 1
            #│
            #○BGMを鳴らす ※繰り返し鳴らす
            pyxel.playm(1, loop=True)
            #│
            #●自機を生成する
            classPlayer(self, 56, 140)
            #┴
        #　│
        elif self.Scene == self.SCENE_GAMEOVER:
        #　├→（シーンが『ゲームオーバー』の場合）
            #○待ち時間をセットする
            self.TimeGameover = self.WAIT_GAMEOVER
            #│
            #●自機を抹消する
            self.objPlayer = None
            #┴
		#　└┐（その他）
        #┴　┴
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅱ.背景クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class classScreen:
    #┬
    #□星の数
    NUM_STARS = 100 
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【公　開】０．初期化処理
    #┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #┃【引き数】① OBJ型 ：生成先のオブジェクト
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(
        self,
        argGame     # 生成先のオブジェクト
        ):
		#┬
        #○引数を退避する
        self.objGame    = argGame   # ゲームへの参照
        #│
        #○基本データを初期化する
        self.Star       = []        # 星リスト ※座標とベクトル
        #│
        #◎└┐すべての星を追加する
        for cnt in range(classScreen.NUM_STARS):
            #│＼（すべての星を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
            #│
            #○└┐座標と速度を求める
                #○X座標を求める
                #○Y座標を求める
                #○方向の速度を求める
            tmpX  = pyxel.rndi(0, pyxel.width  - 1 )  
            tmpY  = pyxel.rndi(0, pyxel.height - 1 )  
            tmpVY = pyxel.rndf(1, 2.5              ) 
                #┴
            #│
            #○星を追加する
            self.Star.append((tmpX, tmpY, tmpVY))
            #┴
        #│
        #〇背景を生成する
        self.objGame.objScreen = self
        #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【非公開】１．更新処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #◎└┐すべての星を更新する
        for tmpID, (tmpX, tmpY, tmpVY) in enumerate(self.Star):
			#│＼（すべての星を処理し終えた場合）
			#│ ▼繰り返し処理を抜ける
            #│
            #○座標を画面下方向に移動する
            tmpY += tmpVY
            if tmpY >= pyxel.height:
            #│＼（画面下に達した場合）
                #○座標を画面上に移動する
                tmpY -= pyxel.height
                #┴
            #│
            #○座標を更新する
            self.Star[tmpID] = (tmpX, tmpY, tmpVY)
        #┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【非公開】２．描画処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        #◇┐銀河を描画する
        if self.objGame.Scene != self.objGame.SCENE_TITLE:
        #　├→（シーンが『タイトル』以外の場合）
            #│
            #○銀河を描画する
            pyxel.blt(0, 0, 1, 0, 0, 120, 160)
            #┴
		#　└┐（その他）
			#┴
        #│
        #◎└┐すべての星を描画する
        for tmpX, tmpY, tmpSpeed in self.Star:
			#│＼（）
			#│ ▼繰り返し処理を抜ける
			#│
            #○速度に応じて色を変える
            #○星を表示する
            tmpColor = 12 if tmpSpeed > 1.8 else 5
            pyxel.pset(tmpX, tmpY, tmpColor)
        #┴　┴
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅲ.自機クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class classPlayer:
    #┬
    #□移動速度
    #□弾の発射間隔
    MOVE_SPEED      = 2
    SHOT_INTERVAL   = 6 
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【公　開】０．初期化処理
    #┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #┃【引き数】① OBJ型 ：生成先のオブジェクト
    #┃　　　　　② 整数型：Ｘ座標
    #┃　　　　　③ 整数型：Ｙ座標
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(
        self,
        argGame,    # 生成先のオブジェクト
        argX,       # Ｘ座標
        argY        # Ｙ座標
        ):
		#┬
        #○引数を退避する
        self.objGame    = argGame
        self.X          = argX
        self.Y          = argY
        #│
        #○└┐基本データを初期化する
            #○当たり判定の領域を初期化する
            #○弾発射までの残り時間を初期化する
        self.HitArea    = (1, 1, 6, 6)
        self.TimeShot   = 0
            #┴
        #│
        #〇自機を生成する
        self.objGame.objPlayer  = self
        #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【非公開】１．更新処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #◇┐キー入力で自機を移動させる
        if pyxel.btn(pyxel.KEY_LEFT ) : self.X -= classPlayer.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT) : self.X += classPlayer.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_UP   ) : self.Y -= classPlayer.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_DOWN ) : self.Y += classPlayer.MOVE_SPEED
        #│
        #〇自機を移動する
        self.X = max(self.X, 0                  )
        self.X = min(self.X, pyxel.width  - 8   )
        self.Y = max(self.Y, 0                  )
        self.Y = min(self.Y, pyxel.height - 8   )
        #│
        #◇┐弾の発射間隔を制限する
        if self.TimeShot > 0:
        #　├→（）
            #○発射可能までの時間を減らす
            self.TimeShot -= 1
            #┴
        #│
        #◇┐弾を発射する
        if pyxel.btn(pyxel.KEY_SPACE) and self.TimeShot == 0:
        #　├→（発射可能で、スペースキーを押した場合）
            #○弾を生成する
            classBullet(
                self.objGame,
                classBullet.OWNER_PLAYER,
                self.X, self.Y - 3,
                -90,
                5
                )
            #│
            #○弾発射音を鳴らす
            pyxel.play(3, 0)
            #│
            #○発射可能までの時間をリセットする
            self.TimeShot = classPlayer.SHOT_INTERVAL
            #┴
        #　└┐（その他）
        #┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【非公開】２．描画処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        #○自機を描画する
        pyxel.blt(self.X, self.Y, 0, 0, 0, 8, 8, 0)
        #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【公　型】被弾・衝突を処理する
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def Sub_Collision(self):
		#┬
        #●爆発を生成する
        classCrush(self.objGame, self.X + 4, self.Y + 4)
        #│
        #○BGMを止める
        #○爆発音を鳴らす
        pyxel.stop()
        pyxel.play(0, 2)
        #│
        #○自機を抹消する
        self.objGame.objPlayer = None
        #│
        #●ゲームオーバー画面を表示する
        self.objGame.Sub_Scene(self.objGame.SCENE_GAMEOVER)
        #┴
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅳ.敵機クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class classEnemy:
    #┬
    #□機種Ａ
    #□機種Ｂ
    #□機種Ｃ
    TYPE_A = 0
    TYPE_B = 1
    TYPE_C = 2
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【公　開】０．初期化処理
    #┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #┃【引き数】① OBJ型 ：生成先のオブジェクト
    #┃　　　　　② 整数型：機種
    #┃　　　　　③ 整数型：難易度
    #┃　　　　　④ 整数型：Ｘ座標
    #┃　　　　　⑤ 整数型：Ｙ座標
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(
        self,
        argGame,    #① 生成先のオブジェクト
        argType,    #② 機種
        argLevel,   #③ 難易度
        argX,       #④ Ｘ座標
        argY        #⑤ Ｙ座標
        ):
		#┬
        #○引数を退避する
        self.objGame    = argGame
        self.Type       = argType
        self.Level      = argLevel
        self.X          = argX
        self.Y          = argY
        #│
        #○└┐基本データを初期化する
            #○当たり判定の領域を初期化する
            #○防御力を初期化する
            #○生存時間を初期化する
            #○衝突有無を初期化する
        self.HitArea    = (0, 0, 7, 7)
        self.Armor      = self.Level - 1
        self.TimeLife   = 0
        self.Collided   = False
        #│
        #〇敵機リストに追加する
        self.objGame.objEnemie.append(self)
        #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【非公開】１．更新処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #○生存時間をカウントする
        self.TimeLife += 1
        #│
        #◇┐敵機を更新する
        if self.Type == classEnemy.TYPE_A:
        #　├→（機種が『Ａ』の場合）
            #○前方に移動させる
            self.Y += 1.2
            #│
            #◇┐弾を発射する
            if self.TimeLife % 50 == 0:
            #　├→（生存時間が50カウントの場合）
                #●自機の角度を求める
                #●弾を発射する
                tmpAngle = self.Fun_Angle()
                classBullet(
                    self.objGame,
                    classBullet.OWNER_ENEMY,
                    self.X, self.Y,
                    tmpAngle,
                    2
                    )
                #┴
            #　└┐（その他）
            #┴　┴
        #　│
        elif self.Type == classEnemy.TYPE_B:
        #　├→（機種が『Ｂ』の場合）
            #○前方に移動する
            self.Y += 1
            #│
            #◇┐左右に移動する
            if self.TimeLife // 30 % 2 == 0:
            #　├→（生存時間が30カウントの場合）
                #│
                #○右に移動する
                self.X += 1.2
                #┴
            #　│
            else:
            #　└┐（その他）
                #○左に移動する
                self.X -= 1.2
            #┴　┴
        #　│
        elif self.Type == classEnemy.TYPE_C:
        #　├→（機種が『Ｃ』の場合）
            #○前方に移動する
            self.Y += 0.8
            #│
            #◇┐弾を発射する
            if self.TimeLife % 40 == 0:
            #　├→（生存時間が40カウントの場合）
                #◎└┐４方向に発射する
                for tmpCnt in range(4):
                    #│＼（4方向の処理を終えた場合）
                    #│ ▼繰り返し処理を抜ける
                    #○当該の方向に弾を発射する
                    classBullet(
                        self.objGame,
                        classBullet.OWNER_ENEMY,
                        self.X, self.Y,
                        tmpCnt * 45 + 22,
                        2
                        )
                #┴　┴
            #　└┐（その他）
            #┴　┴
        #│
        #◇┐敵機を消する
        if self.Y >= pyxel.height:
        #　├→（画面下から出た場合）
            #◇┐敵機を消す
            if self in self.objGame.objEnemie:
            #　├→（敵が存在する場合）
                #○敵機リストから抹消する
                self.objGame.objEnemie.remove(self) 
                #┴
            #　└┐（その他）
            #┴　┴
        #　└┐（その他）
        #┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【非公開】２．描画処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        #◇┐
        if self.Collided:
        #　├→（ダメージ有無が『あり』の場合）
            #○ダメージ有無を『なし』にする
            self.Collided = False
            #│
            #◎└┐
            for tmpCnt in range(1, 15):
                #│＼（15回処理を終えた場合）
                #│ ▼繰り返し処理を抜ける
                #│
                #○
                pyxel.pal(tmpCnt, 15)
                #┴
            #│
            #○
            pyxel.blt(
                self.X, self.Y,
                0, self.Type * 8 + 8, 0,
                8, 8,
                0
                )
            #│
            #○
            pyxel.pal()
            #┴
        #　│
        else:
        #　└┐（その他）
            #○
            pyxel.blt(
                self.X, self.Y,
                0, self.Type * 8 + 8, 0,
                8, 8,
                0
                )
        #┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【公　型】被弾を処理する
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def Sub_Collision(self):
		#┬
        #◇┐
        if self.Armor > 0:
        #　├→（防御力が残っている場合）
            #○防御力を減らす
            #○ダメージ有無を『あり』にする
            #○被弾音を鳴らす
            self.Armor      -= 1
            self.Collided = True
            pyxel.play(2, 1, resume=True)
            #┴
        #　│
        else:
        #　└┐（その他）
            #●爆発エフェクトを生成する
            #○爆発音を鳴らす
            #○スコアを加算する
            classCrush(self.objGame, self.X + 4, self.Y + 4)
            pyxel.play(2, 2, resume=True) 
            self.objGame.Score += self.Level * 10
            #│
            #◇┐敵機を消す
            if self in self.objGame.objEnemie:
            #　├→（敵機リストに存在する場合）
                #○敵機リストから抹消する
                self.objGame.objEnemie.remove(self)
                #┴
            #　└┐（その他）
        #┴　┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【公　型】発射角を得る
    #┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #┃【戻り値】① 小数型：角度
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def Fun_Angle(self):
		#┬
        #○自機を参照する
        tmpObj = self.objGame.objPlayer
        #│
        #◇┐角度を求める
        if tmpObj is None: 
        #　├→（自機が存在しない場合）
            #▼90度を返す
            return 90
        #　│
        else:
		#　└┐（その他）
            #▼自機の方角を返す
            return pyxel.atan2(tmpObj.Y - self.Y, tmpObj.X - self.X)
        #┴
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅴ.弾クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class classBullet:
    #┬
    #□所有者(自機)
    #□所有者(敵機)
    OWNER_PLAYER = 0
    OWNER_ENEMY  = 1 
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【公　開】０．初期化処理
    #┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #┃【引き数】① OBJ型 ：生成先のオブジェクト
    #┃　　　　　② 整数型：所有者
    #┃　　　　　③ 整数型：Ｘ座標
    #┃　　　　　④ 整数型：Ｙ座標
    #┃　　　　　⑤ 小数型：発射角度
    #┃　　　　　⑥ 整数型：移動速度
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(
        self,
        argGame,    #① 生成先のオブジェクト
        argOwner,   #② 所有者
        argX,       #③ Ｘ座標
        argY,       #④ Ｙ座標
        argAngle,   #⑤ 発射角度
        argSpeed    #⑥ 移動速度
        ):
		#┬
        #○引数を退避する
        self.objGame    = argGame
        self.Owner      = argOwner
        self.X          = argX
        self.Y          = argY
        #│
        #○└┐基本データを初期化する
            #○Ｘ軸のベクトル
            #○Ｙ軸のベクトル
        self.VectorX    = pyxel.cos(argAngle) * argSpeed
        self.VectorY    = pyxel.sin(argAngle) * argSpeed
            #┴
        #│
        #◇┐弾を増やす
        if self.Owner == classBullet.OWNER_PLAYER:
        #　├→（弾の所有者が『自機』の場合）
            #○当たり判定の領域をセットする
            #〇弾(自機)リストに追加する
            self.HitArea = (2, 1, 5, 6)
            self.objGame.objBullet_Player.append(self)
            #┴
        #│
        else:
        #　└┐（その他）
            #○当たり判定の領域をセットする
            #〇弾(敵機)リストに追加する
            self.HitArea = (2, 2, 5, 5)
            self.objGame.objBullet_Enemy.append(self)
        #┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【非公開】１．更新処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #○座標を更新する
        self.X += self.VectorX
        self.Y += self.VectorY
        #│
        #◇┐弾を消す
        if (
            self.X <= -8 or self.X >= pyxel.width   or
            self.Y <= -8 or self.Y >= pyxel.height
        ):
        #　├→（座標が画面表示外の場合）
            #◇┐弾を消す
            if self.Owner == classBullet.OWNER_PLAYER:
            #　├→（所有者が『自機』の場合）
                #○弾(自機)リストから抹消する
                self.objGame.objBullet_Player.remove(self)
                #┴
            #│
            else:
            #　└┐（その他）
                #○弾(敵機)リストから抹消する
                self.objGame.objBullet_Enemy.remove(self)
        #┴　┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【非公開】３．描画
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        #○弾を表示する
        tmpSrcX = 0 if self.Owner == classBullet.OWNER_PLAYER else 8
        pyxel.blt(self.X, self.Y, 0, tmpSrcX, 8, 8, 8, 0)
        #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【公　型】命中を処理する
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def Sub_Collision(self):
		#┬
        #◇┐弾を消す
        if self.Owner == classBullet.OWNER_PLAYER:
        #　├→（所有者が『自機』の場合）
            #◇┐弾(自機)リストから魔性する
            if self in self.objGame.objBullet_Player:
            #　├→（弾(自機)リストに存在する場合）
                #○弾(自機)リストから抹消する
                self.objGame.objBullet_Player.remove(self)
                #┴
            #　└┐（その他）
            #┴　┴
        #　│
        elif self in self.objGame.objBullet_Enemy:
        #　├→（弾(敵機)リストに存在する時場合）
            #○弾(敵機)リストから削除する
            self.objGame.objBullet_Enemy.remove(self)
            #┴
        #　└┐（その他）
        #┴　┴
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅵ.爆発クラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class classCrush:
    #┬
    #□開始時の半径
    #□終了時の半径
    START_RADIUS    = 1
    END_RADIUS      = 8 
    #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【公　開】０．初期化処理
    #┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #┃【引き数】① OBJ型 ：生成先のオブジェクト
    #┃　　　　　② 整数型：Ｘ座標
    #┃　　　　　③ 整数型：Ｙ座標
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(
        self,
        atgGame,    #① 生成先のオブジェクト
        argX,       #② Ｘ座標
        argY        #③ Ｙ座標
        ):
		#┬
        #○引数を退避する
        self.objGame    = atgGame
        self.X          = argX
        self.Y          = argY
        #│
        #○基本データ(半径)を初期化する
        self.Radius     = classCrush.START_RADIUS
        #│
        #〇爆発リストに追加する
        self.objGame.objCrush.append(self)
        #┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【非公開】１．更新処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update(self):
		#┬
        #○半径を1ドット大きくする
        self.Radius += 1
        if self.Radius > classCrush.END_RADIUS:
        #　 ＼（半径が最大になった場合）
            #○爆発リストから抹消する
            self.objGame.objCrush.remove(self)
        #┴　┴
	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃【非公開】２．描画処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def draw(self):
		#┬
        #○爆発を描画する
        pyxel.circ (self.X, self.Y, self.Radius,  7)
        pyxel.circb(self.X, self.Y, self.Radius, 10)
        #┴
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃【公　型】衝突の有無を得る
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃【引き数】① OBJ型 ：対象物（1つ目）
#┃　　　　　② OBJ型 ：対象物（2つ目）
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃【戻り値】① 論理型：衝突あり：True／衝突なし：False
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def Fun_Collision(
    argObj1,    #① 対象物１
    argObj2     #② 対象物２
    ):
    #┬
    #○対象物１の座標範囲を求める
    tmpObj1_X1 = argObj1.X + argObj1.HitArea[0]
    tmpObj1_Y1 = argObj1.Y + argObj1.HitArea[1]
    tmpObj1_X2 = argObj1.X + argObj1.HitArea[2]
    tmpObj1_Y2 = argObj1.Y + argObj1.HitArea[3]
    #│
    #○対象物２の座標範囲を求める
    tmpObj2_x1 = argObj2.X + argObj2.HitArea[0]
    tmpObj2_y1 = argObj2.Y + argObj2.HitArea[1]
    tmpObj2_x2 = argObj2.X + argObj2.HitArea[2]
    tmpObj2_y2 = argObj2.Y + argObj2.HitArea[3]
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
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅶ.メイン処理
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┬
#●ゲームのクラスを実行する
Game()
#┴