path = "coll/"
from PIL import Image
import time
import os
from os import listdir
import copy

if not os.path.exists("coll"):
    # Create the folder
    os.mkdir("coll")
    print("S")

def main(repeats):
    faff = input("Welcome to the Collage Zone. Make sure you have added the pics to the folder 'coll'. The first time you answer this, it's probably best to just hit enter \nDo you want to faff? ")
    pix, min_side, params, area, equivalent = getpix()
    if equivalent:
        return(equivalent_suite(pix, min_side, params, area, repeats))
    if (
        faff in {"Y", "y"}
        or len(faff) < 5
        and len(faff) > 1
        and faff[0] in {"y", "Y"}
        and faff[1] in {"e", "E"}
    ):
        return advanced_suite(repeats)
    if (
        faff in {"", "n", "N"}
        or len(faff) < 4
        and faff[0].lower() == "n"
    ):
        pix = getpix()[0]
        printmostcompact(len(pix)**2, [0.5, 1, 1, 0])
        return

    return semi_advanced_suite(repeats)

def printmostcompact(x, params):
    min_bad = [[], 10**50]
    for i in range(x):
        pix, min_side, paramsthrowaway, area = getpix()
        params[-1] = i + 997
        print_complete = layout(copy.deepcopy(pix), min_side, params, area)
        total_area = print_complete[1][0] * print_complete[1][1]
        if print_complete[2] * total_area < min_bad[-1]:
            print_complete[2] *= total_area
            min_bad = print_complete
    coll(min_bad)


def coll(print_complete):
    if len(print_complete[0]) == 0:
        print("add pics to /coll/")
        return
    collage = Image.new("RGB", print_complete[1], (255, 255, 255))
    for name in print_complete[0]:
        collage.paste(Image.open(name[0]), (name[3], name[4]))
    collage.show()
    collage.save("coll"+str(int(time.time()))+".jpg",quality=99) 


def advanced_suite(repeats):
    def isfloat(x):
        try:
            float(x)
            return True
        except ValueError:
            return False

    pix, min_side, params, area = getpix()
    displayed = (
        "do you want to reshuffle? Type 'rs' ",
        "how much border do you like? try using lower numbers ",
        "How much top border do you like? ",
        "How much side border do you like? ",
    )
    print("this probably won't produce the best results (try trying something different next time)")
    params = [0, 0, 0, 0]
    for rep in range(repeats):
        for i in range(len(displayed)):
            text = input(displayed[i])
            if i == 0:
                if rep != 0:
                    if text.lower() == "rs":
                        params[-1] += 1000
                        print_complete = layout(copy.deepcopy(pix), min_side, params, area)
                        coll(print_complete)
                        break
                continue
            while not isfloat(text) or float(text) < -5 or float(text) > 19.9:
                print("enter a number between 0.1 and 10")
                text = input(displayed[i])
            params[i - 1] = float(text)
        if text.lower() == "rs":
            continue
        params[-1] = 0
        print_complete = layout(copy.deepcopy(pix), min_side, params, area)
        coll(print_complete)
        
def semi_advanced_suite(repeats):

    pix, min_side, params, area = getpix()
    displayed = (
        "how much border do you like? - type as many 'b's as you fancy (don't go overboard!)",
        "How much top border do you like? - type as many 'b's as you fancy ",
        "How much side border do you like? - type as many 'b's as you fancy ",
    )
    params = [0, 0, 0, 0]
    for rep in range(repeats):
        for i in range(len(displayed)):
            text = input(displayed[i])
            b=0
            for char in text:
                if char in {"b", "B"}:
                    b += 1
            
            if b > 0:
                params[i] = 0.1 * 1.5**b
            else:
                params[i] = 0
        printmostcompact(len(pix)**2, params)
        
def getpix():
    global path
    pix = []
    area = 0
    dimensions = (0, 0)
    equivalent = 0
    
    for i in os.listdir(path):
        if i == ".DS_Store":
            continue
        img = Image.open(path + i)
        x, y = img.size
        if dimensions[0] == x and dimensions[1] == y:
            equivalent += 1
        else:
            dimensions = (x, y)
        area += x * y
        pix.append([path + i, x, y, 0, 0])
    pix.sort()
    if equivalent == len(pix) - 1:
        equivalent = True
    else:
        equivalent = False
    for i in range(len(pix)):
        pix[i].append(i)
    min_length = int(area**0.5)
    return pix, min_length, [1, 1, 1, 0], area, equivalent


def layout(pix, min_side, params, area):
    widest = [0, 0, 0, 0, 0]
    tallest = [0, 0, 0, 0, 0]
    sprawlingest = [0]
    for pic in pix:
        if pic[1] > widest[1]:
            widest = pic
        if pic[2] > tallest[2]:
            tallest = pic
        area = pic[1] * pic[2]
        if area > sprawlingest[0]:
            sprawlingest = [area, pic]
    wide = []
    tall = []
    min_max_side = min_side
    for pic in pix:
        if pic[1] >= min_side:
            min_max_side = pic[1]
            wide.append(pic)
            continue
        if pic[2] >= min_side:
            min_side = pic[2]
            tall.append(pic)
    if min_max_side > min_side:
        min_side = min_max_side
    min_side = int(min_side * 1.3)
    
    if len(wide) + len(tall) == 0 and len(pix) < 4:
        pass
    orientation = 0
    if tallest[2] > widest[1]:
        orientation = 1
    if tallest[2] * 1.5 > widest[1] and len(tall) > 0:
        orientation = 1
    widest_tallest = [widest, tallest]
    print_complete = draw(
        pix, orientation, sprawlingest[1], widest_tallest, params, min_side, area
    )
    return print_complete


def draw(pix, orientation, sprawlingest, widest_tallest, params, min_side, area):
    # determine which pic to add next
    def nextpic(pix, print_folder, min_side, border, orientation, aspect):
        
        def returnbestmatch(print_folder, candidates, space):
            best = candidates[0]
            for pic in candidates:
                if (pic[aspect + 1] - print_folder[-1][aspect + 1])**2 < (best[aspect + 1] - print_folder[-1][aspect + 1])**2:
                    best = pic
            return best
        
        candidates = []
        for pic in pix:
            if (
                pic[1 + orientation]
                + print_folder[-1][1 + orientation]
                + print_folder[-1][3 + orientation]
                + border
                < min_side
            ):
                candidates.append(pic)
        if len(candidates) == 0:
            return pix[0]
        return returnbestmatch(print_folder.copy(), candidates, min_side - print_folder[-1][1 + orientation] - print_folder[-1][3 + orientation])

    # add x,y coordinates to the most recently added pic
    def addcoordinates(print_folder, min_side, border, orientation, aspect):
        if (
            print_folder[-1][orientation + 1]
            + print_folder[-2][orientation + 1]
            + print_folder[-2][orientation + 3]
            + border
            < min_side
        ):
            print_folder[-1][orientation + 3] = (
                print_folder[-2][orientation + 1]
                + print_folder[-2][orientation + 3]
                + border
            )
            print_folder[-1][aspect + 3] = print_folder[-2][aspect + 3]
        else:
            # find the most awkward pic added to print_folder recently, and copy its awkward height/width as 'mostawkward'
            mostawkward = 0
            for i in range(1, len(print_folder)):
                if print_folder[-1 - i][aspect + 1] > mostawkward:
                    mostawkward = print_folder[-1 - i][aspect + 1]
                if print_folder[-1 - i][orientation + 3] != 0:
                    continue
                # populate the coordinates with the correct layout data
                print_folder[-1][orientation + 3] = 0
                print_folder[-1][aspect + 3] = (
                    mostawkward + print_folder[-1 - i][aspect + 3] + border
                )
                break

    print_folder = []
    border = int(((area / len(pix))**0.5) * params[0])
    min_side += border * len(print_folder)**0.5
    top = int(((area / len(pix))**0.5) * params[1])
    side = int(((area / len(pix))**0.5) * params[2])
    aspect = 1
    if orientation == 1:
        aspect = 0
    ## add 'random' pics to print_folder
    rand = params[-1]
    while rand > 0 and len(pix) > 0:
        print_folder.append(pix[params[-1] % len(pix)])
        pix.remove(pix[params[-1] % len(pix)])
        if len(print_folder) > 1:
            addcoordinates(print_folder, min_side, border, orientation, aspect)
        rand -= 1

##    if len(print_folder) == 0:
##        print_folder.append(sprawlingest)
##        pix.remove(sprawlingest)
    if len(print_folder) == 0:
        print_folder.append(widest_tallest[orientation])
        pix.remove(widest_tallest[orientation])

    while len(pix) > 0:
        next_pic = nextpic(pix, print_folder, min_side, border, orientation, aspect)
        pix.remove(next_pic)
        print_folder.append(next_pic)
        addcoordinates(print_folder, min_side, border, orientation, aspect)

    # get size of the grid
    x = 0
    y = 0
    for pic in print_folder:
        if pic[1] + pic[3] > x:
            x = pic[1] + pic[3]
        if pic[2] + pic[4] > y:
            y = pic[2] + pic[4]

    unbalancedness = centreofmass(print_folder, x, y)

    # increase all coordinates in light of top/bottom and side borders
    for pic in print_folder:
        pic[3] += side
        pic[4] += top

    return [print_folder, (x + 2 * side, y + 2 * top), unbalancedness]

def centreofmass(print_folder, x, y):
    offset_x = 0
    offset_y = 0
    total_area = 0
    for pic in print_folder:
        area = pic[1] * pic[2]
        offset_x += (pic[3] + pic[1] / 2) * area
        offset_y += (pic[4] + pic[2] / 2) * area
        total_area += area
    ideal_x = x * total_area / 2
    ideal_y = y * total_area / 2
    offcentre_x = ideal_x - offset_x
    offcentre_y = ideal_y - offset_y
    
    unbalancedness = (offcentre_x**2 + offcentre_y**2)**0.5 / total_area 
    return unbalancedness + total_area**0.5

def equivalent_suite(pix, min_side, params, area, repeats):
    n = len(pix)
    candidates = []
    
    for i in range(1, n + 1):
        if n % i == 0 and pix[0][1] * n / i <= 2 * min_side and pix[0][1] * n / i >= 0.5 * min_side:
            candidates.append((i, pix[0][1] * n / (i**2 * pix[0][2])))
    if candidates == []:
        return semi_advanced_suite(repeats)
    candidate = (0, 11)
    for grouping in candidates:
        if grouping[1] + 1 / grouping[1] < candidate[1]:
            candidate = (grouping[0], grouping[1] + 1 / grouping[1])

    def isfloat(x):
        try:
            float(x)
            return True
        except ValueError:
            return False

    displayed = (
        "do you want to reshuffle? Type 'rs' ",
        "how much border do you like? try using lower numbers ",
        "How much top border do you like? ",
        "How much side border do you like? ",
    )
    params = [0, 0, 0, 0]
    for rep in range(repeats):
        for i in range(len(displayed)):
            text = input(displayed[i])
            if i == 0:
                if rep != 0:
                    if text.lower() == "rs":
                        params[-1] += 997
                        border = int(((area / len(pix))**0.5) * params[0])
                        min_side = candidate[0] * pix[0][1] + (candidate[0] - 1) * border
                        print_complete = layout(copy.deepcopy(pix), min_side, params, area)
                        coll(print_complete)
                        break
                continue
            while not isfloat(text) or float(text) < -5 or float(text) > 19.9:
                print("enter a number between 0.1 and 10")
                text = input(displayed[i])
            params[i - 1] = float(text)
        if text.lower() == "rs":
            continue
        params[-1] = 0
        border = int(((area / len(pix))**0.5) * params[0])
        min_side = candidate[0] * pix[0][1] + (candidate[0] - 1) * border
        print_complete = layout(copy.deepcopy(pix), min_side, params, area)
        coll(print_complete)  
    
if __name__ == "__main__":
    main(10)
