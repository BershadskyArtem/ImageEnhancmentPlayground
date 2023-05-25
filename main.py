import cv2
import numpy as np
import pywt
import Wavelets

# last - 1.35
# last - 1 1.35
# last - 2 1.35
sharpenCoefficients = [1.5, 1.2, 1.5, 1.2]
denoisingThresholds = [0.0, 10.0, 3.0, 6.0]
denoisingMultiplier = 1.0
clarityMultiplier = 1.0
sharpenMultiplier = 1.0

thrname = 'garrote'


def garotte(data, thr):
    height, width = data.shape[:2]
    for y in range(0, height):
        for x in range(0,width):
            newval = data[y][x] * (1 - (thr * thr / data[y][x] * data[y][x]))
            if abs(data[y][x]) <= thr or data[y][x] == 0:
                newval = 0
            data[y][x] = newval
    return data

def sharpen(coefficients):
    for i in range(1, len(coefficients)):
        v = coefficients[i][0]
        h = coefficients[i][1]
        vh = coefficients[i][2]
        #denoisingThreshold = denoisingThresholds[len(denoisingThresholds) - i]

        print(np.min(v))
        print(np.max(v))
        print(np.mean(v))

        denoisingThreshold = abs(np.min(v)) + abs(np.max(v))
        denoisingThreshold *= 0.01
        denoisingThreshold *= denoisingMultiplier

        print(denoisingThreshold)
        #v = v * 0.0 + pywt.threshold(v, denoisingThreshold, thrname)
        #h = h * 0.0 + pywt.threshold(h, denoisingThreshold, thrname)
        #vh = vh * 0.0 + pywt.threshold(vh, denoisingThreshold, thrname)
        v = garotte(v, denoisingThreshold)
        h = garotte(h, denoisingThreshold)
        vh = garotte(vh, denoisingThreshold)
        #coefficients[i][0] = v
        #coefficients[i][1] = h
        #coefficients[i][2] = vh
        # sharpen
        v *= sharpenCoefficients[len(sharpenCoefficients) - i] * sharpenMultiplier
        h *= sharpenCoefficients[len(sharpenCoefficients) - i] * sharpenMultiplier
        vh *= sharpenCoefficients[len(sharpenCoefficients) - i] * sharpenMultiplier

        # coefficients[i][1] = coefficients[i][1] * sharpenCoefficients[i]
        # coefficients[i][2] = coefficients[i][2] * sharpenCoefficients[i]


if __name__ == '__main__':
    imageImportPath = 'C:\\Users\\Artyom\\SampleImage.jpeg'
    imageExportPath = 'C:\\Users\\Artyom\\EnhancedImage.jpeg'
    img = cv2.imread(imageImportPath)
    height, width = img.shape[:2]
    scaleFactor = 1
    height //= scaleFactor
    width //= scaleFactor
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    labImage = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    cv2.imshow('Initial image', img)
    (l, a, b) = cv2.split(labImage)

    coefficients = Wavelets.decompose(l, 'db8', 4)
    denoisingMultiplier = float(input("Denoising: "))
    #clarityMultiplier = float(input("Clarity: "))
    sharpenMultiplier = float(input("Sharpen: "))

    sharpen(coefficients)
    print('Sharpened')
    lmn = Wavelets.compose(coefficients, 'db8')
    l = lmn.astype(np.uint8)
    enhancedLabImage = cv2.merge([l, a, b])
    enhancedImage = cv2.cvtColor(enhancedLabImage, cv2.COLOR_LAB2BGR)
    cv2.imwrite(imageExportPath, enhancedImage)

    cv2.imshow('Enhanced image', enhancedImage)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
