"""Welcome to Reflex! This file showcases the custom component in a basic app."""

import dataclasses

import reflex as rx
from reflex_mouse_track import MousePosition, mouse_track


@dataclasses.dataclass
class Point:
    """Point dataclass."""

    x: int
    y: int

    def __eq__(self, other):
        """Check if two points are equal."""
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __add__(self, other: "Point | None"):
        """Add two points."""
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Subtract two points."""
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x - other.x, self.y - other.y)

    def to(self, other: "Point"):
        """Return the distance between two points."""
        return Point(self.x - other.x, self.y - other.y)


class MouseTrackState(rx.State):
    """State tracking the mouse position."""

    selecting: rx.Field[bool] = rx.field(False)
    selected: rx.Field[bool] = rx.field(False)

    top_left: rx.Field[Point] = rx.field(Point(0, 0))
    bottom_right: rx.Field[Point] = rx.field(Point(0, 0))

    def handle_click(self, mouse: Point):
        """Handle click event."""
        yield rx.toast(f"Click event: {mouse}")

    def on_mouse_down(self, mouse: Point):
        """Handle mouse down event."""
        self.selected = False
        self.selecting = True
        self.top_left = mouse
        self.bottom_right = Point(0, 0)
        yield rx.toast(f"Mouse down event: {mouse}")

    def on_mouse_up(self, mouse: Point):
        """Handle mouse up event."""
        self.selecting = False
        self.selected = True

        if mouse.x < self.top_left.x:
            self.bottom_right.x = self.top_left.x
            self.top_left.x = mouse.x
        else:
            self.bottom_right.x = mouse.x

        if mouse.y < self.top_left.y:
            self.bottom_right.y = self.top_left.y
            self.top_left.y = mouse.y
        else:
            self.bottom_right.y = mouse.y

        self.top_left = self.top_left
        self.bottom_right = self.bottom_right

        if self.top_left == self.bottom_right:
            self.selected = False

        yield rx.toast(f"Mouse up event: {mouse}")


def selecting_area():
    """Return the selecting area."""
    return rx.cond(
        MouseTrackState.selecting,
        rx.box(
            border="2px dashed red",
            radius="full",
            width=abs(MouseTrackState.top_left.x - MousePosition.x),
            height=abs(MouseTrackState.top_left.y - MousePosition.y),
            position="absolute",
            left=rx.cond(
                MouseTrackState.top_left.x < MousePosition.x,
                MouseTrackState.top_left.x,
                MousePosition.x,
            ),
            top=rx.cond(
                MouseTrackState.top_left.y < MousePosition.y,
                MouseTrackState.top_left.y,
                MousePosition.y,
            ),
        ),
    )


def selected_area():
    """Return the selected area."""
    return rx.cond(
        MouseTrackState.selected,
        rx.box(
            border="2px solid red",
            radius="full",
            width=abs(MouseTrackState.top_left.x - MouseTrackState.bottom_right.x),
            height=abs(MouseTrackState.top_left.y - MouseTrackState.bottom_right.y),
            position="absolute",
            left=MouseTrackState.top_left.x,
            top=MouseTrackState.top_left.y,
        ),
    )


@rx.memo
def track_area():
    """Instantiate the MouseTrack component."""
    return mouse_track(
        selected_area(),
        selecting_area(),
        rx.text(MousePosition.pixel.x),
        rx.text(MousePosition.pixel.y),
        width="90vw",
        height="90vh",
        position="absolute",
        background_color=rx.color("indigo", 5),
        on_mouse_down=MouseTrackState.on_mouse_down,
        on_mouse_up=MouseTrackState.on_mouse_up,
    )


def index():
    """Index page."""
    return rx.center(
        track_area(),
        height="100vh",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
