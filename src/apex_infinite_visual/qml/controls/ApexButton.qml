import QtQuick

Rectangle {
    id: control

    property var bridge
    property string text: ""
    property bool primary: false
    property bool danger: false
    signal clicked()

    property color accent: danger ? bridge.errorColor : bridge.accentColor

    implicitWidth: label.implicitWidth + 28
    implicitHeight: 34
    radius: 3
    color: primary && enabled ? Qt.alpha(accent, 0.16) : bridge.cellColor
    border.color: enabled ? accent : bridge.borderColor
    border.width: 1
    opacity: enabled ? 1.0 : 0.45

    Rectangle {
        anchors.fill: parent
        radius: parent.radius
        color: control.accent
        opacity: mouse.pressed && control.enabled
            ? 0.22
            : (mouse.containsMouse && control.enabled ? 0.10 : 0.0)
        Behavior on opacity { NumberAnimation { duration: 90 } }
    }

    Text {
        id: label
        anchors.centerIn: parent
        text: control.text
        color: control.enabled ? control.accent : bridge.mutedColor
        font.family: bridge.fontFamily
        font.pixelSize: Math.round(13 * bridge.fontScale)
        font.bold: control.primary
        font.capitalization: Font.AllUppercase
        font.letterSpacing: 1.2
    }

    MouseArea {
        id: mouse
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: control.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
        onClicked: if (control.enabled) control.clicked()
    }
}
