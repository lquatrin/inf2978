# This Python file uses the following encoding: utf-8
import re

def FormatContent(content, manual_mode = False):
  
  #Concatenate each line and replace '\n' by ' '
  content = ''.join(content).replace('\n',' ').lower()


  # c
  content = re.sub("[ç]"   , 'c', content)  
  # â á à ã
  content = re.sub("[âáàã]", 'a', content)
  # ê é è
  content = re.sub("[êéè]" , 'e', content)
  # î í ì
  content = re.sub("[îíì]" , 'i', content)
  # ô ó ò õ
  content = re.sub("[ôóòõ]", 'o', content)
  # û ú ù
  content = re.sub("[ûúù]" , 'u', content)
  # ñ
  content = re.sub("[ñ]" , 'n', content)
  
  # ? ! ' . - " … : ; , [ ] ( ) { }
  content = re.sub("[\\?\\!\\'\\.\\-\"…:;,\\[\\]\\(\\)\\{\\}/\/]", ' ', content)
  content = re.sub("[\?\!\'\.\-\[\]\(\)\{\}'\']", ' ', content)
  
  # 1 2 3 4 5 6 7 8 9 0
  #content = re.sub("[1234567890]", ' ', content)
  content = re.sub("[1]", '', content)
  content = re.sub("[2]", '', content)
  content = re.sub("[3]", '', content)
  content = re.sub("[4]", '', content)
  content = re.sub("[5]", '', content)
  content = re.sub("[6]", '', content)
  content = re.sub("[7]", '', content)
  content = re.sub("[8]", '', content)
  content = re.sub("[9]", '', content)
  content = re.sub("[0]", '', content)
  
  content = ' '.join(content.split())
  #content = re.sub(' *', ' ', content)

  #trocar ' ' por '`' para facilitar o hash depois
  if manual_mode == True:
    content = re.sub(' ', chr(96), content)

  return content