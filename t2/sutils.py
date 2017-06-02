import re

def FormatContent(content):
  
  #Concatenate each line and replace '\n' by ' '
  content = ''.join(content).replace('\n',' ').lower()

  # ç
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
  
  # ? ! ' . - " … : ; , [ ] ( ) { }
  content = re.sub("[\\?\\!\\'\\.\\-\"…:;,\\[\\]\\(\\)\\{\\}]", ' ', content)
  
  # 1 2 3 4 5 6 7 8 9 0
  #content = re.sub("[1234567890]", ' ', content)
  content = re.sub("[1]", 'um', content)
  content = re.sub("[2]", 'dois', content)
  content = re.sub("[3]", 'tres', content)
  content = re.sub("[4]", 'quatro', content)
  content = re.sub("[5]", 'cinco', content)
  content = re.sub("[6]", 'seis', content)
  content = re.sub("[7]", 'sete', content)
  content = re.sub("[8]", 'oito', content)
  content = re.sub("[9]", 'nove', content)
  content = re.sub("[0]", 'zero', content)
   
  #trocar ' ' por '`' para facilitar o hash depois
  content = re.sub(' ', chr(96), content)

  return content

#links
#https://docs.python.org/release/2.7.2/library/multiprocessing.html
#http://scipy-cookbook.readthedocs.io/items/ParallelProgramming.html
#http://sebastianraschka.com/Articles/2014_multiprocessing.html
#http://www.parallelpython.com/
#https://blog.dominodatalab.com/simple-parallelization/
#http://dispy.sourceforge.net/