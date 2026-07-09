import QtQuick

Rectangle {
    id: frame

    property var bridge
    property color frameAccent: {
        if (!bridge)
            return "#263c34"
        if (bridge.runHealth === "failed")
            return bridge.errorColor
        if (bridge.runHealth === "complete")
            return bridge.accentColor
        if (bridge.runHealth === "running")
            return bridge.accentColor
        return bridge.borderColor
    }

    visible: bridge && bridge.ambientFrameEnabled
    color: "transparent"
    border.color: frameAccent
    border.width: 1
    radius: 6
    opacity: bridge ? 0.35 + bridge.effectOpacity * 0.4 : 0.0

    Behavior on frameAccent { ColorAnimation { duration: 400 } }

    Rectangle {
        anchors.fill: parent
        anchors.margins: 2
        color: "transparent"
        border.color: frame.frameAccent
        border.width: 1
        radius: 5
        opacity: 0.25
    }
}
