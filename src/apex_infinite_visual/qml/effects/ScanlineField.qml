import QtQuick

Canvas {
    id: field

    property var bridge
    property string mode: bridge ? bridge.effectiveRenderingMode : "modern-crisp"
    property real intensity: bridge ? bridge.effectOpacity : 0.0

    visible: bridge && bridge.scanlinesEnabled && intensity > 0
    onModeChanged: requestPaint()
    onIntensityChanged: requestPaint()
    onWidthChanged: requestPaint()
    onHeightChanged: requestPaint()

    onPaint: {
        var ctx = getContext("2d")
        ctx.clearRect(0, 0, width, height)
        if (!visible)
            return
        var alpha = 0.05 + intensity * 0.14
        ctx.fillStyle = Qt.rgba(0, 0, 0, alpha)
        var y
        var x
        if (mode === "pixel-grid") {
            for (y = 0; y < height; y += 4)
                ctx.fillRect(0, y, width, 1)
            for (x = 0; x < width; x += 4)
                ctx.fillRect(x, 0, 1, height)
        } else if (mode === "subpixel") {
            for (x = 0; x < width; x += 3)
                ctx.fillRect(x, 0, 1, height)
        } else {
            for (y = 0; y < height; y += 4)
                ctx.fillRect(0, y, width, 1.4)
        }
    }
}
