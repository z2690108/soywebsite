#! usr/bin/python #coding=utf-8
import sys

tone_list     = [['1','C'],['1#','C+'],['2','D'],['2#','D+'],['3','E'],['4','F'],['4#','F+'],['5','G'],['5#','G+'],['6','A'],['6#','A+'],['7','B']]
# 默认音高
default_pitch = 4
# 当前音高
cur_pitch     = default_pitch
# 唱名替换
replace_map   = {'2b':'1#', '3b':'2#', '5b':'4#', '6b' :'5#', '7b':'6#'}

def str2list(in_str):
  in_str = in_str.replace('|', '').replace('\r','').replace('\n', ' ')
  return in_str.split(' ')

# 获取首调和正文
def getToneAndContext(mmn_list):
  if not mmn_list:
    return {}

  tone = mmn_list[0].replace('#', '+')
  for i in xrange(0, len(tone_list)):
    if tone == tone_list[i][1]:
      tone_index = i
      break
    if i == len(tone_list) - 1:
      # 没有匹配的首调
      return {}
  context = mmn_list[1:]

  return {'tone':tone, 'context':context}

# 获取唱名对应音名表 tone_map，和唱名对应的音高表 pitch_map
def getToneMapAndPitchMap(tone):
  global tone_list, default_pitch
  tone_index = 0
  for i in xrange(0, len(tone_list)):
    if tone == tone_list[i][1]:
      tone_index = i
      break

  tone_map = {}
  pitch_map = {}
  tmp = tone_index
  for j in xrange(0, len(tone_list)):
    tone_map[tone_list[j][0]] = tone_list[tone_index][1]
    pitch_map[tone_list[j][0]] = default_pitch + (0 if tmp < len(tone_list) else 1)

    tmp = tmp + 1
    tone_index = (tmp) % len(tone_list)    

  tone_map['0'] = 'R'
  pitch_map['0'] = 0

  return {'tone_map':tone_map, 'pitch_map':pitch_map}

# ms2mml制作类
class Ms2mmlMaker:
  def __init__(self, mmn_str):
    mmn_list = str2list(mmn_str)
    tone_context = getToneAndContext(mmn_list)
    if not tone_context:
      print '[ms2mmlMaker]Init Ms2mmlMaker failed.'
      self = {}
      return

    self.tone = tone_context['tone']
    self.context = tone_context['context']

    tonemap_contextmap = getToneMapAndPitchMap(self.tone)
    self.tone_map = tonemap_contextmap['tone_map']
    self.pitch_map = tonemap_contextmap['pitch_map']

  def getTone(self, tone_str):
    global cur_pitch, replace_map;
    is_link, has_dot = False, False

    # 连音符特别处理
    i = tone_str.find('&')
    if i != -1:
      is_link = True
      tone_str = tone_str[0:i]

    t_list = tone_str.split('/')
    t_str = t_list[0] if t_list else ''
    n_str = t_list[1] if len(t_list) == 2 else ''

    add_pitch = 0

    #获取音高
    if t_str.find('+')  > 0:
      add_pitch = t_str.count('+')
    
    if t_str.find('-') > 0:
      add_pitch = -t_str.count('-')

    p_str = t_str.replace('+', '').replace('-', '')

    if p_str.find('.') > 0:
      has_dot = True
      p_str = p_str.replace('.', '')

    # 替换同义唱名
    if replace_map.has_key(p_str):
      p_str = replace_map[p_str]

    if not self.tone_map.has_key(p_str):
      return tone_str
    else:
      roll_str = self.tone_map[p_str]

    tmp_pitch = self.pitch_map[p_str] + add_pitch
    pitch_str = ' O%d' % (tmp_pitch) if tmp_pitch != cur_pitch and p_str != '0' else ''
    cur_pitch = tmp_pitch

    dot_str = '.' if has_dot else ''
    if is_link:
      out_str = '%s %s%s%s&%s%s%s'%(pitch_str, roll_str, n_str, dot_str, roll_str, n_str, dot_str)
    else:
      out_str = '%s %s%s%s'%(pitch_str, roll_str, n_str, dot_str)

    return out_str

  def getMs2mml(self):
    if not hasattr(self, 'context'):
      return ''
    ms2mml_str = ''
    for it in self.context:
      if it != '':
        ms2mml_str = ms2mml_str + self.getTone(it)
    return ms2mml_str

def readFile(file_name):
  print "Reading file....\nFile name: %s." % (file_name)
  
  obj = open(file_name)
  file_str = obj.read()
  obj.close()

  return file_str

def writeFile(file_name, content):
  new_file_name = file_name.split('.')[0] + '.ms2mml'
  print "Generating file....\nFile name: %s." % (new_file_name)
  obj = open(new_file_name, 'w')
  obj.write(content)
  obj.close()

def run(file_name):
  m_ms2mmlMaker = Ms2mmlMaker(readFile(file_name))
  ms2mml_str = m_ms2mmlMaker.getMs2mml()
  writeFile(file_name, ms2mml_str)

if __name__ == "__main__":
  run(sys.argv[1])


