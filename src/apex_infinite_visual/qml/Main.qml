import QtQuick
import QtQuick.Controls
import "shell"

ApplicationWindow {
    id: root

    width: typeof initialWindowWidth !== "undefined" ? initialWindowWidth : 1280
    height: typeof initialWindowHeight !== "undefined" ? initialWindowHeight : 800
    minimumWidth: 980
    minimumHeight: 620
    visible: true
    title: "Apex Infinite Hyperterminal"
    color: safeBridge.backgroundColor

    property var safeBridge: (typeof bridge !== "undefined" && bridge)
        ? bridge : fallbackBridge

    onClosing: safeBridge.storeWindowGeometry(width, height)

    QtObject {
        id: fallbackBridge

        signal statusChanged()
        signal logChanged()
        signal controlsChanged()
        signal effectsChanged()
        signal specChanged()
        signal signalPanelChanged()
        signal doctorChanged()
        signal profilesChanged()
        signal pulsesChanged()

        property string statusText: "Offline"
        property string stageText: "Waiting"
        property string runHealth: "idle"
        property bool running: false
        property bool hasError: false
        property string errorText: ""
        property string projectPath: ""
        property string startCommand: "implement"
        property int maxIterations: 1
        property bool dryRun: true
        property string autonomySummary: "DRY RUN - Codex is not executed."
        property string providerName: "Provider pending"
        property string modelName: "Model pending"
        property string configSource: "Default config"
        property string codexFlagsText: "Not checked"
        property string eventStreamMode: "Fixture playback"
        property string historyDbText: "Created on first run"
        property string iterationText: "Not started"
        property string managerOutput: "No decision yet"
        property string managerReason: ""
        property var logLines: []
        property var eventRows: []
        property string stageFilter: ""
        property string severityFilter: ""
        property string searchText: ""
        property var pulseNames: []
        property bool specDetected: false
        property string specPhase: "No spec system"
        property string specSession: "Session pending"
        property string specCommand: "No command yet"
        property string taskProgressText: "No task data"
        property real taskProgressRatio: 0.0
        property string providerHealth: "unknown"
        property int stderrEvents: 0
        property int malformedEvents: 0
        property string durationText: "00:00"
        property string lastEvent: "None"
        property var artifacts: []
        property string backendName: "unknown"
        property bool shadersAvailable: false
        property string recommendedTier: "balanced"
        property var doctorRows: []
        property string doctorStatus: ""
        property bool doctorLaunchReady: true
        property bool firstRunNeeded: false
        property var profileNames: []
        property string activeProfile: ""
        property string profileError: ""
        property string themeName: "crt-green"
        property string effectiveThemeName: "crt-green"
        property string themeLabel: "Green CRT"
        property var themeNames: ["crt-green", "crt-amber", "ibm-dos", "plain"]
        property string renderingMode: "modern-crisp"
        property string effectiveRenderingMode: "modern-crisp"
        property var renderingModes: ["modern-crisp"]
        property string qualityTier: "balanced"
        property string effectiveQualityTier: "balanced"
        property var qualityTiers: ["balanced"]
        property int effectFps: 0
        property bool reducedEffects: true
        property bool plainFallback: false
        property int effectIntensity: 0
        property real effectOpacity: 0.0
        property string fontFamily: "monospace"
        property real fontScale: 1.0
        property real fontWidth: 1.0
        property real lineSpacing: 1.0
        property var fontFamilies: ["monospace"]
        property color backgroundColor: "#101419"
        property color panelColor: "#182029"
        property color panelAltColor: "#1e2732"
        property color cellColor: "#151b22"
        property color borderColor: "#303943"
        property color accentColor: "#e6edf3"
        property color textColor: "#e6edf3"
        property color mutedColor: "#8b949e"
        property color warningColor: "#d8b45f"
        property color errorColor: "#ff6f6f"
        property bool glowEnabled: false
        property bool scanlinesEnabled: false
        property bool flickerEnabled: false
        property bool curvatureEnabled: false
        property bool bloomEnabled: false
        property bool persistenceEnabled: false
        property bool noiseEnabled: false
        property bool jitterEnabled: false
        property bool syncEnabled: false
        property bool chromaEnabled: false
        property bool ambientFrameEnabled: false

        function startRun() {}
        function stopRun() {}
        function shutdown() {}
        function runDoctor() {}
        function storeWindowGeometry(_w, _h) {}
        function setProjectPath(_value) {}
        function setStartCommand(_value) {}
        function setMaxIterations(_value) {}
        function setDryRun(_value) {}
        function setStageFilter(_value) {}
        function setSeverityFilter(_value) {}
        function setSearchText(_value) {}
        function exportEvents(_path) {}
        function setTheme(_value) {}
        function setRenderingMode(_value) {}
        function setQualityTier(_value) {}
        function setEffectIntensity(_value) {}
        function setFontFamily(_value) {}
        function setFontScale(_value) {}
        function setFontWidth(_value) {}
        function setLineSpacing(_value) {}
        function setReducedEffects(_value) {}
        function setPlainFallback(_value) {}
        function setEffectEnabled(_name, _value) {}
        function saveProfile(_name) {}
        function loadProfile(_name) {}
        function deleteProfile(_name) {}
        function duplicateProfile(_source, _target) {}
        function exportProfile(_name, _path) {}
        function importProfile(_path) {}
    }

    AppShell {
        anchors.fill: parent
        bridge: root.safeBridge
    }
}
