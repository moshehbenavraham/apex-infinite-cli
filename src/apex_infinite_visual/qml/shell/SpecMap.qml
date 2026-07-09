import QtQuick
import QtQuick.Layouts
import "../controls"

Rectangle {
    id: specMap

    property var bridge

    radius: 4
    color: bridge.panelColor
    border.color: bridge.borderColor
    border.width: 1
    implicitHeight: column.implicitHeight + 20

    ColumnLayout {
        id: column
        anchors.fill: parent
        anchors.margins: 10
        spacing: 6

        Text {
            text: "SPEC MAP"
            color: bridge.mutedColor
            font.family: bridge.fontFamily
            font.pixelSize: Math.round(10 * bridge.fontScale)
            font.letterSpacing: 2.0
        }

        ApexStatusCell {
            bridge: specMap.bridge
            labelText: "Spec system"
            valueText: bridge.specDetected ? "Detected" : "Not detected"
            accent: bridge.specDetected ? bridge.accentColor : bridge.mutedColor
            Layout.fillWidth: true
        }

        ApexStatusCell {
            bridge: specMap.bridge
            labelText: "Phase"
            valueText: bridge.specPhase
            accent: bridge.textColor
            Layout.fillWidth: true
        }

        ApexStatusCell {
            bridge: specMap.bridge
            labelText: "Session"
            valueText: bridge.specSession
            accent: bridge.textColor
            Layout.fillWidth: true
        }

        ApexStatusCell {
            bridge: specMap.bridge
            labelText: "Command"
            valueText: bridge.specCommand
            Layout.fillWidth: true
        }

        Text {
            text: "TASKS  " + bridge.taskProgressText
            color: bridge.mutedColor
            font.family: bridge.fontFamily
            font.pixelSize: Math.round(10 * bridge.fontScale)
            font.letterSpacing: 1.4
        }

        Rectangle {
            Layout.fillWidth: true
            implicitHeight: 6
            radius: 3
            color: bridge.cellColor
            border.color: bridge.borderColor
            border.width: 1

            Rectangle {
                width: Math.max(0, (parent.width - 2) * bridge.taskProgressRatio)
                height: parent.height - 2
                x: 1
                y: 1
                radius: 2
                color: bridge.accentColor

                Behavior on width { NumberAnimation { duration: 350 } }
            }
        }
    }
}
