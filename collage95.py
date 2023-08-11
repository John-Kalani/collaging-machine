path = "/Users/mac/Documents/coll/"
from PIL import Image
import time
import os
from os import listdir
print("it probably makes sense to just hit enter the first time at least")

def main(repeats):
    faff = input("Welcome to the Collage Zone. Do you want to faff? ")
    if (
        faff in {"Y", "y"}
        or len(faff) < 5
        and len(faff) > 1
        and faff[0] in {"y", "Y"}
        and faff[1] in {"e", "E"}
    ):
        return semi_advanced_suite(repeats)
    if (
        faff in {"", "n", "N"}
        or len(faff) < 4
        and faff[0].lower() == "n"
    ):
        pix = getpix()[0]
        printmostcompact(len(pix)**2)
        return
    print("just hit enter next time. you're being transferred to the advanced suite, which is not working well")
    for i in range(repeats):
        pass
    return semi_advanced_suite(repeats)

def printmostcompact(x):
    min_area = [10**10, []]
    for i in range(1, x):
        pix, min_side, params, area = getpix()
        params[-1] = i
        print_complete = layout(pix, min_side, params, area)
        total_area = print_complete[1][0] * print_complete[1][1]
        if total_area < min_area[0]:
            min_area = [total_area, print_complete]
    coll(min_area[1])


def coll(print_complete):
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
        "how much border do you like? ",
        "How much top border do you like? ",
        "How much side border do you like? ",
    )
    print("This isn't working properly ATM")
    params = [0, 0, 0, 0]
    for rep in range(repeats):
        for i in range(len(displayed)):
            text = input(displayed[i])
            if i == 0:
                if rep != 0:
                    if text.lower() == "rs":
                        params[-1] += 1
                        print_complete = layout(pix.copy(), min_side, params, area)
                        coll(print_complete)
                        break
                continue
            while not isfloat(text) or float(text) < -5 or float(text) > 20:
                print("enter a number between 0.1 and 10")
                text = input(displayed[i])
            params[i - 1] = float(text)
        if text.lower() == "rs":
            continue
        params[-1] = 0
        print_complete = layout(pix.copy(), min_side, params, area)
        coll(print_complete)
        
def semi_advanced_suite(repeats):

    pix, min_side, params, area = getpix()
    displayed = (
        "how much border do you like? - type as many 'b's as you fancy ",
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
            
            params[i] = b
        
        print_complete = layout(pix, min_side, params, area)
        coll(print_complete)
        
def getpix():
    global path
    pix = []
    area = 0
    for i in os.listdir(path):
        if i == ".DS_Store":
            continue
        img = Image.open(path + i)
        x, y = img.size
        area += x * y
        pix.append([path + i, x, y, 0, 0])
    pix.sort()
    for i in range(len(pix)):
        pix[i].append(i)
    min_length = int(area**0.5)
    return pix, min_length, [0.5, 5, 5, 0], area


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
    min_side = int(min_side * 1.5)
    
    if len(wide) + len(tall) == 0 and len(pix) > 3:
        pass
    orientation = 0
    if tallest[2] > widest[1]:
        orientation = 1
    if tallest[2] * 1.5 > widest[1] and len(tall) > 0:
        orientation = 1
    dimensions = [int(1.5 * min_side), min_side]
    widest_tallest = [widest, tallest]
    if len(pix) < 2:
        error = input(
            "cannot be completed at present - too few pix. type 'y' to see error message, or 'n' to be politely turned down "
        )
        if error == "n":
            quit()
    print_complete = draw(
        pix.copy(), orientation, sprawlingest[1], widest_tallest, params, min_side, area
    )
    return print_complete


# return final folder with printing coordinates for each pic
def draw(pix, orientation, sprawlingest, widest_tallest, params, min_side, area):
    # determine which pic to add next
    def nextpic(pix, print_folder, min_side, border, orientation, aspect):
        for pic in pix:
            if (
                pic[1 + orientation]
                + print_folder[-1][1 + orientation]
                + print_folder[-1][3 + orientation]
                + border
                < min_side
            ):
                return pic
        return pix[0]

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
    border = int((area / len(pix))**0.5 * params[0])
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

    # add top and side borders
    top = int(params[1] * border / 5)
    side = int(params[2] * border / 5)

    # increase all coordinates in light of top/bottom and side borders
    for pic in print_folder:
        pic[3] += side
        pic[4] += top

    return (print_folder, (x + 2 * side, y + 2 * top))

if __name__ == "__main__":
    main(5)
