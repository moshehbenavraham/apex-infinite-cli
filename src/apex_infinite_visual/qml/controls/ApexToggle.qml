import QtQuick

Item {
    id: control

    property var bridge
    property string text: ""
    property bool checked: false
    signal toggled(bool value)

    implicitWidth: row.implicitWidth
    implicitHeight: 26
    opacity: enabled ? 1.0 : 0.45

    Row {
        id: row
        spacing: 8
        anchors.verticalCenter: parent.verticalCenter

        Rectangle {
            width: 34
            height: 16
            radius: 8
            anchors.verticalCenter: parent.verticalCenter
            color: control.checked
                ? Qt.alpha(bridge.accentColor, 0.35)
                : bridge.cellColor
            border.color: control.checked ? bridge.accentColor : bridge.borderColor
            border.width: 1

            Rectangle {
                width: 10
                height: 10
                radius: 5
                y: 3
                x: control.checked ? parent.width - width - 3 : 3
                color: control.checked ? bridge.accentColor : bridge.mutedColor
                Behavior on x { NumberAnimation { duration: 110 } }
            }
        }

        Text {
            text: control.text
            anchors.verticalCenter: parent.verticalCenter
            color: bridge.textColor
            font.family: bridge.fontFamily
            font.pixelSize: Math.round(12 * bridge.fontScale)
        }
    }

    MouseArea {
        anchors.fill: parent
        cursorShape: control.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
        onClicked: {
            if (!control.enabled)
                return
            control.checked = !control.checked
            control.toggled(control.checked)
        }
    }

    Accessible.role: Accessible.CheckBox
    Accessible.name: text
}
