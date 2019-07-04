import re
from collections import defaultdict

import jieba
import numpy as np
from jieba import posseg
import datetime
from spa.corpus import WaimaiCorpus
from sklearn.externals import joblib


# ################################################
# classifier based on sentiment f_dict
# ################################################
class DictClassifier:
    def __init__(self):
        self.__root_filepath = "f_dict/"

        jieba.load_userdict("f_dict/user.dict")  # 准备分词词典

        # 准备情感词典词典
        self.__phrase_dict = self.__get_phrase_dict()
        self.__positive_dict = self.__get_dict(self.__root_filepath + "positive_dict.txt")
        self.__negative_dict = self.__get_dict(self.__root_filepath + "negative_dict.txt")
        self.__conjunction_dict = self.__get_dict(self.__root_filepath + "conjunction_dict.txt")
        self.__punctuation_dict = self.__get_dict(self.__root_filepath + "punctuation_dict.txt")
        self.__adverb_dict = self.__get_dict(self.__root_filepath + "adverb_dict.txt")
        self.__denial_dict = self.__get_dict(self.__root_filepath + "denial_dict.txt")

    def classify(self, sentence):
        return self.analyse_sentence(sentence)

    def analysis_file(self, filepath_in, filepath_out, encoding="utf-8", print_show=False, start=0, end=-1):
        open(filepath_out, "w")
        results = []

        with open(filepath_in, "r", encoding=encoding) as f:
            line_number = 0
            for line in f:
                # 控制分析的语料的开始位置（行数）
                line_number += 1
                if line_number < start:
                    continue

                results.append(self.analyse_sentence(line.strip(), filepath_out, print_show))

                # 控制分析的语料的结束位置（行数）
                if 0 < end <= line_number:
                    break

        return results

    def analyse_sentence(self, sentence, runout_filepath=None, print_show=False):
        # 情感分析整体数据结构
        comment_analysis = {"score": 0}

        # 将评论分句
        the_clauses = self.__divide_sentence_into_clauses(sentence + "%")

        # 对每分句进行情感分析
        for i in range(len(the_clauses)):
            # 情感分析子句的数据结构
            sub_clause = self.__analyse_clause(the_clauses[i].replace("。", "."), runout_filepath, print_show)

            # 将子句分析的数据结果添加到整体数据结构中
            comment_analysis["su-clause" + str(i)] = sub_clause
            comment_analysis['score'] += sub_clause['score']

        if runout_filepath is not None:
            # 将整句写进运行输出文件，以便复查
            self.__write_runout_file(runout_filepath, "\n" + sentence + '\n')
            # 将每个评论的每个分句的分析结果写进运行输出文件，以便复查
            self.__output_analysis(comment_analysis, runout_filepath)
            # 将每个评论的的整体分析结果写进运行输出文件，以便复查
            self.__write_runout_file(runout_filepath, str(comment_analysis) + "\n\n\n\n")
        if print_show:
            print("\n" + sentence)
            self.__output_analysis(comment_analysis)
            print(comment_analysis, end="\n\n\n")

        if comment_analysis["score"] > 0:
            return 1
        else:
            return 0

    def __analyse_clause(self, the_clause, runout_filepath, print_show):
        sub_clause = {"score": 0, "positive": [], "negative": [], "conjunction": [], "punctuation": [], "pattern": []}
        seg_result = posseg.lcut(the_clause)

        # 将分句及分词结果写进运行输出文件，以便复查
        if runout_filepath is not None:
            self.__write_runout_file(runout_filepath, the_clause + '\n')
            self.__write_runout_file(runout_filepath, str(seg_result) + '\n')
        if print_show:
            print(the_clause)
            print(seg_result)

        # 判断句式：如果……就好了
        judgement = self.__is_clause_pattern2(the_clause)
        if judgement != "":
            sub_clause["pattern"].append(judgement)
            sub_clause["score"] -= judgement["value"]
            return sub_clause

        # 判断句式：是…不是…
        judgement = self.__is_clause_pattern1(the_clause)
        if judgement != "":
            sub_clause["pattern"].append(judgement)
            sub_clause["score"] -= judgement["value"]

        # 判断句式：短语
        judgement = self.__is_clause_pattern3(the_clause, seg_result)
        if judgement != "":
            sub_clause["score"] += judgement["score"]
            if judgement["score"] >= 0:
                sub_clause["positive"].append(judgement)
            elif judgement["score"] < 0:
                sub_clause["negative"].append(judgement)
            match_result = judgement["key"].split(":")[-1]
            i = 0
            while i < len(seg_result):
                if seg_result[i].word in match_result:
                    if i + 1 == len(seg_result) or seg_result[i + 1].word in match_result:
                        del (seg_result[i])
                        continue
                i += 1

        # 逐个分析分词
        for i in range(len(seg_result)):
            mark, result = self.__analyse_word(seg_result[i].word, seg_result, i)
            if mark == 0:
                continue
            elif mark == 1:
                sub_clause["conjunction"].append(result)
            elif mark == 2:
                sub_clause["punctuation"].append(result)
            elif mark == 3:
                sub_clause["positive"].append(result)
                sub_clause["score"] += result["score"]
            elif mark == 4:
                sub_clause["negative"].append(result)
                sub_clause["score"] -= result["score"]

        # 综合连词的情感值
        for a_conjunction in sub_clause["conjunction"]:
            sub_clause["score"] *= a_conjunction["value"]

        # 综合标点符号的情感值
        for a_punctuation in sub_clause["punctuation"]:
            sub_clause["score"] *= a_punctuation["value"]

        return sub_clause

    @staticmethod
    def __is_clause_pattern2(the_clause):
        # re_pattern = re.compile(r".*(如果|要是|希望).+就[\u4e00-\u9fa5]+(好|完美)了")
        re_pattern = re.compile(r".*(如果|要是|希望).+就[\u4e00-\u9fa5]*(好|完美)了")
        match = re_pattern.match(the_clause)
        if match is not None:
            pattern = {"key": "如果…就好了", "value": 1.0}
            return pattern
        return ""

    def __is_clause_pattern3(self, the_clause, seg_result):
        for a_phrase in self.__phrase_dict:
            keys = a_phrase.keys()
            to_compile = a_phrase["key"].replace("……", "[\u4e00-\u9fa5]*")

            if "start" in keys:
                to_compile = to_compile.replace("*", "{" + a_phrase["start"] + "," + a_phrase["end"] + "}")
            if "head" in keys:
                to_compile = a_phrase["head"] + to_compile

            match = re.compile(to_compile).search(the_clause)
            if match is not None:
                can_continue = True
                pos = [flag for word, flag in posseg.cut(match.group())]
                if "between_tag" in keys:
                    if a_phrase["between_tag"] not in pos and len(pos) > 2:
                        can_continue = False

                if can_continue:
                    for i in range(len(seg_result)):
                        if seg_result[i].word in match.group():
                            try:
                                if seg_result[i + 1].word in match.group():
                                    return self.__emotional_word_analysis(
                                        a_phrase["key"] + ":" + match.group(), a_phrase["value"],
                                        [x for x, y in seg_result], i)
                            except IndexError:
                                return self.__emotional_word_analysis(
                                    a_phrase["key"] + ":" + match.group(), a_phrase["value"],
                                    [x for x, y in seg_result], i)
        return ""

    def __analyse_word(self, the_word, seg_result=None, index=-1):
        # 判断是否是连词
        judgement = self.__is_word_conjunction(the_word)
        if judgement != "":
            return 1, judgement

        # 判断是否是标点符号
        judgement = self.__is_word_punctuation(the_word)
        if judgement != "":
            return 2, judgement

        # 判断是否是正向情感词
        judgement = self.__is_word_positive(the_word, seg_result, index)
        if judgement != "":
            return 3, judgement

        # 判断是否是负向情感词
        judgement = self.__is_word_negative(the_word, seg_result, index)
        if judgement != "":
            return 4, judgement

        return 0, ""

    @staticmethod
    def __is_clause_pattern1(the_clause):
        re_pattern = re.compile(r".*(要|选)的.+(送|给).*")
        match = re_pattern.match(the_clause)
        if match is not None:
            pattern = {"key": "要的是…给的是…", "value": 1}
            return pattern
        return ""

    def __is_word_conjunction(self, the_word):
        if the_word in self.__conjunction_dict:
            conjunction = {"key": the_word, "value": self.__conjunction_dict[the_word]}
            return conjunction
        return ""

    def __is_word_punctuation(self, the_word):
        if the_word in self.__punctuation_dict:
            punctuation = {"key": the_word, "value": self.__punctuation_dict[the_word]}
            return punctuation
        return ""

    def __is_word_positive(self, the_word, seg_result, index):
        # 判断分词是否在情感词典内
        if the_word in self.__positive_dict:
            # 在情感词典内，则构建一个以情感词为中心的字典数据结构
            return self.__emotional_word_analysis(the_word, self.__positive_dict[the_word],
                                                  [x for x, y in seg_result], index)
        # 不在情感词典内，则返回空
        return ""

    def __is_word_negative(self, the_word, seg_result, index):
        # 判断分词是否在情感词典内
        if the_word in self.__negative_dict:
            # 在情感词典内，则构建一个以情感词为中心的字典数据结构
            return self.__emotional_word_analysis(the_word, self.__negative_dict[the_word],
                                                  [x for x, y in seg_result], index)
        # 不在情感词典内，则返回空
        return ""

    def __emotional_word_analysis(self, core_word, value, segments, index):
        # 在情感词典内，则构建一个以情感词为中心的字典数据结构
        orientation = {"key": core_word, "adverb": [], "denial": [], "value": value}
        orientation_score = orientation["value"]  # my_sentiment_dict[segment]

        # 在三个前视窗内，判断是否有否定词、副词
        view_window = index - 1
        if view_window > -1:  # 无越界
            # 判断前一个词是否是情感词
            if segments[view_window] in self.__negative_dict or \
                            segments[view_window] in self.__positive_dict:
                orientation['score'] = orientation_score
                return orientation
            # 判断是否是副词
            if segments[view_window] in self.__adverb_dict:
                # 构建副词字典数据结构
                adverb = {"key": segments[view_window], "position": 1,
                          "value": self.__adverb_dict[segments[view_window]]}
                orientation["adverb"].append(adverb)
                orientation_score *= self.__adverb_dict[segments[view_window]]
            # 判断是否是否定词
            elif segments[view_window] in self.__denial_dict:
                # 构建否定词字典数据结构
                denial = {"key": segments[view_window], "position": 1,
                          "value": self.__denial_dict[segments[view_window]]}
                orientation["denial"].append(denial)
                orientation_score *= -1
        view_window = index - 2
        if view_window > -1:
            # 判断前一个词是否是情感词
            if segments[view_window] in self.__negative_dict or \
                            segments[view_window] in self.__positive_dict:
                orientation['score'] = orientation_score
                return orientation
            if segments[view_window] in self.__adverb_dict:
                adverb = {"key": segments[view_window], "position": 2,
                          "value": self.__adverb_dict[segments[view_window]]}
                orientation_score *= self.__adverb_dict[segments[view_window]]
                orientation["adverb"].insert(0, adverb)
            elif segments[view_window] in self.__denial_dict:
                denial = {"key": segments[view_window], "position": 2,
                          "value": self.__denial_dict[segments[view_window]]}
                orientation["denial"].insert(0, denial)
                orientation_score *= -1
                # 判断是否是“不是很好”的结构（区别于“很不好”）
                if len(orientation["adverb"]) > 0:
                    # 是，则引入调节阈值，0.3
                    orientation_score *= 0.3
        view_window = index - 3
        if view_window > -1:
            # 判断前一个词是否是情感词
            if segments[view_window] in self.__negative_dict or segments[view_window] in self.__positive_dict:
                orientation['score'] = orientation_score
                return orientation
            if segments[view_window] in self.__adverb_dict:
                adverb = {"key": segments[view_window], "position": 3,
                          "value": self.__adverb_dict[segments[view_window]]}
                orientation_score *= self.__adverb_dict[segments[view_window]]
                orientation["adverb"].insert(0, adverb)
            elif segments[view_window] in self.__denial_dict:
                denial = {"key": segments[view_window], "position": 3,
                          "value": self.__denial_dict[segments[view_window]]}
                orientation["denial"].insert(0, denial)
                orientation_score *= -1
                # 判断是否是“不是很好”的结构（区别于“很不好”）
                if len(orientation["adverb"]) > 0 and len(orientation["denial"]) == 0:
                    orientation_score *= 0.3
        # 添加情感分析值。
        orientation['score'] = orientation_score
        # 返回的数据结构
        return orientation

    # 输出comment_analysis分析的数据结构结果
    def __output_analysis(self, comment_analysis, runout_filepath=None):
        output = "Score:" + str(comment_analysis["score"]) + "\n"

        for i in range(len(comment_analysis) - 1):
            output += "Sub-clause" + str(i) + ": "
            clause = comment_analysis["su-clause" + str(i)]
            if len(clause["conjunction"]) > 0:
                output += "conjunction:"
                for punctuation in clause["conjunction"]:
                    output += punctuation["key"] + " "
            if len(clause["positive"]) > 0:
                output += "positive:"
                for positive in clause["positive"]:
                    if len(positive["denial"]) > 0:
                        for denial in positive["denial"]:
                            output += denial["key"] + str(denial["position"]) + "-"
                    if len(positive["adverb"]) > 0:
                        for adverb in positive["adverb"]:
                            output += adverb["key"] + str(adverb["position"]) + "-"
                    output += positive["key"] + " "
            if len(clause["negative"]) > 0:
                output += "negative:"
                for negative in clause["negative"]:
                    if len(negative["denial"]) > 0:
                        for denial in negative["denial"]:
                            output += denial["key"] + str(denial["position"]) + "-"
                    if len(negative["adverb"]) > 0:
                        for adverb in negative["adverb"]:
                            output += adverb["key"] + str(adverb["position"]) + "-"
                    output += negative["key"] + " "
            if len(clause["punctuation"]) > 0:
                output += "punctuation:"
                for punctuation in clause["punctuation"]:
                    output += punctuation["key"] + " "
            if len(clause["pattern"]) > 0:
                output += "pattern:"
                for pattern in clause["pattern"]:
                    output += pattern["key"] + " "
            # if clause["pattern"] is not None:
            #     output += "pattern:" + clause["pattern"]["key"] + " "
            output += "\n"
        if runout_filepath is not None:
            self.__write_runout_file(runout_filepath, output)
        else:
            print(output)

    def __divide_sentence_into_clauses(self, the_sentence):
        #拆成单独的小句子
        the_clauses = self.__split_sentence(the_sentence)

        # 识别“是……不是……”句式
        pattern = re.compile(r"([，、。%！；？?,!～~.… ]*)([\u4e00-\u9fa5]*?(要|选)"
                             r"的.+(送|给)[\u4e00-\u9fa5]+?[，。！%；、？?,!～~.… ]+)")
        match = re.search(pattern, the_sentence.strip())

        if match is not None and len(self.__split_sentence(match.group(2))) <= 2:
            to_delete = []
            for i in range(len(the_clauses)):
                if the_clauses[i] in match.group(2):
                    to_delete.append(i)
            if len(to_delete) > 0:
                for i in range(len(to_delete)):
                    the_clauses.remove(the_clauses[to_delete[0]])
                the_clauses.insert(to_delete[0], match.group(2))

        # 识别“要是|如果……就好了”的假设句式
        pattern = re.compile(r"([，%。、！；？?,!～~.… ]*)([\u4e00-\u9fa5]*?(如果|要是|"
                             r"希望).+就[\u4e00-\u9fa5]+(好|完美)了[，。；！%、？?,!～~.… ]+)")
        match = re.search(pattern, the_sentence.strip())
        if match is not None and len(self.__split_sentence(match.group(2))) <= 3:
            to_delete = []
            for i in range(len(the_clauses)):
                if the_clauses[i] in match.group(2):
                    to_delete.append(i)
            if len(to_delete) > 0:
                for i in range(len(to_delete)):
                    the_clauses.remove(the_clauses[to_delete[0]])
                the_clauses.insert(to_delete[0], match.group(2))

        the_clauses[-1] = the_clauses[-1][:-1]
        return the_clauses

    @staticmethod
    def __split_sentence(sentence):
        pattern = re.compile("[，。%、！!？?,；～~.… ]+")

        split_clauses = pattern.split(sentence.strip())
        punctuations = pattern.findall(sentence.strip())
        try:
            split_clauses.remove("")
        except ValueError:
            pass
        punctuations.append("")

        clauses = [''.join(x) for x in zip(split_clauses, punctuations)]

        return clauses

    def __get_phrase_dict(self):
        sentiment_dict = []
        pattern = re.compile(r"\s+")
        with open(self.__root_filepath + "phrase_dict.txt", "r", encoding="utf-8") as f:
            for line in f:
                a_phrase = {}
                result = pattern.split(line.strip())
                if len(result) >= 2:
                    a_phrase["key"] = result[0]
                    a_phrase["value"] = float(result[1])
                    for i, a_split in enumerate(result):
                        if i < 2:
                            continue
                        else:
                            a, b = a_split.split(":")
                            a_phrase[a] = b
                    sentiment_dict.append(a_phrase)

        return sentiment_dict

    # 情感词典的构建
    @staticmethod
    def __get_dict(path, encoding="utf-8"):
        sentiment_dict = {}
        pattern = re.compile(r"\s+")
        with open(path, encoding=encoding) as f:
            for line in f:
                result = pattern.split(line.strip())
                if len(result) == 2:
                    sentiment_dict[result[0]] = float(result[1])
        return sentiment_dict

    @staticmethod
    def __write_runout_file(path, info, encoding="utf-8"):
        with open(path, "a", encoding=encoding) as f:
            f.write("%s" % info)


# ################################################
# classifier based on Support Vector Machine
# ################################################
from sklearn.svm import SVC


class SVMClassifier:
    def __init__(self, train_data, train_labels, best_words, C):
        train_data = np.array(train_data)
        train_labels = np.array(train_labels)

        self.best_words = best_words
        self.clf = SVC(C=C)
        self.__train(train_data, train_labels)

    def words2vector(self, all_data):
        vectors = []

        best_words_index = {}
        for i, word in enumerate(self.best_words):
            best_words_index[word] = i

        for data in all_data:
            vector = [0 for x in range(len(self.best_words))]
            for word in data:
                i = best_words_index.get(word)
                if i is not None:
                    vector[i] = vector[i] + 1
            vectors.append(vector)

        vectors = np.array(vectors)
        return vectors

    def __train(self, train_data, train_labels):
        print("SVMClassifier is training ...... ")

        train_vectors = self.words2vector(train_data)

        self.clf.fit(train_vectors, np.array(train_labels))

        #save model
        joblib.dump(self,'../saved_model/waimai.pkl')

        print("SVMClassifier trains over!")




    def classify(self, data):
        vector = self.words2vector([data])

        prediction = self.clf.predict(vector)

        return prediction[0]


    '''效率测试'''
    def test_svm(self):
        print("SVMClassifier")
        print("---" * 45)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)
        print("C = %s" % self.C)

        from spa.classifiers import SVMClassifier
        svm = SVMClassifier(self.train_data, self.train_labels, self.best_words, self.C)

        classify_labels = []
        print("SVMClassifier is testing ...")
        for data in self.test_data:
            classify_labels.append(svm.classify(data))
        print("SVMClassifier tests over.")

        filepath = "f_runout/SVM-%s-train-%d-test-%d-f-%d-C-%d-%s-lin.xls" % \
                   (self.type,
                    self.train_num, self.test_num,
                    self.feature_num, self.C,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        self.write(filepath, classify_labels, 2)


if __name__=='__main__':
    '''利用情感词典的情感极性分析'''

    '''单个句子'''
    d = DictClassifier()
    a_sentence = "剁椒鸡蛋好咸,土豆丝不好吃"
    result = d.analyse_sentence(a_sentence,runout_filepath="hyoupannokeka.txt",print_show=True)
    #print(result)

    '''文件分析'''
    # d=DictClassifier()
    # d.analysis_file(f
    # ilepath_in="../hyoupan.txt",filepath_out="../hyoupannokeka.txt")

    '''利用svm进行分析'''

    '''训练模型'''
    # type_ = "waimai"
    # train_num = 3000
    # test_num = 1000
    # feature_num = 5000
    # max_iter = 500
    # C = 150
    # k = 13
    # k = [1, 3, 5, 7, 9, 11, 13]
    # corpus = WaimaiCorpus()
    #
    # train_data, train_labels = corpus.get_train_corpus(train_num)
    # from spa.feature_extraction import ChiSquare
    # fe = ChiSquare(train_data, train_labels)
    # best_words = fe.best_words(feature_num)
    #
    # svm=SVMClassifier(train_data,train_labels,best_words,C)
    #
    # '''利用模型进行分析'''
    # svm=joblib.load("../saved_model/waimai.pkl")
    # print(svm.classify("没以前好吃了"))
    # print(svm.classify("超好吃"))




