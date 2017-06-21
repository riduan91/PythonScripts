# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import re

VNNorUpLets = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
               'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V',
               'W', 'X', 'Y', 'Z']
VNSpecUpLets = ['Ă', 'Â', 'Ê', 'Ô', 'Ơ', 'Ư', 'Đ',
          'À', 'Ằ', 'Ầ', 'È', 'Ề', 'Ì', 'Ò', 'Ồ', 'Ờ', 'Ù', 'Ừ', 'Ỳ',
          'Á', 'Ắ', 'Ấ', 'É', 'Ế', 'Í', 'Ó', 'Ố', 'Ớ', 'Ú', 'Ứ', 'Ý',
          'Ả', 'Ẳ', 'Ẩ', 'Ẻ', 'Ể', 'Ỉ', 'Ỏ', 'Ổ', 'Ở', 'Ủ', 'Ử', 'Ỷ',
          'Ã', 'Ẵ', 'Ẫ', 'Ẽ', 'Ễ', 'Ĩ', 'Õ', 'Ỗ', 'Ỡ', 'Ũ', 'Ữ', 'Ỹ',
          'Ạ', 'Ặ', 'Ậ', 'Ẹ', 'Ệ', 'Ị', 'Ọ', 'Ộ', 'Ợ', 'Ụ', 'Ự', 'Ỵ']

VNFalsePropNouns = ['ND', 'Mùa', 'Ngày', 'Tháng', 'Năm', 'Bọn', 'Lúc', 'Ở', 'Đời', 'Xem', 
                    'Khi', 'Ấy', 'Rồi', 'Sai', 'Riêng', 'Chỉ', 'Con', 'Còn', 'Dùng', 'Đổi', 
                    'Đến', 'Quyển', 'Người', 'Để', 'Nhưng', 'Bổ', 'Chb', 'Chức', 'Do', 'Dân',
                    'Em', 'Giáng', 'Giặc', 'Giết', 'Nay', 'Sau', 'Theo', 'Tên', 'Tước', 'Tượng',
                    'Việc', 'Vợ', 'Đều', 'Đặt', 'Đầu', 'Đất']
VNFalseUnpropNouns = ['vương', 'hầu', 'sứ', 'đế', 'công']

VNHistoryIdentities = ['Chùa', 'Núi', 'Sông', 'Phủ', 'Hồ', 'Thành', 'Thánh', 'Động', 'Đồi', 
                       'Đền', 'Quận', 'Huyện', 'Cửa', 'Nhà', 'Bộ', 'Chúa', 'Chợ', 'Cầu',
                       'Họ', 'Hội', 'Làng', 'Xã', 'Sao', 'Sách', 'Sư', 'Thời', 'Triều',
                       'Trường', 'Trấn', 'Tướng', 'Vua', 'Vùng', 'Điện', 'Đèo']

def isVNCapital(word):
    '''
    Kiểm tra một tiếng được viết hoa trong tiếng Việt
    '''
    if len(word) <= 0:
        return False
    if word[0] in VNNorUpLets:
        return True
    if len(word) <= 1:
        return False
    if word[0:2] in VNSpecUpLets:
        return True
    if len(word) <= 2:
        return False
    if word[0:3] in VNSpecUpLets:
        return True
    return False

def retrieveProperNounsFromSentence(sentence):
    '''
    Lấy ra tất cả các danh từ riêng trong một câu
    '''
    propNounsList = []
    #words = re.split(" |, |\. |\: |; ", sentence)
    words = re.split(" ", sentence)
    currentPropNoun = ""
    for word in words:
        if isVNCapital(word) or word in VNFalseUnpropNouns:
            if not (word in VNFalsePropNouns and len(currentPropNoun)==0):
                currentPropNoun += " " + word
            if re.compile(r',|;|:|\.|\-|\!|\?|\-').search(word) is not None:
                if len(currentPropNoun)>0:
                    if (" " in currentPropNoun[1:]):
                        propNounsList.append(clean(currentPropNoun[1:]))
                    currentPropNoun = ""
        else:
            if len(currentPropNoun)>0:
                if " " in currentPropNoun[1:]:
                    propNounsList.append(clean(currentPropNoun[1:]))
                currentPropNoun = ""
    if len(currentPropNoun)>0:
        if " " in currentPropNoun[1:]:
            propNounsList.append(clean(currentPropNoun[1:]))
        currentPropNoun = ""    
    return propNounsList

def retrieveProperNounsFromFile(myfile):
    '''
    '''
    myfile = open(myfile, 'r')
    text = myfile.read()
    sentences = text.split("\n")
    propNounsList = []
    for sentence in sentences:
        propNounsList += retrieveProperNounsFromSentence(sentence)
    myfile.close()
    return sorted(set(propNounsList))

def retrieveProperNounsFromFileByLine(myfile):
    '''
    '''
    myfile = open(myfile, 'r')
    text = myfile.read()
    sentences = text.split("\n")
    propNounsList = []
    for sentence in sentences:
        propNounsList.append("\t".join(retrieveProperNounsFromSentence(sentence)))
    myfile.close()
    return propNounsList

def clean(word):
    '''
    '''
    return re.sub("\)|\.|[0-9]|\"|\]|,|;|:|\+|\?|\!|\-", "", word)

def reformat(myfile, mynewfile):
    text = open(myfile, 'r').read()
    text = re.sub("(Quyển.+[IVXLCDM]+)", r"\1.", text)
    text = re.sub("(Quyển.+[IVXLCDM]+)\.\.", r"\1.", text)
    text = re.sub("\.\n", "\t\t", text)
    text = re.sub("\.\n([0-9]+) ", r"\t\t\t\t\1 ", text)
    text = re.sub("\n([0-9]+) ", r"\t\t\t\1 ", text)
    text = re.sub("\n", " ", text)
    text = re.sub("  ", " ", text)
    text = re.sub("\t\t\t\t", ".\n", text)
    text = re.sub("\t\t\t", "\n", text)
    text = re.sub("\t\t", ".\n", text)
    f = open(mynewfile, 'w')
    f.write(text)
    f.close()

def getNotice(myfile, myfileupdated, mynoticefile):
    lines = open(myfile, 'r').readlines()
    f = open(mynoticefile, 'w')
    g = open(myfileupdated, 'w')
    for line in lines:
        if re.match("^([0-9]+ ).+$", line) and not re.match("^([0-9]+ [a-z\(]).+$", line):
            f.write(line)
        else:
            g.write(line)
    f.close()
    g.close()
    



                