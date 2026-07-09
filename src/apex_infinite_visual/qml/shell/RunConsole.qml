import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls"

Rectangle {
    id: console_

    property var bridge

    radius: 4
    color: bridge.panelAltColor
    border.color: bridge.hasError ? bridge.errorColor : bridge.borderColor
    border.width: 1

    TextEdit {
        id: clipboardHelper
        visible: false
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        RowLayout {
            Layout.fillWidth: true
            spacing: 8

            Text {
                text: "EVENT CORE"
                color: bridge.textColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(13 * bridge.fontScale)
                font.bold: true
                font.letterSpacing: 2.0
            }

            Item { Layout.fillWidth: true }

            ApexSegmentedControl {
                bridge: console_.bridge
                model: ["all", "info", "success", "warning", "error"]
                currentValue: bridge.severityFilter === ""
                    ? "all" : bridge.severityFilter
                onSelected: function(value) {
                    bridge.setSeverityFilter(value === "all" ? "" : value)
                }
            }

            TextField {
                id: searchField
                placeholderText: "Search"
                placeholderTextColor: bridge.mutedColor
                color: bridge.textColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(11 * bridge.fontScale)
                background: Rectangle {
                    color: bridge.cellColor
                    border.color: searchField.activeFocus
                        ? bridge.accentColor : bridge.borderColor
                    border.width: 1
                    radius: 3
                }
                Layout.preferredWidth: 150
                Accessible.name: "Search events"
                onTextEdited: bridge.setSearchText(text)
            }

            ApexButton {
                bridge: console_.bridge
                text: "Export"
                enabled: bridge.eventRows.length > 0
                Accessible.name: "Export events"
                onClicked: bridge.exportEvents(
                    "~/.local/state/apex-infinite/event-export.json")
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 1
            color: bridge.borderColor
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: bridge.hasError ? errorColumn.implicitHeight + 20 : 0
            visible: bridge.hasError
            radius: 3
            color: Qt.alpha(bridge.errorColor, 0.08)
            border.color: bridge.errorColor
            border.width: 1

            ColumnLayout {
                id: errorColumn
                anchors.fill: parent
                anchors.margins: 10
                spacing: 3

                Text {
                    text: bridge.statusText
                    color: bridge.errorColor
                    font.family: bridge.fontFamily
                    font.pixelSize: Math.round(14 * bridge.fontScale)
                    font.bold: true
                    elide: Text.ElideRight
                    Layout.fillWidth: true
                }

                Text {
                    text: bridge.errorText
                    color: bridge.textColor
                    font.family: bridge.fontFamily
                    font.pixelSize: Math.round(11 * bridge.fontScale)
                    wrapMode: Text.Wrap
                    maximumLineCount: 2
                    elide: Text.ElideRight
                    Layout.fillWidth: true
                }
            }
        }

        ListView {
            id: eventList
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: bridge.eventRows
            clip: true
            spacing: Math.round(4 * bridge.lineSpacing)
            boundsBehavior: Flickable.StopAtBounds
            reuseItems: true
            Accessible.name: "Event log"

            onCountChanged: if (atYEnd || count < 4) positionViewAtEnd()

            Text {
                visible: eventList.count === 0
                anchors.centerIn: parent
                text: bridge.running ? "Waiting for events" : "Offline"
                color: bridge.mutedColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(14 * bridge.fontScale)
            }

            delegate: Rectangle {
                required property var modelData
                width: eventList.width
                implicitHeight: rowLayout.implicitHeight + 12
                radius: 2
                color: modelData.severity === "error"
                    ? Qt.alpha(bridge.errorColor, 0.06)
                    : bridge.cellColor
                border.color: modelData.severity === "error"
                    ? Qt.alpha(bridge.errorColor, 0.5)
                    : "transparent"
                border.width: 1

                property color severityColor: modelData.severity === "error"
                    ? bridge.errorColor
                    : modelData.severity === "warning"
                        ? bridge.warningColor
                        : modelData.severity === "success"
                            ? bridge.accentColor
                            : bridge.mutedColor

                Rectangle {
                    width: 3
                    height: parent.height - 6
                    y: 3
                    radius: 1
                    color: parent.severityColor
                }

                RowLayout {
                    id: rowLayout
                    anchors.fill: parent
                    anchors.leftMargin: 12
                    anchors.rightMargin: 8
                    anchors.topMargin: 6
                    anchors.bottomMargin: 6
                    spacing: 10

                    Text {
                        text: modelData.sequence.toString().padStart(3, "0")
                        color: bridge.mutedColor
                        font.family: bridge.fontFamily
                        font.pixelSize: Math.round(10 * bridge.fontScale)
                    }

                    Rectangle {
                        implicitWidth: stageTag.implicitWidth + 12
                        implicitHeight: 16
                        radius: 2
                        color: "transparent"
                        border.color: severityColor
                        border.width: 1

                        Text {
                            id: stageTag
                            anchors.centerIn: parent
                            text: modelData.stage
                            color: severityColor
                            font.family: bridge.fontFamily
                            font.pixelSize: Math.round(9 * bridge.fontScale)
                            font.capitalization: Font.AllUppercase
                            font.letterSpacing: 1.0
                        }
                    }

                    ColumnLayout {
                        spacing: 1
                        Layout.fillWidth: true

                        Text {
                            text: modelData.title
                            color: bridge.textColor
                            font.family: bridge.fontFamily
                            font.pixelSize: Math.round(12 * bridge.fontScale)
                            font.bold: modelData.severity === "error"
                            elide: Text.ElideRight
                            Layout.fillWidth: true
                        }

                        Text {
                            visible: modelData.detail.length > 0
                            text: modelData.detail
                            color: bridge.mutedColor
                            font.family: bridge.fontFamily
                            font.pixelSize: Math.round(10 * bridge.fontScale)
                            elide: Text.ElideRight
                            Layout.fillWidth: true
                        }
                    }

                    Text {
                        visible: modelData.iteration >= 0
                        text: "it " + modelData.iteration
                        color: bridge.mutedColor
                        font.family: bridge.fontFamily
                        font.pixelSize: Math.round(9 * bridge.fontScale)
                    }

                    Text {
                        text: modelData.timestamp
                        color: bridge.mutedColor
                        font.family: bridge.fontFamily
                        font.pixelSize: Math.round(9 * bridge.fontScale)
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.RightButton
                    onClicked: {
                        clipboardHelper.text = modelData.title + " - "
                            + modelData.detail + " (" + modelData.event + ")"
                        clipboardHelper.selectAll()
                        clipboardHelper.copy()
                    }
                }
            }

            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AsNeeded
            }
        }
    }
}
