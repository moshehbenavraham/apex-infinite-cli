import QtQuick
import QtQuick.Layouts
import "../controls"

Rectangle {
    id: rail

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
                text: "MISSION STATE"
                color: bridge.mutedColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(10 * bridge.fontScale)
                font.letterSpacing: 2.0
            }

            ApexStatusCell {
                bridge: rail.bridge
                labelText: "Status"
                valueText: bridge.statusText
                accent: bridge.hasError ? bridge.errorColor : bridge.accentColor
                charged: bridge.running
                Layout.fillWidth: true
            }

            ApexStatusCell {
                bridge: rail.bridge
                labelText: "Stage"
                valueText: bridge.stageText
                accent: bridge.warningColor
                Layout.fillWidth: true
            }

            ApexStatusCell {
                bridge: rail.bridge
                labelText: "Iteration"
                valueText: bridge.iterationText
                Layout.fillWidth: true
            }

            ApexStatusCell {
                bridge: rail.bridge
                labelText: "Provider"
                valueText: bridge.providerName
                Layout.fillWidth: true
            }

            ApexStatusCell {
                bridge: rail.bridge
                labelText: "Model"
                valueText: bridge.modelName
                Layout.fillWidth: true
            }

            ApexStatusCell {
                bridge: rail.bridge
                labelText: "Config"
                valueText: bridge.configSource
                accent: bridge.textColor
                Layout.fillWidth: true
            }

            ApexStatusCell {
                bridge: rail.bridge
                labelText: "Codex flags"
                valueText: bridge.codexFlagsText
                accent: bridge.codexFlagsText === "Incompatible"
                    ? bridge.errorColor : bridge.textColor
                Layout.fillWidth: true
            }

            ApexStatusCell {
                bridge: rail.bridge
                labelText: "Event stream"
                valueText: bridge.eventStreamMode
                accent: bridge.textColor
                Layout.fillWidth: true
            }

            ApexStatusCell {
                bridge: rail.bridge
                labelText: "History DB"
                valueText: bridge.historyDbText
                accent: bridge.textColor
                Layout.fillWidth: true
            }

            Text {
                text: "DECISION"
                color: bridge.mutedColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(10 * bridge.fontScale)
                font.letterSpacing: 2.0
                Layout.topMargin: 6
            }

            Rectangle {
                Layout.fillWidth: true
                implicitHeight: decisionColumn.implicitHeight + 16
                radius: 3
                color: bridge.cellColor
                border.color: bridge.borderColor
                border.width: 1

                ColumnLayout {
                    id: decisionColumn
                    anchors.fill: parent
                    anchors.margins: 8
                    spacing: 3

                    Text {
                        text: bridge.managerOutput
                        color: bridge.accentColor
                        font.family: bridge.fontFamily
                        font.pixelSize: Math.round(13 * bridge.fontScale)
                        font.bold: true
                        wrapMode: Text.Wrap
                        Layout.fillWidth: true
                    }

                    Text {
                        visible: bridge.managerReason.length > 0
                        text: bridge.managerReason
                        color: bridge.mutedColor
                        font.family: bridge.fontFamily
                        font.pixelSize: Math.round(11 * bridge.fontScale)
                        wrapMode: Text.Wrap
                        maximumLineCount: 3
                        elide: Text.ElideRight
                        Layout.fillWidth: true
                    }
                }
            }
        }
    }
}
