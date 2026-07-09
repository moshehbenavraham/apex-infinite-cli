import QtQuick

Rectangle {
    id: control

    property var bridge
    property var model: []
    property string currentValue: ""
    signal selected(string value)

    implicitWidth: rowLayout.implicitWidth + 4
    implicitHeight: 30
    radius: 3
    color: bridge.cellColor
    border.color: bridge.borderColor
    border.width: 1
    opacity: enabled ? 1.0 : 0.45

    Row {
        id: rowLayout
        anchors.centerIn: parent
        spacing: 2

        Repeater {
            model: control.model

            Rectangle {
                required property string modelData
                width: segLabel.implicitWidth + 20
                height: 24
                radius: 2
                color: modelData === control.currentValue
                    ? Qt.alpha(bridge.accentColor, 0.22)
                    : "transparent"
                border.color: modelData === control.currentValue
                    ? bridge.accentColor
                    : "transparent"
                border.width: 1

                Text {
                    id: segLabel
                    anchors.centerIn: parent
                    text: parent.modelData
                    color: parent.modelData === control.currentValue
                        ? bridge.accentColor
                        : bridge.mutedColor
                    font.family: bridge.fontFamily
                    font.pixelSize: Math.round(11 * bridge.fontScale)
                    font.capitalization: Font.AllUppercase
                    font.letterSpacing: 0.8
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: control.enabled
                        ? Qt.PointingHandCursor : Qt.ArrowCursor
                    onClicked: if (control.enabled) control.selected(parent.modelData)
                }
            }
        }
    }
}
