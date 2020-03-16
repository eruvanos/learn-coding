import mustache from 'https://unpkg.com/mustache@latest/mustache.mjs';

var template = "{{#pixels}}\n<div style=\"display: flex; flex-direction: column; text-align: center;\">\n    <virtual-rgb-led color=\"{{color}}\"></virtual-rgb-led>\n    <span style=\"color: white; font-size: x-small; margin-top: 2px\">{{index}}</span>\n</div>\n{{/pixels}}\n";

class VirtualRgbLed extends HTMLElement {
    constructor() {
        super();
        const color = this.getAttribute('color');
        this.style=`color:${color}`;
        this.innerHTML = `<div></div>`;
    }
}

customElements.define('virtual-rgb-led', VirtualRgbLed);

class VirtualLightstrip extends HTMLElement {
    //https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements

    constructor() {
        super();
        this.__templateArgs = {};
        this.pixels = [];
    }

    begin() {

    }

    updateLength(numPixels) {
        this.pixels = [];
        for (var i = 0; i < numPixels; i++) {
            this.pixels.push({color: 'rgb(0,0,0)', index: i});
        }
    }

    show() {
        this.__templateArgs.pixels = this.pixels;
        this.innerHTML = mustache.render(template, this.__templateArgs);
    }

    setPixelColor(nLed, red_or_color, green = undefined, blue = undefined, white = undefined) {
        if (!isNaN(red_or_color)) {
            this.pixels[nLed].value = `rgb(${red_or_color || 0}, ${green || 0}, ${blue || 0})`;
            this.pixels[nLed].color = `rgb(${red_or_color || 0}, ${green || 0}, ${blue || 0})`;
        } else if (typeof red_or_color === 'string') {
            this.pixels[nLed].value = red_or_color;
            this.pixels[nLed].color = COLORS[red_or_color] || red_or_color;
        }
    }

    fill(red_or_color, green = undefined, blue = undefined, white = undefined) {
        for (var i = 0; i < this.pixels.length; i++) {
            this.setPixelColor(i, red_or_color, green, blue, white);
        }
    }

    getPixelColor(nLed) {
        return this.pixels[nLed].value
    }

    setBrightness() {

    }

    getBrightness() {

    }

    clear() {
        this.fill('BLACK');
    }

    length() {
        return this.pixels.length;
    }

}

const COLORS = {
    "ALICEBLUE": "#F0F8FF",
    "ANTIQUEWHITE": "#FAEBD7",
    "AQUA": "#00FFFF",
    "AQUAMARINE": "#7FFFD4",
    "AZURE": "#F0FFFF",
    "BEIGE": "#F5F5DC",
    "BISQUE": "#FFE4C4",
    "BLACK": "#000000",
    "BLANCHEDALMOND": "#FFEBCD",
    "BLUE": "#0000FF",
    "BLUEVIOLET": "#8A2BE2",
    "BROWN": "#A52A2A",
    "BURLYWOOD": "#DEB887",
    "CADETBLUE": "#5F9EA0",
    "CHARTREUSE": "#7FFF00",
    "CHOCOLATE": "#D2691E",
    "CORAL": "#FF7F50",
    "CORNFLOWERBLUE": "#6495ED",
    "CORNSILK": "#FFF8DC",
    "CRIMSON": "#DC143C",
    "CYAN": "#00FFFF",
    "DARKBLUE": "#00008B",
    "DARKCYAN": "#008B8B",
    "DARKGOLDENROD": "#B8860B",
    "DARKGRAY": "#A9A9A9",
    "DARKGREY": "#A9A9A9",
    "DARKGREEN": "#006400",
    "DARKKHAKI": "#BDB76B",
    "DARKMAGENTA": "#8B008B",
    "DARKOLIVEGREEN": "#556B2F",
    "DARKORANGE": "#FF8C00",
    "DARKORCHID": "#9932CC",
    "DARKRED": "#8B0000",
    "DARKSALMON": "#E9967A",
    "DARKSEAGREEN": "#8FBC8F",
    "DARKSLATEBLUE": "#483D8B",
    "DARKSLATEGRAY": "#2F4F4F",
    "DARKSLATEGREY": "#2F4F4F",
    "DARKTURQUOISE": "#00CED1",
    "DARKVIOLET": "#9400D3",
    "DEEPPINK": "#FF1493",
    "DEEPSKYBLUE": "#00BFFF",
    "DIMGRAY": "#696969",
    "DIMGREY": "#696969",
    "DODGERBLUE": "#1E90FF",
    "FIREBRICK": "#B22222",
    "FLORALWHITE": "#FFFAF0",
    "FORESTGREEN": "#228B22",
    "FUCHSIA": "#FF00FF",
    "GAINSBORO": "#DCDCDC",
    "GHOSTWHITE": "#F8F8FF",
    "GOLD": "#FFD700",
    "GOLDENROD": "#DAA520",
    "GRAY": "#808080",
    "GREY": "#808080",
    "GREEN": "#008000",
    "GREENYELLOW": "#ADFF2F",
    "HONEYDEW": "#F0FFF0",
    "HOTPINK": "#FF69B4",
    "INDIANRED": "#CD5C5C",
    "INDIGO": "#4B0082",
    "IVORY": "#FFFFF0",
    "KHAKI": "#F0E68C",
    "LAVENDER": "#E6E6FA",
    "LAVENDERBLUSH": "#FFF0F5",
    "LAWNGREEN": "#7CFC00",
    "LEMONCHIFFON": "#FFFACD",
    "LIGHTBLUE": "#ADD8E6",
    "LIGHTCORAL": "#F08080",
    "LIGHTCYAN": "#E0FFFF",
    "LIGHTGOLDENRODYELLOW": "#FAFAD2",
    "LIGHTGRAY": "#D3D3D3",
    "LIGHTGREY": "#D3D3D3",
    "LIGHTGREEN": "#90EE90",
    "LIGHTPINK": "#FFB6C1",
    "LIGHTSALMON": "#FFA07A",
    "LIGHTSEAGREEN": "#20B2AA",
    "LIGHTSKYBLUE": "#87CEFA",
    "LIGHTSLATEGRAY": "#778899",
    "LIGHTSLATEGREY": "#778899",
    "LIGHTSTEELBLUE": "#B0C4DE",
    "LIGHTYELLOW": "#FFFFE0",
    "LIME": "#00FF00",
    "LIMEGREEN": "#32CD32",
    "LINEN": "#FAF0E6",
    "MAGENTA": "#FF00FF",
    "MAROON": "#800000",
    "MEDIUMAQUAMARINE": "#66CDAA",
    "MEDIUMBLUE": "#0000CD",
    "MEDIUMORCHID": "#BA55D3",
    "MEDIUMPURPLE": "#9370DB",
    "MEDIUMSEAGREEN": "#3CB371",
    "MEDIUMSLATEBLUE": "#7B68EE",
    "MEDIUMSPRINGGREEN": "#00FA9A",
    "MEDIUMTURQUOISE": "#48D1CC",
    "MEDIUMVIOLETRED": "#C71585",
    "MIDNIGHTBLUE": "#191970",
    "MINTCREAM": "#F5FFFA",
    "MISTYROSE": "#FFE4E1",
    "MOCCASIN": "#FFE4B5",
    "NAVAJOWHITE": "#FFDEAD",
    "NAVY": "#000080",
    "OLDLACE": "#FDF5E6",
    "OLIVE": "#808000",
    "OLIVEDRAB": "#6B8E23",
    "ORANGE": "#FFA500",
    "ORANGERED": "#FF4500",
    "ORCHID": "#DA70D6",
    "PALEGOLDENROD": "#EEE8AA",
    "PALEGREEN": "#98FB98",
    "PALETURQUOISE": "#AFEEEE",
    "PALEVIOLETRED": "#DB7093",
    "PAPAYAWHIP": "#FFEFD5",
    "PEACHPUFF": "#FFDAB9",
    "PERU": "#CD853F",
    "PINK": "#FFC0CB",
    "PLUM": "#DDA0DD",
    "POWDERBLUE": "#B0E0E6",
    "PURPLE": "#800080",
    "REBECCAPURPLE": "#663399",
    "RED": "#FF0000",
    "ROSYBROWN": "#BC8F8F",
    "ROYALBLUE": "#4169E1",
    "SADDLEBROWN": "#8B4513",
    "SALMON": "#FA8072",
    "SANDYBROWN": "#F4A460",
    "SEAGREEN": "#2E8B57",
    "SEASHELL": "#FFF5EE",
    "SIENNA": "#A0522D",
    "SILVER": "#C0C0C0",
    "SKYBLUE": "#87CEEB",
    "SLATEBLUE": "#6A5ACD",
    "SLATEGRAY": "#708090",
    "SLATEGREY": "#708090",
    "SNOW": "#FFFAFA",
    "SPRINGGREEN": "#00FF7F",
    "STEELBLUE": "#4682B4",
    "TAN": "#D2B48C",
    "TEAL": "#008080",
    "THISTLE": "#D8BFD8",
    "TOMATO": "#FF6347",
    "TURQUOISE": "#40E0D0",
    "VIOLET": "#EE82EE",
    "WHEAT": "#F5DEB3",
    "WHITE": "#FFFFFF",
    "WHITESMOKE": "#F5F5F5",
    "YELLOW": "#FFFF00",
    "YELLOWGREEN": "#9ACD32",
};

const VirtualLightstripTag = 'virtual-lightstrip';

customElements.define(VirtualLightstripTag, VirtualLightstrip);

export default VirtualLightstrip;
export { VirtualLightstripTag };