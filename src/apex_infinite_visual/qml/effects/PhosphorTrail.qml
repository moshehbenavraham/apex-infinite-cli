import QtQuick

Rectangle {
    id: trail

    property var bridge
    property color trailColor: bridge ? bridge.accentColor : "#6ee7a8"

    visible: bridge && bridge.persistenceEnabled
    color: trailColor
    opacity: 0.0
    radius: 4

    function pulse() {
        fade.restart()
    }

    function faultPulse() {
        trailColor = bridge.errorColor
        fade.restart()
        resetColor.restart()
    }

    SequentialAnimation {
        id: fade
        NumberAnimation {
            target: trail
            property: "opacity"
            to: bridge ? 0.05 + bridge.effectOpacity * 0.10 : 0.0
            duration: 110
            easing.type: Easing.OutQuad
        }
        NumberAnimation {
            target: trail
            property: "opacity"
            to: 0.0
            duration: 1600
            easing.type: Easing.InQuad
        }
    }

    Timer {
        id: resetColor
        interval: 1800
        onTriggered: trail.trailColor = Qt.binding(function() {
            return bridge ? bridge.accentColor : "#6ee7a8"
        })
    }
}
