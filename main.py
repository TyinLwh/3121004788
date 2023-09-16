import math
import re
import jieba
import sys


# 从指定路径获取文本信息
def get(path):
  file = open(path, 'r', encoding='utf-8')
  message = file.read()
  file.close()
  return message


# 对文本进行分割
def cut(message):
  comp = re.compile('[^A-Z^a-z0-9\u4e00-\u9fa5]')
  words = jieba.lcut(comp.sub('', message), cut_all=False)
  word = [w for w in words if len(w.strip()) > 0]
  return word


# 对各词语出现次数进行统计
def count(text1, text2):
  #合并两个句子的单词
  key_word = list(set(text1 + text2))
  v1 = []
  for i in range(len(key_word)):
      v1.append(0)
      for j in range(len(text1)):
          if key_word[i] == text1[j]:
              v1[i] += 1
              continue
  v2 = []
  for k in range(len(key_word)):
      v2.append(0)
      for m in range(len(text2)):
          if key_word[k] == text2[m]:
              v2[k] += 1
              continue
  return v1, v2


# 计算余弦相似度
def cosin(vec1, vec2):
  add = 0
  squ1 = 0
  squ2 = 0
  for i in range(len(vec1)):
      add += vec1[i] * vec2[i]
      squ1 += vec1[i] ** 2
      squ2 += vec2[i] ** 2
  try:
      cos = (add / ((math.sqrt(squ1)) * (math.sqrt(squ2))))
      return cos
  except ZeroDivisionError:
      print('文本空白。')
      return 0


def main_test(path1, path2, save_path):
  try:
      file1 = get(path1)
      file2 = get(path2)
      cut1 = cut(file1)
      cut2 = cut(file2)
      count1, count2 = count(cut1, cut2)
      result = cosin(count1, count2)
      print(str(path1) + "与" + str(path2) + "的相似度：%.2f%%\n" % (result * 100))
      f = open(save_path, 'a', encoding="utf-8")
      f.write(str(path1) + "与" + str(path2) + "的相似度：%.2f%%\n" % (result * 100))
      f.close()
  # 捕捉文件路径错误
  except FileNotFoundError:
      print("抱歉，文件不存在。")

if __name__ == '__main__':
  filepath1 = ''
  filepath2 = ''
  result_save_path = ''
  try:
      # 与命令行参数交互
      filepath1 = sys.argv[1]
      filepath2 = sys.argv[2]
      result_save_path = sys.argv[3]
  except IndexError:
      filepath1 = input("输入原版文件路径:")
      filepath2 = input("输入抄袭版文件路径:")
      result_save_path = input("请输入要保存相似度结果的文件的路径：")
  main_test(filepath1, filepath2, result_save_path)