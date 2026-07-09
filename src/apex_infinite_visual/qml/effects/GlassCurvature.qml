import QtQuick

Canvas {
    id: glass

    property var bridge
    property real strength: bridge && bridge.curvatureEnabled
        ? bridge.effectOpacity : 0.0

    visible: strength > 0
    onStrengthChanged: requestPaint()
    onWidthChanged: requestPaint()
    onHeightChanged: requestPaint()

    onPaint: {
        var ctx = getContext("2d")
        ctx.clearRect(0, 0, width, height)
        if (strength <= 0)
            return
        var gradient = ctx.createRadialGradient(
            width / 2, height / 2, Math.min(width, height) * 0.42,
            width / 2, height / 2, Math.max(width, height) * 0.78)
        gradient.addColorStop(0, "rgba(0,0,0,0)")
        gradient.addColorStop(1, "rgba(0,0,0," + (0.16 + strength * 0.22) + ")")
        ctx.fillStyle = gradient
        ctx.fillRect(0, 0, width, height)
    }
}
