#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃技術評論社 ゲームで学ぶPython！ CHAPTER6:MAGA WING
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from enum import IntEnum, auto

class ID(IntEnum):
	#┬
	#□シーン
	タイトル				= 100
	プレイ					= 200
	ステージコール	= auto()
	ボーナス				= auto()
	ボス対決				= auto()
	終了						= 300
	#┴