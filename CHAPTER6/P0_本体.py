#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import time
import pyxel
from P1_背景    import classScreen
from P2_自機    import classPlayer
from P3_敵機    import classEnemy

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
	#┃０．初期化処理 
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
	#┃１．更新処理
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
        #┃1-1.1.弾(自機)を更新
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
        #┃1-1.2.敵機を更新
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
        #┃1-2.1.弾(自機)を更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update_BulletPlayer(self):
		#┬
		#◎└┐弾(自機)を更新する
        for tmpObj in self.objBullet_Player.copy():
			#│＼（すべての弾を処理し終えた）
			#│ ▼繰り返し処理を抜ける
            #●弾(自機)を更新する
            tmpObj.update()
            #│
            #◎└┐すべての敵機との衝突判定を行う
            for tmpObjEnemy in self.objEnemie.copy():
                #│＼（すべての敵機を処理し終えた場合）
                #│ ▼繰り返し処理を抜ける
                #●敵機との衝突を調べる
                if Fun_Collision(tmpObjEnemy, tmpObj):
                #　 ＼（衝突している場合）
                    #●弾(自機)を命中させる
                    #●敵機を被弾させる
                    tmpObj.Sub_Collision()
                    tmpObjEnemy.Sub_Collision() 
        #┴　┴　┴　┴
        #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #┃1-2.2.弾(敵機)を更新
        #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def update_BulletEnemy(self):
		#┬
        #◎└┐すべての弾(敵機)を更新する
        for tmpObj in self.objBullet_Enemy.copy():
            #│＼（すべての弾(敵機)を処理し終えた場合）
            #│ ▼繰り返し処理を抜ける
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
        #┃1-3.1.破壊を更新
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
        #┃1-3.2.更新
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
            #◇┐敵機を追加する
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
    def Sub_Scene(self,
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
            #●敵機を抹消(リスト全体をクリア)する
            #●弾(自分)を抹消(リスト全体をクリア)する
            #●弾(敵機)を抹消(リスト全体をクリア)する
            self.objPlayer = None
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
#┃衝突の有無を得る
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