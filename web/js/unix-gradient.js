function UnixGradient () {

    const timeStart = 0;
    const timeEnd = 281474943156225;
    const totalRgbColors = 16777215;

    let time = timeStart;
    let color1 = [0, 0, 0];
    let color2 = [0, 0, 0];

    const getTime = function () {
        return time;
    };

    const setTime = function (newTime) {
        time = newTime;
        if (time >= timeEnd) {
            setColor1([255,255,255]);
            setColor2([255,255,255]);
        } else if (time > totalRgbColors) {
            setColor1(getRgbColorFromDecimalNumber(Math.floor(time / totalRgbColors)));
            setColor2(getRgbColorFromDecimalNumber((time - (Math.floor(time / totalRgbColors) * totalRgbColors)) - 1));
        } else {
            setColor2(getRgbColorFromDecimalNumber(time));
        }
    };

    const getColor1 = function () {
        return color1;
    };

    const setColor1 = function (newColor) {
        color1 = newColor;
    };

    const getColor2 = function () {
        return color2;
    };

    const setColor2 = function (newColor) {
        color2 = newColor;
    };

    const getRgbColorFromDecimalNumber = function (decimalNumber) {
        let r = 0;
        let g = 0;
        let b = decimalNumber;
        if (b > 255) {
            g = Math.floor(decimalNumber / 256);
            b = decimalNumber - (g * 256);
        }
        if (g > 255) {
            r = Math.floor((decimalNumber / 256) / 256);
            g = g - (r * 256);
        }
        return [r, g, b];
    };

    return {
        getTime: getTime,
        setTime: setTime,
        getColor1: getColor1,
        getColor2: getColor2
    };
}
