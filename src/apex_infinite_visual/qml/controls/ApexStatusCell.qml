import QtQuick
import QtQuick.Layouts

Rectangle {
    id: cell

    property var bridge
    property string labelText: ""
    property string valueText: ""
    property color accent: bridge.accentColor
    property bool charged: false

    implicitHeight: 52
    radius: 3
    color: bridge.cellColor
    border.color: charged ? accent : bridge.borderColor
    border.width: 1

    Rectangle {
        width: 3
        height: parent.height - 8
        y: 4
        x: 0
        radius: 1
        color: cell.accent
        opacity: 0.85
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 8
        anchors.topMargin: 7
        anchors.bottomMargin: 7
        spacing: 2

        Text {
            text: cell.labelText
            color: bridge.mutedColor
            font.family: bridge.fontFamily
            font.pixelSize: Math.round(10 * bridge.fontScale)
            font.capitalization: Font.AllUppercase
            font.letterSpacing: 1.4
            elide: Text.ElideRight
            Layout.fillWidth: true
        }

        Text {
            text: cell.valueText
            color: cell.accent
            font.family: bridge.fontFamily
            font.pixelSize: Math.round(14 * bridge.fontScale)
            font.bold: true
            elide: Text.ElideRight
            Layout.fillWidth: true
        }
    }
}
