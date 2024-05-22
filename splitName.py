import re

# Thai text with English text
text = "4U2 For You Too Shimmer Blush 5g #03 Bride To Be บลัชออนสูตรชิมเมอร์ จากโฟร์ยูทู เนื้อเนียนละเอียด บางเบา เกลี่ยง่าย ติดทนตลอดวัน แต่งเติมแก้มสีสวยหวาน เปล่งประกาย ดูเปล่งปลั่งเป็นธรรมชาติ"

# Split Thai and English text
thai_text = re.findall(r'[\u0E00-\u0E7F\s]+', text)
english_text = re.findall(r'[A-Za-z#0-9\s]+', text)

print("Thai Text:", thai_text)
print("English Text:", english_text)

txt = "4U2 For You Too Shimmer Blush 5g #03 Bride To Be"

x = txt.split("#")

print(x)
