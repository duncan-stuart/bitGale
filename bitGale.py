import os

from PIL import Image


def open_image():
    '''
    Prompt user for directory, open image file (if found) and return as an array
    Directory for testing: D:\PyCharm\Projects\bitGale\testImg.jpg
    '''
    imgReadOK = False
    while not imgReadOK:
        try:
            # imgDir = input("Path location of image to open:")  # Commented out for testing purposes
            imgDir = 'D:\\PyCharm\\Projects\\bitGale\\testImg.jpg'
            userImg = Image.open(imgDir)
            imgReadOK = True
        except IOError:
            print("File not found!")
    return userImg


def make_pixel_array(img):
    # Convert PIL image object to list of tuples in the form [(R, G, B)]
    rawPixels = list(img.getdata())
    width, height = img.size

    # Make image into array (this just puts each row of pixels into a sublist)
    imgAsArray = [rawPixels[i * width:(i + 1) * width] for i in range(height)]

    # Convert pixels to lists for edibility
    for y in range(len(imgAsArray)):
        for x in range(len(imgAsArray[y])):
            imgAsArray[y][x] = list(imgAsArray[y][x])

    return imgAsArray


def pixel_sort(image, mode='c'):
    '''
    Pixelsorting effect taking an image array, and the mode. Uses variation on merge sort algorithm
    Inputs: image - image array | mode - either sort by 'R', 'G', 'B' or 'C' (for combined average)
            direction - either 'up', 'down', 'left, 'right'
    '''
    # todo direction (lowest-highest, up/down, etc)

    # Function definitions for merge sort
    def merge(left, right, index):
        result = []
        l = 0  # pointer to the left list
        r = 0  # pointer to the right list
        while l < len(left) and r < len(right):
            # Sort based on average of RGB values
            if index == 3:
                avgR = (left[l][0] + left[l][1] + left[l][2]) / 2
                avgL = (right[r][0] + right[r][1] + right[r][2]) / 2
                if avgR <= avgL:
                    result.append(left[l])
                    l += 1
                else:
                    result.append(right[r])
                    r += 1
            # Sort based on R(0), G(1), or B(2)
            else:
                if left[l][index] <= right[r][index]:
                    result.append(left[l])
                    l += 1
                else:
                    result.append(right[r])
                    r += 1
        result += left[l:]
        result += right[r:]
        return result

    def merge_sort(list, index):
        if len(list) in [1, 0]:
            return list

        mid = len(list) // 2
        left = merge_sort(list[:mid], index)
        right = merge_sort(list[mid:], index)
        return merge(left, right, index)

    # 3 is not handled as an index, but is looked for as a special mode in merge()
    index = 0 if mode == 'r' else 1 if mode == 'g' else 2 if mode == 'b' else 3

    # Sort each row lowest->highest
    sortedImage = []
    for row in image:
        sortedImage.append(merge_sort(row, index))
    return sortedImage


def rgb_offset(array, mode):
    # Interpret mode input as the index to operate on in each pixel
    channel = 0 if mode == 'r' else 1 if mode == 'g' else 2 if mode == 'b' else 0

    # Take the first pixel value, and bubble it through all rows to the end of the image (shifting all values one left)
    for y in range(len(array)):
        firstPixel = array[y][0]
        for x in range(len(array[y])):
            array[y][x][channel], firstPixel[channel] = firstPixel[channel], array[y][x][channel]
        if y == len(array):  #
            array[y][len(array[y])-1][channel], array[y+1][0][channel] = array[y+1][0][channel], array[y][len(array[y])-1][channel]
    return array


def make_pil_image(array):
    # Get (width, height) of array as a tuple
    size = (len(array[0]), len(array))

    # Create blank PIL image object with width, height of array
    outputImg = Image.new('RGB', size)

    # Convert pixels to tuples so that they can be read by PIL
    for y in range(len(array)):
        for x in range(len(array[y])):
            array[y][x] = tuple(array[y][x])

    # Put values from array into new image object
    for y in range(outputImg.size[1]):
        for x in range(outputImg.size[0]):
            outputImg.putpixel((x, y), array[y][x])
    outputImg.show()  # For testing
    return outputImg


def save_image(img):
    # Get path to save to from user and verify it
    pathFileOK = False
    while not pathFileOK:
        # Get save path and name from user
        path = input("Path location of image to save into: (in form: .../directory/directory/)\nq to quit")
        fileName = input("File name: (as filename.filetype")

        # Quit check
        if path == 'q':
            return None

        # Check if path/file exist. If yes, ask if OK to overwrite. If only path, continue. If neither, ask to make path
        if os.path.exists(path) and not os.path.exists(path + fileName):  # Directory exists, and no file with name
            pathFileOK = True

        elif os.path.exists(path) and os.path.exists(path + fileName):  # Directory exists, file with name exists
            overwrite = input("File already exists, OK to overwrite? (y/n)")
            while overwrite not in ['y', 'n']:
                overwrite = input("Not valid input! OK to overwrite? (y/n)")
            pathFileOK = True if overwrite == 'y' else False

        else:  # Directory doesnt exist
            makeDir = input("Directory doesnt exist, would you like to create it? (y/n)")
            while makeDir not in ['y', 'n']:
                makeDir = input("Not valid input! Create directory? (y/n)")
            pathFileOK = True if makeDir == 'y' else False

    img.save(path+fileName)
    # TODO protect against no backslash at end of path and forwardslash vs backslash


def main():
    # Testing space ... for now!
    #userImage = open_image()
    #print(userImage[0])
    #userImageSorted = pixel_sort(userImage, 'G')
    #print(userImageSorted[0])

    userImage = open_image()
    userImageArray = make_pixel_array(userImage)

    userImageArray = rgb_offset(rgb_offset(userImageArray, 'r', 45), 'r', 45)
    #userImageArraySorted = pixel_sort(userImageArray)
    save_image(make_pil_image(userImageArray))


main()
