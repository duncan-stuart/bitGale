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
            #imgDir = input("Path location of image to open:")  # Commented out for testing purposes
            imgDir = 'D:\\PyCharm\\Projects\\bitGale\\testImg.jpg'
            userImg = Image.open(imgDir)
            imgReadOK = True
        except IOError:
            print("File not found!")
    return userImg


def make_pixel_array(PILimg):
    img = make_thumb(PILimg)

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


def make_thumb(img):
    width, height = img.size

    # If the image area exceeds 1920*1080
    if width * height > 2073600:
        print(" *** You have opened a larger than HD image. Operations will be preformed on a downsized copy to make\n"
              "the program run faster in use, and then applied to the full-size image when saving. Saving will\n"
              "therefore take a while!\n")

        # Determine if the height and/or width is excessively large
        heightTooBig = True if height > 1080 else False
        widthTooBig = True if width > 1920 else False

        # Get the percent by which to scale the thumbnail so that the thumb does not exceed 1920 by 1080
        resizePercent = 1080 / height if heightTooBig else 1920 / width if widthTooBig else 1

        # Get the new (width, height) as a tuple
        newSize = (int(resizePercent * width), int(resizePercent * height))

        # Resize the image
        return img.resize(newSize)
    return img


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


def parse(rawInput, validFlags):
    # Parse raw input into a dictionary with flags as keys
    params = rawInput.strip().split('-')
    if '' in params:
        params.remove('')
    flags = {}
    for argument in params:
        argument = argument.strip().split()
        try:  # Protect against commands with flags but no associated value
            flags[argument[0]] = argument[1]
        except IndexError:
            print("*** One flag or value given without the other")
            return 'invalid'

    # Check if only valid flags have been specified
    for f in flags:
        if f not in validFlags:
            print('Invalid parameters, returning to shell.')
            return 'invalid'
    return flags


def rotate_image(array, flags):
    # Interpret flags, default to 90 degree rotate right
    angle = flags['ang'] if 'ang' in flags else '90'

    rotatedImage = []
    if angle == '90':
        # Run through each column of the image, starting at the leftmost column
        for x in range(len(array[0])):
            # Create a new row in the rotated image
            rotatedImage.append([])
            # Starting at the bottommost row, add every pixel in the columns to the row in the rotated image
            for y in range(len(array) -1, 0, -1):
                rotatedImage[x].append(array[y][x])
    elif angle == '180':
        # Run through the rows of the image, starting from the bottom, and add them to the rotated image
        for row in range(len(array)-1, 0, -1):
            rotatedImage.append(array[row])
    elif angle == '270':
        # Run through each column of the image, starting at the rightmost column
        xRotatedImage = 0  # Counter that increments the row being adding to with every column being run through
        for x in range(len(array[0]) - 1, 0, -1):
            # Create a new row in the rotated image
            rotatedImage.append([])
            # Starting at the topmost row, add every pixel in the columns to the row in the rotated image
            for y in range(len(array)):
                rotatedImage[xRotatedImage].append(array[y][x])
            xRotatedImage += 1
    else:
        print("*** Not a right angle, returning to shell.")
    return rotatedImage


def show_help(params):
    # Default to general help file if no flag is given
    fileName = params['eff'] if 'eff' in params else 'general'

    # Get the absolute path of the file
    projectPath = os.path.dirname(__file__)
    absolutePath = os.path.join(projectPath, 'helpdocs', fileName + '.txt')

    # Display help
    with open(absolutePath) as helpFile:
        print(helpFile.read())
