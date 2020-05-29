#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import json
import textwrap

#img = Image.new('RGBA', (981, 552), color = (73, 109, 137))
#d = ImageDraw.Draw(img)
#img.save('test.png')

def createImages(keyword):

    f=open("json/"+keyword+".json", "r")

    data = json.loads(f.read())
    print(json.dumps(data, indent=2, sort_keys=True))

    max_words = 16

    for i in (data):
        img = Image.open("bg0.jpeg")
        w, h = img.size

        img = img.convert("RGBA")

        tmp = Image.new('RGBA', img.size, (0,0,0,0))

        draw = ImageDraw.Draw(tmp)
        draw.rectangle([(50, 50), (w - 50, h - 50)], fill=(0,0,0,127))

        img = Image.alpha_composite(img, tmp)
        img = img.convert("RGB") # Remove alpha for saving in jpg format.
        #img.save('test.png')
        d = ImageDraw.Draw(img)
        
        quote = "\""
        quote += i.get('quote')
        quote += "\""
        author = "- "
        author += i.get('author')
        
        words = quote.split(' ')
        
        lines = textwrap.wrap(quote, width=15)
        y_text = h/6
        x_text = w
        
        # tweak those based on image size
        fontSize1 = 120
        try:
            ratio = (w/7)
            fontSize1 = int(ratio)
        except:
            print("test")

        fontSize2 = int(2 * fontSize1 /3)
        print(fontSize2)

        font = ImageFont.truetype(r'Amatic_SC/AmaticSC-Regular.ttf', fontSize1)
        font2 = ImageFont.truetype(r'Amatic_SC/AmaticSC-Bold.ttf', fontSize2)
        
        for line in lines:
            width, height = font.getsize(line)
            print(lines)
            d.text(((x_text - width) / 2 + 8, y_text + 8), line, font=font, fill=(0,0,0))
            d.text(((x_text - width) / 2, y_text), line, font=font, fill=(255,255,255))
            y_text += height


        a_x = ( (w-60) - (len(author)*40) )
        #a_x = 200
        a_y = h - 250
        
        d.text( (a_x + 8, a_y + 8), author, font=font2, fill=(0,0,0), align ="right",spacing=54)

        d.text( (a_x, a_y), author, font=font2, fill=(255,255,255), align ="right",spacing=54)

        img.save('img/'+author.replace('-','')+' '+quote+'.png')
        
        quote = ""

