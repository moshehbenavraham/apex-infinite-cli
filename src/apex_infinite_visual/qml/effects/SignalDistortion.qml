import QtQuick

Item {
    id: distortion

    property var bridge
    property bool faultLocked: false

    // Flicker: brief whole-surface brightness ripple.
    Rectangle {
        anchors.fill: parent
        visible: bridge && bridge.flickerEnabled
        color: "#ffffff"
        opacity: 0.0

        SequentialAnimation on opacity {
            running: bridge && bridge.flickerEnabled && bridge.effectFps > 0
            loops: Animation.Infinite
            NumberAnimation {
                to: bridge ? 0.012 + bridge.effectOpacity * 0.035 : 0.0
                duration: 90
                easing.type: Easing.OutQuad
            }
            NumberAnimation { to: 0.0; duration: 460; easing.type: Easing.InOutQuad }
            PauseAnimation { duration: bridge && bridge.effectFps >= 45 ? 900 : 2400 }
        }
    }

    // Horizontal sync band: a slow travelling darker band, cinematic mode only.
    Rectangle {
        id: syncBand
        visible: bridge && bridge.syncEnabled
        width: parent.width
        height: Math.max(30, parent.height * 0.05)
        color: "#000000"
        opacity: bridge && bridge.syncEnabled ? 0.05 + bridge.effectOpacity * 0.06 : 0

        NumberAnimation on y {
            running: bridge && bridge.syncEnabled && bridge.effectFps > 0
            loops: Animation.Infinite
            from: -60
            to: distortion.height + 60
            duration: bridge && bridge.effectFps >= 45 ? 7000 : 12000
        }
    }

    // Fault lock: red edge clamp while an error state is active.
    Rectangle {
        anchors.fill: parent
        visible: distortion.faultLocked
        color: "transparent"
        border.color: bridge ? bridge.errorColor : "#ff4d5e"
        border.width: 2
        opacity: 0.55

        SequentialAnimation on opacity {
            running: distortion.faultLocked
            loops: Animation.Infinite
            NumberAnimation { to: 0.25; duration: 700 }
            NumberAnimation { to: 0.6; duration: 700 }
        }
    }
}
