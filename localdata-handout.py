
import csv
import xml.dom.minidom as parser
from math import sqrt, pi, ceil, floor

size(210*mm, 297*mm)
colormode(CMYK)

fillclr = (color(1, 0, 0, 0.25))
fillclrop = (color(1, 0, 0, 0.25, 0.4))

fillclr50p = (color(0.5, 0, 0, 0.125))
fillclr25p = (0, 0, 0, 0.25)
fillclr15p = (color(0, 0, 0, 0.25, 0.5))
fillclr_red = (color(0, 0.5, 0.2, 0, 0.5)) 

fillclr0op = (1, 0.3)
white = 1

textfill = (0, 0, 0, 1)



# ///////////////// SETUP ////////////////////



class Reader:
    
    #Reader reads in a csv file and stores the data
    
    def __init__(self, file, dl=";"):
            
        # We read in all the rows as a list.
        # We can't use "for row in reader" since we want to know the total length. 
        self.rows = list(csv.reader(open(file, "rU"), delimiter=dl))
        self.header_row = self.rows[0]
        self.column_count = len(self.header_row)

        self.rows = self.rows[1:]
        self.row_count = len(self.rows)

        # Turn the row data into columns.
        self.columns = {}
        for row in self.rows:
            for i, value in enumerate(row):
                try:
                    value = float(value)
                except ValueError:
                    pass
                column_values = self.columns.get(i, [])
                column_values.append(value)
                self.columns[i] = column_values
        


# ------------ plotting functions -------------

# Simple line graph
def plot_line_horizontal(datarow, x, y, value_scale, spacing, height=45, scalestep=5000, range=2000): 
    points = []
    xs = 0
    print sum(datarow)
    average = float(sum(datarow)) / float(len(datarow))
    
    #!FIXIT! Floor, ceil
    maxval = int(ceil(max(datarow)+range)/scalestep)*scalestep
    min_y = int(floor(min(datarow)-range)/scalestep)*scalestep
    
    vscalef = ((maxval-min_y)*value_scale)/height

    
    for entry in datarow:
            entry = float(entry)
            ypos = ((entry-min_y)*value_scale)/vscalef
            points.append(Point(xs, ypos))
            xs +=spacing
    push()

    translate(x, y)
    #zero-point
    stroke(fillclr)
    
    line(0, 0, xs-spacing, 0)
    selite_align(format_number(min_y), -55, 3)
    
    selite_align(format_number(maxval), -55, -((maxval-min_y)*value_scale)/vscalef+3)
    line(0, -((maxval-min_y)*value_scale/vscalef), xs-spacing, -((maxval-min_y)*value_scale)/vscalef)

    
    nofill()
    strokewidth(2)
    beginpath()
    moveto(points[0].x, -points[0].y)
    for point in points:
        x1=point.x
        y1=point.y
        lineto(x1, -y1)
    autoclosepath(False)    
    endpath()
    pop()





# Horizontal bar plot
def plot_bar_horizontal(datacolumn, x, y, value_scale, bar_height, h_spacing, textfield=50): 
    push()
   
    for entry in datacolumn:
        try: 
            entry = float(entry)
            width = entry*value_scale
            rect(x, y-bar_height/3, width, bar_height)
            translate(0, bar_height+h_spacing)
        
        except ValueError:
            align(RIGHT)
            entry = entry.decode("utf-8")
            text(entry, x, y+fontsize()/2, width=textfield)
            translate(0, bar_height+h_spacing)
    pop()
    
    
# Horizontal sum bar plot
def plot_sumbar(data, x, y, value_scale, width, height, labels=None, textfield=50, altfill=True): 
    push()
    stroke(white)
    fill0=fillclr
    
    total = float(sum(data))
    ws = total/width
    yshift = 0
    for i in range(len(data)):
        entry = float(data[i])

        w = (entry*value_scale)/ws

        if labels:
            label = labels[i].decode("utf-8")       
            if i > len(data)-2:label = "muut"       # hackish way of making the last label into "others"             
            push()
            if w<28:
                transform(CORNER)
                translate(-25, y+height+45)
    
                rotate(45)
                selite_align(label, 0, 0, fontsz=10, width=55)
            
            else: 
                translate(5, y+height+10)
                selite(label, 0, 0)
            pop()
                    
        # draw the bars & percentages
        fill(fill0)  
        rect(x, y, w, height)
        selite_align(str(int(entry)), 8, y+height-6, al=LEFT, fillcolor=white)

        translate(w, 0)
        if fill0==fillclr:
            fill0= fillclr50p 
        else: fill0=fillclr
    selite_align("100 %", 8, y+height-6, al=LEFT, fillcolor=textfill)

        
    pop()    
    
    
# Area plot
def area_from_value(value,x=0, y=0, s=1, type="C"):
    fill(fillclr)

    if type=="C":
    
        d = 2*(sqrt(value/pi))
        ds = d*s
        oval(x, y-ds/2, ds, ds)
 
    elif type=="S":
        w = sqrt(value)
        ws = w*s                
        rect(x-ws/2, y, ws, ws)
    else:
        print "type must be either \"C\" for circle or \"S\" for square"
        return
        
# Unit figure plot        
def symbols_from_value(value,x=0, y=0, s=1, unit=10, squared=False, gridw=10, gridh=10, cs=10, rs=10, ssize= 10, paths=None):
    unitvalue = float(value/unit)
    vsq =  ceil(sqrt(unitvalue))
    fill(fillclr)
    
    if squared:
        if vsq > gridw: 
            gridh += vsq-gridw
        else:
            gridw = vsq
            gridh= vsq
    
    #unitvalue = int(unitvalue)
    #print unitvalue    
    
    
    push()
    translate(x, y)

    x1=0
    y1=0
    for i in range(int(unitvalue)):
        if i!=0 and i%gridw == 0:
            x1 = 0
            y1 += rs
        rect(x1, y1, ssize, ssize)
        x1 += cs
    
    # add a half-unit at the end if necessary
    if round(unitvalue-int(unitvalue))!=0:
        rect(x1, y1, ssize/2, ssize)

    # get the width of the figure
    graphwidth = gridw*cs
    if unitvalue < gridw:
        graphwidth = int(unitvalue*cs)
           
    """   
    ## old version using grid function
      
    n = 0

    for x1, y1 in grid(gridw, gridh, cs, rs):
        if n < unitvalue: 
            if paths == None:
                rect(x1, y1, ssize, ssize)
            else:
                psz=bounds([paths])
                pw, ph = psz[1][0], psz[1][1]
                drawpaths([paths], x1, y1, scale=s)
            n+=1
    """
    pop()
    return graphwidth
    
    
# ------------ Utility functions -------------   


#number formatting function
def format_number (n, number_format="fi"):
    s = str (n).partition(".")
    suffix = s[2]
    s = s[0]
    if (len(suffix) > 0):
        if (number_format == "fi"): suffix = "," + s
        if (number_format == "en"): suffix = "." + s
    for i in range (len (s) / 3):
        if i == 0: j = len (s) - (i) * 3 - 3
        j = len (s) - (i) * 4 - 3
        s = s [0:j] + ":" + s [j:len (s)]
    if (number_format == "fi"): s = s.replace (":", " ")
    if (number_format == "en"): s = s.replace (":", ",")
    return s + suffix    
    

# preparing percentages

def cook_percentages(data, decimals=1, cutoff= 6):
    total = float(sum(data))
    percentages = []
    sum_cutoff = 0
    #assuming a sorted list with cathegory "others" at end
    for i in range(len(data)):
        entry = round((data[i]/total)*100, decimals)  
        if i < cutoff:
            percentages.append(entry)
        else: sum_cutoff +=entry
    #appending summedpercentages at end of list 
    if sum_cutoff !=0:  percentages.append(round(sum_cutoff, decimals))
    return percentages    



# ------------ SVG utils ----------------
def bounds(paths=[]):
   """ Returns (x, y), (width, height) bounds for a group of paths.
   """
   if len(paths) == 0: 
       return (0,0), (0,0)
   l = t = float("inf")
   r = b = float("-inf")
   for path in paths:
       (x, y), (w, h) = path.bounds
       l = min(l, x)
       t = min(t, y)
       r = max(r, x+w)
       b = max(b, y+h)
   return (l, t), (r-l, b-t)
def drawpaths(paths=[], x=0, y=0, rotate=0, scale=1, origin=(0, 0)):
   """ Draws a group of paths that rotate and scale from the given origin.
   """
   _ctx.transform(CORNER)
   _ctx.push()
   _ctx.translate(x, y)
   _ctx.rotate(rotate)
   _ctx.scale(scale)
   (x, y), (w, h) = bounds(paths)
   _ctx.translate((-x-w)*origin[0], (-y-h)*origin[1])
   for path in paths:
       #_ctx.fill(path.fill)
       #_ctx.stroke(path.stroke)
       #_ctx.strokewidth(path.strokewidth)
       # Use copies of the paths that adhere to the transformations.
       _ctx.drawpath(path.copy())
   _ctx.pop()





# ------------ Typography -------------

type_normal = "PT Sans"
type_bold = "PT Sans Bold"

def header(txt, x, y, typeface=type_bold, fontsz=25, fillcolor=textfill):
    fill(fillcolor)
    font(typeface, fontsz)
    text(txt, x, y)
    return textheight(txt) 

def selite(txt, x, y, typeface=type_normal, fontsz=10, fillcolor=textfill):
    fill(fillcolor)

    font(typeface, fontsz)
    text(txt, x, y)
    return textheight(txt) 
    
def selite_align(txt, x, y, typeface=type_normal, fontsz=8, al=RIGHT, width=50, fillcolor=textfill):
    fill(fillcolor)

    align(al)
    font(typeface, fontsz)
    text(txt, x, y, width)
    return textheight(txt) 
    
    

def selite_bold(txt, x, y, typeface=type_bold, fontsz=10, fillcolor=textfill):
    fill(fillcolor)

    font(typeface, fontsz)
    text(txt, x, y)
    return textheight(txt) 


def hz_hairline(y):
    stroke(fillclr)
    strokewidth(0.75)
    line(0, y, WIDTH, y) 
    nostroke()
    
    
# ///////////////// BUILDING THE VISUALISATION ////////////////////

district = "703"

keyfigures = Reader(u"full-data/regions.csv")
#keyfigures = Reader(u"region-data/"+ district + "_regions.csv")
#columnskf= keyfigures.columns

#popproject = Reader(u"region-data/"+ district +"_population.csv")
popproject = Reader(u"full-data/population.csv")

#languages = Reader(u"region-data/" + district + "_languages.csv")
languages = Reader(u"full-data/languages.csv")

#voting = Reader(u"region-data/" + district + "_voting.csv")
voting = Reader(u"full-data/voting.csv")

regionnames = Reader(u"full-data/region-names.csv")

leftmargin = 5

baseline0 = 120
baseline1 = 260
baseline2 = 400
baseline3 = 610


datascaling = 0.001
bar_spacing = 2
bar_width = 14
textfield_width = 150
text_spacing = 10
unit = 1000

xpos= 0

curRow = None
for row in regionnames.rows:
    if(row[0] == district): curRow = row
title= curRow[1].decode("utf-8")
header(title, leftmargin, 30)

# --------- Helsinki population

keyfigureData = None
for row in keyfigures.rows:
    if(row[0] == district): keyfigureData = row
keyfigureLabels = keyfigures.header_row

keyfigureData = keyfigureData[1:]
keyfigureLabels = keyfigureLabels[1:]
fullCityData = keyfigures.rows[0]

hpop = int(fullCityData[14])

selite(u"Helsingin väkiluku\n"+format_number(int(hpop)), leftmargin, baseline0-60)
area_from_value(hpop, leftmargin, baseline0, 0.10)

# Area population
apop = int(keyfigureData[13])
selite(u"Peruspiirin väkiluku\n"+format_number(int(apop)), leftmargin+120, baseline0-60)
area_from_value(apop, leftmargin+120, baseline0, 0.10)


hz_hairline(baseline1-55)

# --------- Demographics

selite_bold(u"Väestö", leftmargin, baseline1-40)  

push()

#print keyfigureLabels
#print keyfigureData

over15 = int(keyfigureData[27])
over65 = int(keyfigureData[20])
from15to65 = over15-over65
under15 = apop-over15

head = ["Alle 15-v","15-65-vuotiaat","Yli 65-vuotiaat"]
val = [under15, from15to65, over65]

# Printing numbers from rows concerning age distribution
for i in range(0,3):
    header = head[i]
    header = header.decode("utf-8")
    dval = val[i]
    print header
    print dval
    
    selite(header+"\n"+format_number(int(dval)), leftmargin, baseline1-20)  

    xpos = symbols_from_value(dval, leftmargin, baseline1, unit=unit, gridw=10, gridh=20, ssize=9)
    translate(xpos +30, 0) 
    
pop()

#---- population prediction 
#print  popproject.rows[0][1:]  
selite(u"Väestöennuste",  leftmargin+350, baseline1-20)  

curRow = None
for row in popproject.rows:
    if(row[0] == district): curRow = row

items = []
for item in curRow[1:]:
    items.append(int(item))

plot_line_horizontal(items, leftmargin+350, baseline1+30, 0.008, 5)

vuodet=[1, 10, 20, 27, 35]
for vuosi in vuodet:
    fill(white)
    nostroke()
    rect(leftmargin+350+(vuosi-1)*5, baseline1+28, 2, 3)
    fill(fillclr0op)
    rect(leftmargin+350+(27-1)*5, baseline1-14, 40, 43)

    selite_align(str(popproject.header_row[vuosi]), leftmargin+326+(vuosi-1)*5, baseline1+42,  al=CENTER)
    
hz_hairline(baseline2-55)

#---- Languages

selite_bold(u"Puhutut kielet", leftmargin, baseline2-40)  

curRow = None
for row in languages.rows:
    if(row[0] == district): curRow = row

unzipped = zip(*sorted(zip(languages.header_row[2:-1], curRow[2:-1]), key=lambda x: -int(x[1])))
labels = list(unzipped[0])
rawvalues = list(unzipped[1])
labels.append(languages.header_row[-1])
rawvalues.append(curRow[-1])

values = list()
for x in rawvalues:
    values.append(int(x))

mainlanguages =  cook_percentages(values, cutoff = 2)
seclanguages = cook_percentages(values[2:], cutoff = 8)

selite(u"Kaksi puhutuinta kieltä, prosenttia väestöstä", leftmargin, baseline2-10) 
plot_sumbar(mainlanguages, leftmargin, baseline2, 1, 400, 20, labels=labels, altfill= True)

selite(u"Puhutuimmat muut kielet, prosenttia", leftmargin, baseline2-10+70) 
plot_sumbar(seclanguages, leftmargin, baseline2+70, 1, 400, 20, labels=labels[2:], altfill= True)    



hz_hairline(baseline3-55)

#---- Voting

curRow = None
for row in voting.rows:
    if(row[0] == district): curRow = row

unzipped = zip(*sorted(zip(voting.header_row[1:-2], curRow[1:-2]), key=lambda x: -float(x[1])))
labels = list(unzipped[0])
rawvalues = list(unzipped[1])
labels.append(voting.header_row[-2])
rawvalues.append(curRow[-2])

values = list()
for x in rawvalues:
    values.append(float(x))

votingresults = cook_percentages(values, cutoff = 6)
print votingresults

selite_bold(u"Vaalitulokset", leftmargin, baseline3-40)  

votingpercentage = str(curRow[-1])

selite(u"Äänestystulokset eduskuntavaaleissa 2007, äänestysprosentti " + votingpercentage + " %", leftmargin, baseline3-10) 

plot_sumbar(votingresults, leftmargin, baseline3, 1, 400, 20, labels=labels, altfill= True)



    
#---- Map

try:
    svg = ximport("svg")
except:
    svg = ximport("__init__")
    reload(svg)

# The parse() command will return
# a list of the shapes in the SVG file.
path_ids = svg.parse_as_dict(open("full-data/basedistricts.svg").read())


paths= path_ids[0]
keys= path_ids[1]


index = keys.index(district) 
#print keys
#print index




fill(0.9)
translate(340,10)
drawpaths(paths[1:], scale=0.035)
push()
scale(0.035)

fill(0.5)
nostroke()
drawpath(paths[0])
pop()
strokewidth(25)
stroke(1)

nofill()
drawpaths(paths[1:], scale=0.035)

scale(0.035)
stroke(1)
strokewidth(35)
selectedclr = fillclrop
fill(selectedclr)
p = (paths[index])

# centerpoint and name of borough 
(x, y), (w, h) = p.bounds
cx = (x+w/2)  
cy = (y+h/2)   
drawpath(p)
fill(0)
psz=25
#text(keys[index], cx, cy-psz)


