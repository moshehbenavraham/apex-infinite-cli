import QtQuick

Item {
    id: surface

    property var bridge

    // The effect surface only decorates; it never intercepts input.
    enabled: false

    function trigger(name) {
        if (name === "surface_charge")
            glow.sweep(0.9)
        else if (name === "signal_sweep")
            glow.sweep(0.5)
        else if (name === "completion_sweep")
            glow.sweep(1.0)
        else if (name === "glow_drain")
            glow.drainNow()
        else if (name === "persistence_trail" || name === "decision_pulse")
            trail.pulse()
        else if (name === "fault_lock" || name === "error_signature")
            trail.faultPulse()
        distortion.faultLocked = bridge
            ? bridge.runHealth === "failed"
            : false
    }

    Connections {
        target: bridge

        function onPulsesChanged() {
            var names = bridge.pulseNames
            for (var i = 0; i < names.length; i++)
                surface.trigger(names[i])
        }

        function onStatusChanged() {
            distortion.faultLocked = bridge.runHealth === "failed"
        }
    }

    GlowField {
        id: glow
        anchors.fill: parent
        bridge: surface.bridge
    }

    PhosphorTrail {
        id: trail
        anchors.fill: parent
        bridge: surface.bridge
    }

    ScanlineField {
        anchors.fill: parent
        bridge: surface.bridge
    }

    SignalDistortion {
        id: distortion
        anchors.fill: parent
        bridge: surface.bridge
    }

    GlassCurvature {
        anchors.fill: parent
        bridge: surface.bridge
    }

    FrameTreatment {
        anchors.fill: parent
        anchors.margins: 4
        bridge: surface.bridge
    }
}
