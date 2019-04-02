from bs4 import BeautifulSoup as bs
import requests, re
from fpdf import FPDF

title = "Doulou Dalu"

class Chapter:
    def __init__(self,number, chaptername ,content):
        self.number = number
        self.chaptername = chaptername
        self.content = content


class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 22)

        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # # Colors of frame, background and text
        # self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 230)
        self.set_text_color(220, 50, 50)
        # # Thickness of frame (1 mm)
        # self.set_line_width(1)
        # # Title
        self.cell(w, 9, title, 0, 1, 'C', 1)
        # # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)

        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)

        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, 'DuongHao314', 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name):
        # Read text file
        with open(name, 'rb') as fh:
            txt = fh.read().decode('utf-8')
        # Times 12
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)

        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()
        # Mention in italics

        self.cell(0, 5, '(Hết chương)')

    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)


def getNextChapter(soup):
    try:
        nextLinkTag = str(soup.find(rel="next"))
        nextChapterHalfLink = str(re.findall('href="(.*?)"', nextLinkTag)[0])
        nextChaterLink = 'http://truyencuatui.net' + nextChapterHalfLink
        return nextChaterLink
    except BaseException:
        return ""


def find_str(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index + len(char)] == char:
                    return index

            index += 1

    return -1


def getChapterName(soup):
    try:
        chapterTag = str(soup.find(id='b3'))
        chapterName = str(re.findall('<span>(.*?)</span>', chapterTag, flags=re.S | re.M | re.I)[0])
        return chapterName
    except BaseException:
        return 'error'


def getContents(soup):
    try:
        contentTag = str(soup.find_all('div', itemprop='articleBody'))
        #print(contentTag)
        contents = str(re.findall('articleBody">(.*?)<a href', contentTag, flags=re.S|re.M|re.I)[0])
        #print(contents)
        newContents = contents.replace('<br>', '\n')
        newContents = newContents.replace('<br/>', '\n')
        newContents = newContents.replace('<i>', '')
        newContents = newContents.replace('</i>', '')
        return newContents
    except BaseException:
        return 'Chương trống'


def getAll(beginLink):
    htmlLink = beginLink
    pdf = PDF()

    pdf.set_title(title)
    pdf.set_author('Duong Gia Tam Thieu')
    count = 0
    while len(htmlLink) > 0 and count < 200:
        htmlContent = requests.get(htmlLink).text

        soup = bs(htmlContent, 'html.parser')
        name = getChapterName(soup)
        print('Xử lý ' + name + '.....', end='')
        #fileName = getChapterName(soup).split(':')[0].split(' ')[1] + '.txt'
        fileName = 'currentChapter.txt'
        f = open(fileName, 'w', encoding='utf-8')
        f.write(name + '\n\n')
        f.write(getContents(soup))
        f.close()
        pdf.print_chapter(1, '', 'currentChapter.txt')
        htmlLink = getNextChapter(soup)
        print('thành công!')
        count += 1
    pdf.output('dldl.pdf', 'F')
def writeToPdf(list,author,outputname):
    pdf = PDF()

    pdf.set_title(title)
    pdf.set_author(author)
    for chapter in list:
        fileName = 'currentChapter.txt'
        f = open(fileName, 'w', encoding='utf-8')
        f.write(chapter.chaptername + '\n\n')
        f.write(chapter.content)
        f.close()
        pdf.print_chapter(chapter.number, '', 'currentChapter.txt')
        output = str(outputname) +'.pdf'
    pdf.output(output, 'F')
def getToClass(beginLink,author,output):
    htmlLink = beginLink
    count = 0
    list = []
    while len(htmlLink) > 0 and count < 20:
        htmlContent = requests.get(htmlLink).text

        soup = bs(htmlContent, 'html.parser')
        name = getChapterName(soup)
        print('Xử lý ' + name + '.....', end='')
        fileName = getChapterName(soup).split(':')[0].split(' ')[1]
        content = getContents(soup)
        currentChapter = Chapter(fileName, name,content)
        list.append(currentChapter)
        htmlLink = getNextChapter(soup)
        print('thành công!')
        count += 1
    print(list)
    writeToPdf(list,author,output)

"""--------------------------------------------"""
#link chương 1
htmlLink = 'http://truyencuatui.net/truyen/ta-la-chi-ton/chuong-185-cac-nguoi-cung-chung-ta-khong-cach-nao-/3146268.html'
getToClass(htmlLink,'Duong Gia Tam Thieu', 'douloudalu')

# pdf = PDF()
#
# pdf.set_title(title)
# pdf.set_author('Phong Lang Thien Ha')
# pdf.print_chapter(1, 'chapter 148', 'Chương 148.txt')
# pdf.print_chapter(1, 'chapter 149', 'Chương 149.txt')
# pdf.output('148-34442.pdf', 'F')
