import QtQuick
import QtQuick.Layouts
import "../controls"

Rectangle {
    id: panel

    property var bridge

    radius: 4
    color: bridge.panelColor
    border.color: bridge.borderColor
    border.width: 1

    Flickable {
        anchors.fill: parent
        anchors.margins: 10
        contentWidth: width
        contentHeight: column.implicitHeight
        clip: true

        ColumnLayout {
            id: column
            width: parent.width
            spacing: 6

            Text {
                text: "SIGNAL"
                color: bridge.mutedColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(10 * bridge.fontScale)
                font.letterSpacing: 2.0
            }

            ApexStatusCell {
                bridge: panel.bridge
                labelText: "Provider health"
                valueText: bridge.providerHealth
                accent: bridge.providerHealth === "ok"
                    ? bridge.accentColor
                    : bridge.providerHealth === "failed"
                        ? bridge.errorColor : bridge.mutedColor
                Layout.fillWidth: true
            }

            ApexStatusCell {
                bridge: panel.bridge
                labelText: "Runtime"
                valueText: bridge.durationText
                accent: bridge.textColor
                Layout.fillWidth: true
            }

            ApexStatusCell {
                bridge: panel.bridge
                labelText: "Stderr events"
                valueText: bridge.stderrEvents.toString()
                accent: bridge.stderrEvents > 0
                    ? bridge.warningColor : bridge.textColor
                Layout.fillWidth: true
            }

            ApexStatusCell {
                bridge: panel.bridge
                labelText: "Malformed events"
                valueText: bridge.malformedEvents.toString()
                accent: bridge.malformedEvents > 0
                    ? bridge.warningColor : bridge.textColor
                Layout.fillWidth: true
            }

            ApexStatusCell {
                bridge: panel.bridge
                labelText: "Last event"
                valueText: bridge.lastEvent
                accent: bridge.textColor
                Layout.fillWidth: true
            }

            Text {
                visible: bridge.artifacts.length > 0
                text: "ARTIFACTS"
                color: bridge.mutedColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(10 * bridge.fontScale)
                font.letterSpacing: 2.0
                Layout.topMargin: 4
            }

            Repeater {
                model: bridge.artifacts

                Text {
                    required property string modelData
                    text: "- " + modelData
                    color: bridge.accentColor
                    font.family: bridge.fontFamily
                    font.pixelSize: Math.round(11 * bridge.fontScale)
                    elide: Text.ElideMiddle
                    Layout.fillWidth: true
                }
            }
        }
    }
}
