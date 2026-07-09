#!/usr/bin/env python3
"""Offscreen screenshot smoke for the Hyperterminal QML surface.

Loads the real QML shell offscreen, grabs a frame, verifies the frame is
not blank, and optionally writes the PNG for release evidence.

Usage:
    python scripts/visual_screenshot_smoke.py --theme apex-reactor \
        --out /tmp/apex-smoke.png
"""

from __future__ import annotations

import argparse
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_BACKEND", "software")


def main() -> int:
    """Run one offscreen screenshot smoke pass."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--theme", default="apex-reactor")
    parser.add_argument("--out", default="")
    parser.add_argument("--grab-after-ms", type=int, default=700)
    args = parser.parse_args()

    # Importing QtQuick ensures the QML root window is wrapped as a
    # QQuickWindow so grabWindow() is available.
    from PySide6.QtQuick import (  # pylint: disable=import-outside-toplevel
        QQuickWindow,
    )

    from apex_infinite_visual.main import (  # pylint: disable=import-outside-toplevel
        build_bridge_class,
        import_qt_modules,
        parse_args,
    )

    options = parse_args(
        [
            "--theme",
            args.theme,
            "--path",
            "/tmp",
            "--dry-run",
            "--no-restore-profile",
            "--auto-close-ms",
            str(args.grab_after_ms + 1500),
        ]
    )
    qt = import_qt_modules()
    app = qt["QApplication"](sys.argv[:1])
    bridge = build_bridge_class(qt)(options)
    engine = qt["QQmlApplicationEngine"]()
    engine.rootContext().setContextProperty("bridge", bridge)
    engine.load(qt["QUrl"].fromLocalFile(str(options.qml_path)))
    if not engine.rootObjects():
        print("SMOKE FAIL: QML surface could not be loaded", file=sys.stderr)
        return 1

    window = engine.rootObjects()[0]
    if not isinstance(window, QQuickWindow):
        print("SMOKE FAIL: root object is not a QQuickWindow", file=sys.stderr)
        return 1
    result = {"code": 1}

    def grab() -> None:
        image = window.grabWindow()
        if image.isNull() or image.width() < 100 or image.height() < 100:
            print("SMOKE FAIL: grabbed image is empty", file=sys.stderr)
            app.quit()
            return
        colors = set()
        step = max(1, image.width() // 64)
        for x in range(0, image.width(), step):
            for y in range(0, image.height(), max(1, image.height() // 64)):
                colors.add(image.pixel(x, y))
                if len(colors) > 8:
                    break
            if len(colors) > 8:
                break
        if len(colors) <= 2:
            print(
                f"SMOKE FAIL: frame is blank ({len(colors)} colors)",
                file=sys.stderr,
            )
            app.quit()
            return
        if args.out:
            image.save(args.out)
        print(
            f"SMOKE OK: theme={args.theme} size={image.width()}x{image.height()} "
            f"distinct-colors>{len(colors) - 1}"
        )
        result["code"] = 0
        app.quit()

    bridge.startRun()
    qt["QTimer"].singleShot(args.grab_after_ms, grab)
    qt["QTimer"].singleShot(args.grab_after_ms + 8000, app.quit)
    app.exec()
    bridge.shutdown()
    return result["code"]


if __name__ == "__main__":
    raise SystemExit(main())
