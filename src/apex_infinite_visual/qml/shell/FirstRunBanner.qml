import QtQuick
import QtQuick.Layouts
import "../controls"

Rectangle {
    id: banner

    property var bridge
    property bool dismissed: false
    signal doctorRequested()

    visible: bridge.firstRunNeeded && !dismissed
    implicitHeight: visible ? row.implicitHeight + 20 : 0
    radius: 4
    color: Qt.alpha(bridge.warningColor, 0.08)
    border.color: bridge.warningColor
    border.width: 1

    RowLayout {
        id: row
        anchors.fill: parent
        anchors.margins: 10
        spacing: 12

        Text {
            text: "FIRST RUN"
            color: bridge.warningColor
            font.family: bridge.fontFamily
            font.pixelSize: Math.round(11 * bridge.fontScale)
            font.bold: true
            font.letterSpacing: 1.8
        }

        Text {
            text: "No shared config.yaml was found. Run Doctor to check "
                + "provider, Codex, and project readiness, then start with a "
                + "dry run. Create config.yaml from the packaged default "
                + "before a live run; the wrapper never writes shared CLI "
                + "config without explicit confirmation."
            color: bridge.textColor
            font.family: bridge.fontFamily
            font.pixelSize: Math.round(11 * bridge.fontScale)
            wrapMode: Text.Wrap
            Layout.fillWidth: true
        }

        ApexButton {
            bridge: banner.bridge
            text: "Doctor"
            primary: true
            onClicked: {
                bridge.runDoctor()
                banner.doctorRequested()
            }
        }

        ApexButton {
            bridge: banner.bridge
            text: "Dismiss"
            onClicked: banner.dismissed = true
        }
    }
}
