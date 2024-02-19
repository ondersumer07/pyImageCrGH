from PIL import Image, ImageDraw, ImageFont
from datetime import date
import requests
import os

# get data from pockethost
api_url = "https://personal-website.pockethost.io/api/collections/poems/records?perPage=101"
response = requests.get(api_url)
data = response.json()

interExtraBold = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 'fonts/Inter-ExtraBold.ttf'
    )
)

interRegular = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 'fonts/Inter-Regular.ttf'
    )
)

interLightItalic = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 'fonts/Inter-LightItalic.otf'
    )
)

def createPoemImage():
    # get poem number from public api
    poemNumApi = "http://ondersumer07.pythonanywhere.com/randomNumAPI"
    responsePoemNum = requests.get(poemNumApi)
    dataPoemNum = responsePoemNum.json()
    # dataPoemNum["randomNum"]
    poemNum = dataPoemNum["randomNum"]

    # get POEM
    poemData =  data["items"][poemNum]["poem"]

    # CLEAR poem from '\r'
    def clearPoem():
        poem = poemData.translate(str.maketrans('', '', '\r'))
        return poem

    # get POEM LINE COUNT to decide on height
    poemLineCount = clearPoem().count('\n')

    # get LONGEST LINE in poem
    def longestLineFinder(poem):
        lines = poem.splitlines()
        longestline = max(lines, key=len)
        return longestline

    # create FONT OBJECTS
    fontObjectTitle = ImageFont.truetype(font=interExtraBold, size=40)
    fontObjectPoem = ImageFont.truetype(font=interRegular, size=30)
    fontObjectSource = ImageFont.truetype(font=interLightItalic, size=20)

    # calculate the IDEAL HEIGHT of picture and source
    idealHeightofSource = 1500

    if(poemLineCount >= 50):
        idealHeightofSource = 150 + poemLineCount*fontObjectPoem.getmask(clearPoem()).getbbox()[3] - 50
        print(poemLineCount)
    if(poemLineCount < 50):
        idealHeightofSource = 150 + poemLineCount*fontObjectPoem.getmask(clearPoem()).getbbox()[3] + 50
        print(poemLineCount)

    heightOfWebsite = idealHeightofSource + 50
    idealHeightofPic =heightOfWebsite + 120

    # calculate poem TITLE and LONGEST LINE WIDTH to make sure it fits
    pageWidth = 1500
    widthOfTitle = fontObjectTitle.getlength(data["items"][poemNum]["title"])
    longestLineWidth = fontObjectPoem.getlength(longestLineFinder(poemData))

    if(widthOfTitle > 1400):
        pageWidth = int(widthOfTitle) + 200

    if(longestLineWidth > 1400):
        pageWidth = int(longestLineWidth) + 200

    # calculate idealPoemWidth here, so if pageWidth changes it's correct
    idealPoemWidth = (pageWidth - longestLineWidth) / 2

    # CREATE image
    imgObj = Image.new("RGB", (pageWidth,idealHeightofPic), (31,27,24))
    drawingObject = ImageDraw.Draw(imgObj)

    # draw the image
    drawingObject.text((pageWidth/2,75), data["items"][poemNum]["title"], (251,231,209), font=fontObjectTitle, anchor="mt")
    drawingObject.text((idealPoemWidth,150), clearPoem(), (251,231,209), font=fontObjectPoem)
    drawingObject.text((pageWidth/2,idealHeightofSource), "From " + data["items"][poemNum]["source"], (251,231,209), font=fontObjectSource, anchor="mt")
    drawingObject.text((pageWidth/2,idealHeightofSource+100), "ondersumer.com  •  Poem of the day, " + date.today().strftime("%d %b %Y"), (251,231,209), font=fontObjectSource, anchor="mt")

    imgObj.save("todaysPoem.jpg")

createPoemImage()