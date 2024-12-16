# mouse-track

A Reflex custom component mouse-track.

## Installation

```bash
pip install reflex-mouse-track
```

Example:
```python
@dataclasses.dataclass
class Point:
    """Point dataclass."""

    x: int
    y: int

class MouseTrackState(rx.State):
    def handle_click(self, mouse: Point):
        """Handle click event."""
        yield rx.toast(f"Click event: {mouse}")

def tracking_area():
    return mouse_track(
        background_color="gray",
        on_click=MouseTrackState.handle_click,
        width="100vw",
        height="100vh",
    )
```

## API
- Event Triggers:
    - `on_click`: Triggered when the user clicks on the tracking area.
    - `on_mouse_down`: Triggered when the user press a mouse button on the tracking area.
    - `on_mouse_up`: Triggered when the user releases the mouse on the tracking area.

Known errors:
 - When trying to access `MousePosition`, if you get an error saying `'mouse' is undefined`, you might need to decorate the global function where you do the mouse tracking with `@rx.memo`. 