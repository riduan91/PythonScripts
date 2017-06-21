# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 23:17:35 2017

@author: ndoannguyen
"""

def decode(s):
    s = s.replace("Ã ", "à").replace("áº£", "ả").replace("Ã£", "ã").replace("áº¡", "ạ")
    s = s.replace("Äƒ", "ă").replace("XXX", "ằ" ).replace("XXX", "ắ").replace("XXX", "ẳ").replace("XXX", "ẵ").replace("XXX", "ặ")
    s = s.replace("Ã¢", "â").replace("áº§", "ầ" ).replace("áº¥", "ấ").replace("XXX", "ẩ").replace("XXX", "ẫ").replace("XXX", "ặ")
    s = s.replace("Ã¨", "è").replace("XXX", "é" ).replace("XXX", "ẻ").replace("XXX", "ẽ").replace("XXX", "ẹ")
    s = s.replace("Ãª", "ê").replace("XXX", "ề").replace("áº¿", "ế" ).replace("á»ƒ", "ể").replace("á»…", "ễ").replace("á»‡", "ệ")
    s = s.replace("Ã¬", "ì").replace("á»‰", "ỉ").replace("Ä©", "ĩ").replace("á»‹", "ị")
    s = s.replace("Ã²", "ò").replace("Ã³", "ó" ).replace("XXX", "ỏ").replace("XXX", "õ")
    s = s.replace("Ã´", "ô").replace("XXX", "ồ").replace("á»‘", "ố" ).replace("á»•", "ổ").replace("XXX", "ỗ").replace("á»™", "ộ")
    s = s.replace("Æ¡", "ơ").replace("Ã¡»", "ờ").replace("á»›", "ớ" ).replace("XXX", "ở").replace("XXX", "ỡ").replace("á»£", "ợ").replace("á»", "ọ")
    s = s.replace("Ã¹", "ù").replace("Ãº", "ú" ).replace("á»§", "ủ").replace("XXX", "ũ").replace("á»¥", "ụ")
    s = s.replace("Æ°", "ư").replace("á»«", "ừ").replace("á»©", "ứ" ).replace("XXX", "ử").replace("á»¯", "ữ").replace("á»±", "ự")
    s = s.replace("XXX", "ỳ").replace("XXX", "ý" ).replace("XXX", "ỷ").replace("XXX", "ỹ").replace("XXX", "ỵ")
    s = s.replace("Ä‘", "đ").replace("Ä", "Đ").replace("Ã¡", "á" ).replace("Ã", "í" )
    return s
    
print decode("Em mong muá»‘n quá»¹ há»c bá»•ng Äá»“ng HÃ nh cÃ³ thÃªm nhá»¯ng há»c bá»•ng khÃ¡c nhau phÃ¹ há»£p cho tá»«ng hoÃ n cáº£nh Ä‘á»ƒ giÃºp Ä‘á»¡ cÃ¡c báº¡n sinh viÃªn khÃ³ khÄƒn vÆ°á»£t khÃ³ há»c táº­p.­")