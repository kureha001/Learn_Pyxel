#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃技術評論社 ゲームで学ぶPython！ CHAPTER6:MAGA WING
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel

from シーン         import classタイトル, classプレイ, class終了
from 演出	        import class背景
from .更新1_移動    import class移動処理
from .更新2_除外    import class除外処理
from .更新3_発射    import class発射処理
from .更新4_衝突    import class衝突処理
from .更新5_出現    import class出現処理

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅱ．ゲームクラス
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class classGame:

    #┬
    #□└┐所有者
        #□なし
        #□自機
        #□敵機
    定数_所有者_なし    = 0
    定数_所有者_自機    = 1
    定数_所有者_標的    = 2 
    #┴　┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃０．初期化処理 
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(self):
		#┬
        #□└┐制御データ
            #□シーン
            #□難易度
            #□プレイ時間
            #□スコア
        self.シーン     = None
        self.難易度     = 0
        self.プレイ時間 = 0
        self.得点       = 0
            #┴
        #│
        #□└┐インスタンス
            #□自機
            #□標的
            #□弾(自機)
            #□弾(敵機)
            #□爆発
        self.obj自機        = None
        self.obj標的        = []
        self.obj弾_自機     = [] 
        self.obj弾_標的     = [] 
        self.obj爆発        = [] 
		#┴　┴

		#┬
        #○Pyxelを初期化する
        self.初期化_リソース()
        #│
        #○背景をオブジェクト化する
        self.F背景 = class背景(self)
        #│
        #○更新処理のリストを作る
        self.FN更新処理 = (
                class移動処理(self),
                class除外処理(self),
                class発射処理(self),
                class衝突処理(self),
                class出現処理(self) )
        #│
        #○描画処理のリストを作る
        self.FN描画処理 = (
                self.obj標的,
                self.obj弾_自機,
                self.obj弾_標的,
                self.obj爆発 )
        #│
        #●シーンの処理ををオブジェクト化する
        self.Fシーン = {
                classタイトル.定数_シーン   : classタイトル(self),
                classプレイ.定数_シーン     : classプレイ(self),
                class終了.定数_シーン       : class終了(self) }
            #┴
        #│
        #●シーンを切替える(タイトル)
        self.Fシーン[class終了.定数_シーン].Fn切替()
        #│
        #○ゲームの実行を開始する
        pyxel.run(self.更新処理,self.描画処理)
		#┴　┴
	#────────────────────────────────────	
    def 初期化_リソース(self):
		#┬
		#○画面を初期化する
		#○リソースファイルを読み込む
        pyxel.init(120, 160, title="Mega Wing  Ver.2025/05/03-02")
        pyxel.load("../リソース/mega_wing.pyxres")
		#│
		#○Soundデータを登録する
        pyxel.sounds[50].mml(
                "t100 @1 o2 q7 v7 l4" +
                "l8d4a4g2.fed4c<b->c<a>e4d1.a4>" +
                "c4<b2.gfe4fga1&a1d4a4g2.fed4c<b->c<a>e4d1." )
        pyxel.sounds[51].mml(
                "t100 @0 o1 q7 v4 l2" +
                "l8dafadbgbd>c<a>c<db-fb-e>c<a>c" +
                "<daf+adaf+agb-a>c" +
                "<dafadbgbdbgbdb-g+b-c" +
                "+aeadaeac+aea<b>ac+adafadbgbd>c" +
                "<a>c<db-fb-e>c<a>c<daf+adaf+adaf+a" )
		#│
		#○Musicデータを登録する
        pyxel.musics[7].set([50],[51])
		#┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃１．更新処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def 更新処理(self):
		#┬
        #●背景を更新する
        self.F背景.移動処理()
        #│
        #◎└┐キャラクターを更新する
        for tmp処理 in self.FN更新処理: tmp処理.実行()
			#│＼（すべての処理を終えた場合）
            #│ ↓
			#│ ▼繰り返し処理を抜ける
			#│
            #●キャラクターを更新する
            #┴ 
        #│
        #●シーンを更新する
        self.Fシーン[self.シーン].更新処理()
		#┴ 	┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃２．描画処理
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def 描画処理(self):
		#┬
        #○画面をクリアする
        pyxel.cls(0)
        #│
        #●背景を描画する
        self.F背景.描画処理()
        #│
        #◇┐自機を描画する
        if self.obj自機 is not None: self.obj自機.描画処理()
        #　├┐（自機が存在する場合）
            #↓
            #●自機を描画する
			#┴
		#　└┐（その他）
			#┴
        #│
        #◎└┐自機以外のキャラクタを描画する
        for tmp処理 in self.FN描画処理: self.Fn描画処理(tmp処理)
			#│＼（すべての処理を終えた場合）
            #│ ↓
			#│ ▼繰り返し処理を抜ける
			#│
            #●キャラクタを描画する
            #┴ 
        #│
        #〇└┐ゲーム情報を描画する
            #〇得点を描画する
            #〇難易度を描画する
        pyxel.text( 5, 2, f"SCORE:{self.得点}", 7)
        pyxel.text(85, 2, f"LEVEL:{self.難易度}", 7)
            #┴
        #│
        #●シーンを描画する
        self.Fシーン[self.シーン].描画処理()
        #┴　┴
	#────────────────────────────────────	
    def Fn描画処理(self,
        argオブジェクト):   #① リスト・オブジェクト
        
		#┬
        #◎└┐オブジェクトのすべてのキャラクタを描画する
        for tmpObj in argオブジェクト:
			#│＼（すべての処理を終えた場合）
            #│ ↓
			#│ ▼繰り返し処理を抜ける
            #│
            #●ひとつずつ描画する
            tmpObj.描画処理()
        #┴　┴