import sys

'''
python sample.py 1>/tmp/my_stdout 2>/tmp/my_stderr && echo "exit 0" || echo "exit 1"
cat /tmp/my_stdout
cat /tmp/my_stderr
'''

print('hoge')
print('fuga',file=sys.stderr)


exit(0)
