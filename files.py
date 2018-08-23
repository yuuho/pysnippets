import re
import shutil
from pathlib import Path

'''
-----------------------------------------------------
# pathlib.Pathで最初からできること
- Path.exists() : 存在するか
- Path.is_dir() : ディレクトリか
-----------------------------------------------------
# 関数名の後ろについている文字の意味
H : 既に存在する場合上書き
S : 既に存在する場合無視

F : ファイル
D : ディレクトリ
A : ファイルとディレクトリ

R : 再帰的に下層まで
C : 指定したディレクトリのみ
-----------------------------------------------------
# 引数・戻り値の型
引数のpatternは文字列．それ以外はpathlib.Path
戻り値があるもの(find)はpathlib.Pathのlist
-----------------------------------------------------
# 関数の一覧
## ディレクトリを作成する
- mkdirH : path
- mkdirS : path

## ディレクトリ・ファイルに関わらず削除・コピー・移動をする
- rm  : path
- cpH : src, dst
- cpS : src, dst
- mvH : src, dst
- mvS : src, dst

## ディレクトリ・ファイル，または両方を再帰的もしくは指定したディレクトリ内から探す
- findFR : path, pattern
- findFC : path, pattern
- findDR : path, pattern
- findDC : path, pattern
- findAR : path, pattern
- findAC : path, pattern
----------------------------------------------------------
# ルール
それぞれの関数の中では，このファイルで定義されている自分以外の関数を使わない．
----------------------------------------------------------
'''

# ディレクトリの作成(既に存在する場合上書き)
def mkdirH(path):
    # 既に存在していたら消す
    shutil.rmtree(str(path),ignore_errors=True)
    path.mkdir(parents=True)

# ディレクトリの作成(既に存在する場合無視)
def mkdirS(path):
    path.mkdir(parents=True,exist_ok=True)

# ディレクトリやファイルを消す
def rm(path):
    # 消す対象が存在するとき，ディレクトリかファイルか判断して消す
    if path.exists():
        if path.is_dir():
            shutil.rmtree(str(path))
        else:
            path.unlink()

# ファイル・ディレクトリのコピー
#   src:ファイル名, dst:ファイル名
def cpH(src,dst):
    # ディレクトリかファイルかの判定．ディレクトリならツリーで
    if src.is_dir():
        # 既にあるなら消す
        shutil.rmtree(str(dst),ignore_errors=True)
        #ツリーごとコピー
        shutil.copytree(str(src),str(dst))
    else:
        # 既にあるなら消す
        if dst.exists():
            dst.unlink()
        # 途中のパスがそんざいしないなら作る
        dst.parent.mkdir(parents=True,exist_ok=True)
        #ファイルをコピー
        shutil.copy(str(src),str(dst))

# ファイル・ディレクトリのコピー
#   src:ファイル名, dst:ファイル名
def cpS(src,dst):
    # 既にある場合はやめる
    if dst.exists():
        return
    # ディレクトリかファイルかの判定．ディレクトリならツリーで
    if src.is_dir():
        #ツリーごとコピー
        shutil.copytree(str(src),str(dst))
    else:
        # 途中のパスがそんざいしないなら作る
        dst.parent.mkdir(parents=True,exist_ok=True)
        #ファイルをコピー
        shutil.copy(str(src),str(dst))

def mvH(src,dst):
    # 存在するなら消す(ファイルの場合，macなら消さなくても上書きになるがwinはわからない)
    if dst.exists():
        if path.is_dir():
            shutil.rmtree(str(dst))
        else:
            path.unlink()
    shutil.move(str(src),str(dst))

def mvS(src,dst):
    if dst.exists():
        return
    shutil.move(str(src),str(dst))


# 以下，全て条件式がちょっと違うだけ
# ワンライナーで書くならこれが楽かも(正規表現でスラッシュや拡張子の有無を見ればほぼ対応できるので)
# [item for item in list(path.rglob('*')) if re.search(pattern,str(item))]

def findFR(path,pattern):
    allitem = list(path.rglob('*'))
    matchitem = [item for item in allitem
                    if re.search(pattern,str(item)) and not item.is_dir()]
    return matchitem

def findFC(path,pattern):
    allitem = list(path.glob('*'))
    matchitem = [item for item in allitem
                    if re.search(pattern,str(item)) and not item.is_dir()]
    return matchitem

def findDR(path,pattern):
    allitem = list(path.rglob('*'))
    matchitem = [item for item in allitem
                    if re.search(pattern,str(item)) and item.is_dir()]
    return matchitem

def findDC(path,pattern):
    allitem = list(path.glob('*'))
    matchitem = [item for item in allitem
                    if re.search(pattern,str(item)) and item.is_dir()]
    return matchitem

def findAR(path,pattern):
    allitem = list(path.rglob('*'))
    matchitem = [item for item in allitem
                    if re.search(pattern,str(item))]
    return matchitem

def findAC(path,pattern):
    allitem = list(path.glob('*'))
    matchitem = [item for item in allitem
                    if re.search(pattern,str(item))]
    return matchitem
