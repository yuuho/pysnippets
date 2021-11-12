
from pathlib import Path
import subprocess
import tempfile
import os

# subprocess.run    : subprocess.{call, check_call, check_output} のまとめ、コマンド終了を待つ
# subprocess.popen  : コマンド終了を待たない。 subprocess.run の基底
# 基本的には run でやっていくのがいい

# ■ 基本:
#   普通のコマンドは error (= exit code 1) でなくても stderr や stdout の両方に何か出力したりする。
#   つまり、 exit status によらず stdout にも stderr にも何か出力できる

# subprocess.run
#   - check : コマンドが失敗したときに CalledProcessError を返す
#               これを使わずとも、戻り値の .returncode で判別できる
#   - timeout : タイムアウト時間
#   - env : 環境変数の指定？
#   - encoding : python3.6以降、これに 'utf8' を指定しておくと

#   戻り値:
#       - returncode
#       - stdout
#       - stderr


# bash とか使いつつ
# subporcess.PIPE を stdin, stdout に指定すると timeout が機能しなくなるエラーがある。
# 3.9 では直ってた
# 3.7.3 だとバグっている
# 3.8 でも直っている
# 3.6 以降なら

# パイプできないコマンド
def basic_command( command ):
    result = subprocess.run( command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode()


def basic_command_env( command, env ):
    result = subprocess.run( command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    return result.stdout.decode()


# コマンドがエラーにならない、必ず終了する前提
def bash_command( command ):
    with tempfile.NamedTemporaryFile('w') as f:
        Path(f.name).write_text(command)
        result = subprocess.run( ['bash',f.name],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,check=True)
        return result.stdout.decode()

# コマンドがエラーでも構わない、stdout も stderr も出力する
def bash_command_except( command ):
    try:
        with tempfile.NamedTemporaryFile('w') as f:
            Path(f.name).write_text(command)
            result = subprocess.run( ['bash',f.name],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,check=True)
            return 0, result.stdout.decode(), result.stderr.decode()
    # コマンドが失敗したとき
    except subprocess.CalledProcessError as e:
        return 1, e.stdout.decode(), e.stderr.decode()


def bash_command_env( command, env ):
    try:
        with tempfile.NamedTemporaryFile('w') as f:
            Path(f.name).write_text(command)
            result = subprocess.run( ['bash',f.name],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,check=True,env=env,encoding='utf8')
            return result.stdout#.decode()
    # コマンドが失敗したとき
    except subprocess.CalledProcessError as e:
        return e.stderr#.decode()



def bash_command_timeoutable( command, limit ):

    print(limit)
    try:
        with tempfile.NamedTemporaryFile('w') as f:
            Path(f.name).write_text(command)
            result = subprocess.run( ['bash',f.name],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,check=True,timeout=limit)
        return result.stdout.decode()
    # コマンドが失敗したとき
    except subprocess.CalledProcessError as e:
        return e.stderr.decode()
    # コマンドが終了しないとき
    except subprocess.TimeoutExpired as e:
        print(e.stdout)
        return -1, "", ""


def basic_command_timeoutable( command, limit ):
    try:
        result = subprocess.run( command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=limit)
        return result.stdout.decode()
    except subprocess.TimeoutExpired as e:
        print(e.stdout)
        return -1, "", ""
    

# 全対応、シングルプロセスならこれが正解
def bash_command_x( command, timelimit=10, env=None ):
    try:
        with tempfile.NamedTemporaryFile('w') as f:
            Path(f.name).write_text(command)
            result = subprocess.run( ['bash',f.name],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        timeout=timelimit, encoding='utf8', env=env)
        return ( False, result.returncode, result.stdout, result.stderr )
    # コマンドが終了しないとき
    except subprocess.TimeoutExpired as e:
        return ( True, 1, "", "" )


def main():

    print('##### command 0 #####')
    command = 'ls -la'
    try:
        print('■ SUCCESS: %s\n'%command, basic_command(command) )
    except:
        print('■ ERROR: %s\n'%command, 'これは成功するはず\n')
    

    print('##### command 1 #####')
    command = 'ls -la | cat'
    try:
        print('■ SUCCESS: %s\n'%command, basic_command(command) )
    except:
        print('■ ERROR: %s\n'%command, 'パイプみたいなことはできない\n')


    print('##### command 2 #####')
    command = 'bash -c "ls -la"'
    try:
        print('■ SUCCESS: %s\n'%command, basic_command(command) )
    except:
        print('■ ERROR: %s\n'%command, '空白のあるコマンドもできない\n')


    print('##### command 3 #####')
    command = 'ls -la | cat'
    try:
        print('■ SUCCESS: %s\n'%command, bash_command(command) )
    except:
        print('■ ERROR: %s\n'%command, 'これは成功するはず\n')
    

    print('##### command 4 #####')
    command = 'ls -la /hoge'
    try:
        print('■ SUCCESS: %s\n'%command, bash_command(command) )
    except:
        print('■ ERROR: %s\n'%command, 'わざとエラーしてみる\n')
    

    print('##### command 5 #####')
    command = 'ls -la /'
    try:
        print('■ SUCCESS: %s\n'%command, bash_command_except(command) )
    except:
        print('■ ERROR: %s\n'%command, 'エラーにならない\n')
    

    print('##### command 6 #####')
    command = 'ls -la /hoge'
    try:
        print('■ SUCCESS: %s\n'%command, bash_command_except(command) )
    except:
        print('■ ERROR: %s\n'%command, 'エラーにならない\n')
    

    print('##### command 7 #####')
    command = 'echo $HOGE'
    d = dict(os.environ)
    d.update({'HOGE':'fuga'})
    try:
        print('■ SUCCESS: %s\n'%command, bash_command_env(command, d ) )
    except:
        print('■ ERROR: %s\n'%command, 'エラーにならない\n')
    

    print('##### command 8 #####')
    command = 'echo $HOGE'
    d = dict(os.environ)
    d.update({'HOGE':'fuga'})
    try:
        # これはうまくいかない シェルじゃないから？
        print('■ SUCCESS: %s\n'%command, basic_command_env(command, d ) )
    except:
        print('■ ERROR: %s\n'%command, 'エラーにならない\n')


    print('##### command 9 #####')
    command = 'python sample2.py'
    try:
        print('■ SUCCESS: %s\n'%command, bash_command_timeoutable(command, 2 ) )
    except:
        print('■ ERROR: %s\n'%command, 'エラーにならない\n')


    print('##### command 10 #####')
    command = 'python sample2.py'
    try:
        print('■ SUCCESS: %s\n'%command, basic_command_timeoutable(command, 2 ) )
    except:
        print('■ ERROR: %s\n'%command, 'エラーにならない\n')


    print('done.')


if __name__=='__main__': main()
