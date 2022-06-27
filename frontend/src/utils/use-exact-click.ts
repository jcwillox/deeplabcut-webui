export function getEventLocation(e: MouseEvent | TouchEvent | Touch) {
  if (e instanceof TouchEvent) {
    e = e.touches[0];
  }
  return [e.clientX, e.clientY];
}

/**
 * On click callback is only triggered if the mouse did not move between the
 * mousedown and mouseup events.
 */
export function useExactClick(
  onClick: (
    x: number,
    y: number,
    e: PointerEvent | MouseEvent | TouchEvent
  ) => void,
  maxDiff = 2
) {
  let lX = 0;
  let lY = 0;

  const mouseDown = (e: MouseEvent | TouchEvent) => {
    [lX, lY] = getEventLocation(e);
  };

  const mouseUp = (e: MouseEvent | TouchEvent) => {
    const [x, y] = getEventLocation(e);
    const dX = Math.abs(lX - x);
    const dY = Math.abs(lY - y);
    if (dX <= maxDiff && dY <= maxDiff) {
      onClick(x, y, e);
    }
  };

  return [mouseDown, mouseUp];
}
