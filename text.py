import re
from pathlib import Path

'''
文字列を処理する．(正規表現，抜き出し，etc...)

通常pathlibのrglobではフルパス状態でサーチされる(？)

# ファイル名に関して探す．
r'^.*\/[^/]+$'


'''

def findAR(path,pattern):
    allitem = list(path.rglob('*'))
    matchitem = [item for item in allitem
                    if re.search(pattern,str(item))]
    return matchitem


if __name__ == '__main__':
    root_path = Path('hogehoge')

    # png形式のファイルだけ検索
    paths = findAR(root_path,r'^.*\/[^/]+\.png$')
    # png形式のファイルで隠しファイルのもの以外
    paths = findAR(root_path,r'^.*\/[^.][^/]*\.png$')

    # 表示
    [print(str(p)) for p in paths]