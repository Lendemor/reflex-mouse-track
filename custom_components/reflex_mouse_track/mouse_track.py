"""Reflex custom component MouseTrack."""

# For wrapping react guide, visit https://reflex.dev/docs/wrapping-react/overview/

from types import SimpleNamespace

import reflex as rx


class MousePosition(SimpleNamespace):
    """MousePosition namespace."""

    x = rx.Var("Math.round(mouse.x)").to(int)
    y = rx.Var("Math.round(mouse.y)").to(int)
    pixel = SimpleNamespace(
        x=rx.Var(f"{x} + `px`"),
        y=rx.Var(f"{y} + `px`"),
    )
    defined = rx.Var("mouse.x & mouse.y")


def on_click_signature() -> list[rx.Var]:
    """Return the signature for the on_click event of MouseTrack."""
    callback = rx.vars.function.ArgsFunctionOperation.create(
        [],
        {"x": MousePosition.x, "y": MousePosition.y},
        _var_data=rx.vars.VarData(deps=[rx.Var("mouse")]),
    ).call()
    return [callback]


class MouseTrack(rx.el.Div, rx.Component):
    """MouseTrack component."""

    on_click: rx.EventHandler[on_click_signature]
    on_mouse_down: rx.EventHandler[on_click_signature]
    on_mouse_up: rx.EventHandler[on_click_signature]

    def add_hooks(self):
        """Add hooks for MouseTrack."""
        return [
            rx.Var(
                f"const mouse = useMouse({self.get_ref()}, {{enterDelay: 100,leaveDelay: 100}});",
                _var_data=rx.vars.VarData(
                    imports={
                        "@react-hook/mouse-position@4.1.3": [
                            rx.ImportVar(tag="useMouse", is_default=True)
                        ],
                    }
                ),
            )
        ]

    def get_ref(self):
        """Return the ref for MouseTrack."""
        return "mouseRef"

    @classmethod
    def create(cls, *children, **props):
        """Create a MouseTrack component."""
        props["width"] = props.get("width", "100vw")
        props["height"] = props.get("height", "100vh")
        return super().create(*children, **props)


mouse_track = MouseTrack.create
