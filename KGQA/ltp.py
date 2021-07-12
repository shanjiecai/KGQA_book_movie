# -*- coding: utf-8 -*-
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import SementicRoleLabeller
from pyltp import NamedEntityRecognizer
from pyltp import Parser
import os
LTP_DATA_DIR = 'D:/python36/ltp_data_v3.4.0'  # ltp模型目录的路径

#分词


def segmentor(sentence):
    segmentor = Segmentor()  # 初始化实例
    segmentor.load(os.path.join(LTP_DATA_DIR, 'cws.model'))  # 加载模型
    words = segmentor.segment(sentence)  # 分词
    #默认可以这样输出
    print ('\t'.join(words))
    # 可以转换成List 输出
    words_list = list(words)
    segmentor.release()  # 释放模型
    return words_list

def posttagger(words):
    postagger = Postagger() # 初始化实例
    postagger.load(os.path.join(LTP_DATA_DIR, 'pos.model'))  # 加载模型
    postags = postagger.postag(words)  # 词性标注
    for word,tag in zip(words,postags):
        print (word+'/'+tag)
    postagger.release()  # 释放模型
    return postags

#分句，也就是将一片文本分割为独立的句子
def sentence_splitter(sentence):
    sents = SentenceSplitter.split(sentence)  # 分句
    print ('\n'.join(sents))


#命名实体识别
def ner(words, postags):
    recognizer = NamedEntityRecognizer() # 初始化实例
    recognizer.load(os.path.join(LTP_DATA_DIR, 'ner.model'))  # 加载模型
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    name_list = []
    for word, ntag in zip(words, netags):
        if ntag == 'S-Nh':  #  识别为人名
            name_list.append(word)
    recognizer.release()  # 释放模型
    return name_list

#依存语义分析
def parse(words, postags):
    parser = Parser() # 初始化实例
    parser.load(os.path.join(LTP_DATA_DIR, 'parser.model'))  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    print ("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
    parser.release()  # 释放模型
    return arcs

#角色标注
def role_label(words, postags, netags, arcs):
    labeller = SementicRoleLabeller() # 初始化实例
    labeller.load(os.path.join(LTP_DATA_DIR, 'srl'))  # 加载模型
    roles = labeller.label(words, postags, netags, arcs)  # 语义角色标注
    for role in roles:
        print (role.index, "".join(["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
    labeller.release()  # 释放模型


def check_name(question):
    #分词
    words = segmentor(question)
    tags = posttagger(words)
    return ner(words,tags)
