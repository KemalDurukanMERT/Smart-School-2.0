@echo off
REM Generated by trunk tool 'black'
set HOME=%HOME%
if not defined HOME set HOME=
set VIRTUAL_ENV=C:\Users\laptop\AppData\Local\trunk\tools\black\23.12.1-b110d5db43a6dc1812c59c9549d25d5f
set PATH=C:\Users\laptop\AppData\Local\trunk\tools\black\23.12.1-b110d5db43a6dc1812c59c9549d25d5f/bin;C:\Users\laptop\AppData\Local\trunk\tools\black\23.12.1-b110d5db43a6dc1812c59c9549d25d5f/Scripts;C:\Users\laptop\AppData\Local\trunk\tools\python\3.10.8-2211cb108575de2785d77a26a1f8d070/bin;C:\Users\laptop\AppData\Local\trunk\tools\python\3.10.8-2211cb108575de2785d77a26a1f8d070;C:\Users\laptop\AppData\Local\trunk\tools\git-bash\2.40.1-da0c3e1526d36e62bf43d06ec46c5052/bin;C:\Users\laptop\AppData\Local\trunk\tools\git-bash\2.40.1-da0c3e1526d36e62bf43d06ec46c5052/usr/bin;%PATH%
set PYTHONUTF8=1

start /w /b black %*
