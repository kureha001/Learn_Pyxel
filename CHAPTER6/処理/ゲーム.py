#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃技術評論社 ゲームで学ぶPython！ CHAPTER6:MAGA WING
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃Ⅰ.インポート
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import pyxel
from 演出		import class背景
from .更新      import class更新処理
from .シーン    import classシーン処理
from .描画      import class描画処理

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
    定数_所有者_敵機    = 2 
    #┴　┴

	#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	#┃０．初期化処理 
	#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def __init__(self):
		#┬
        #□└┐制御データ
            #□スコア
            #□シーン
        self.得点       = 0
        self.シーン     = None
            #┴
        #│
        #□└┐インスタンス
            #□自機
            #□敵機
            #□アイテム
        self.obj自機        = None
        self.obj敵機        = []
        self.objアイテム    = [] 
            #│
            #□弾(自機)
            #□弾(敵機)
        self.obj弾_自機     = [] 
        self.obj弾_敵機     = [] 
            #│
            #□爆発
        self.obj爆発        = [] 
            #┴
        #│
        #□└┐制御データ
            #□プレイ時間
            #□難易度
        self.プレイ時間 = 0
        self.難易度     = 0
		#┴　┴

		#┬
        #○Pyxelを初期化する
        self.初期化_リソース()
        #│
        #○└┐オブジェクト化する
            #●背景をオブジェクト化する
            #●更新処理をオブジェクト化する
            #●描画処理をオブジェクト化する
        self.obj背景    = class背景(self)
        self.F更新      = class更新処理(self)
        self.Fシーン    = classシーン処理(self)
        self.F描画      = class描画処理(self)
            #┴
        #│
        #●シーンを切替える(タイトル)
        self.Fシーン.Fn切替_タイトル()
        #│
        #○ゲームの実行を開始する
        pyxel.run(self.F更新.実行,self.F描画.実行)
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