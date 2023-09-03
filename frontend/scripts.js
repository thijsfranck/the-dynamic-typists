/**
 * Allows the user to rotate the given element by left-clicking the element and dragging the mouse in a circle around the element center until the left mouse button is released.
 */
class RotationController {

    /**
     * Creates a new `RotationController` for the given `element`.
     * @param {HTMLElement} element The element rotated by this instance
     * @param {Object} options The options for this instance
     * @param {number} [options.rotationSteps=360] The number of positions to which the element can snap during rotation, evenly divided around the circle.
     */
    constructor(element, { rotationSteps = 360 }) {

        /**
         * The element rotated by this instance
         * @type {HTMLElement}
         */
        this.element = element;

        /**
         * The number of positions to which the element can snap during rotation, evenly divided around the circle.
         * @type {number}
         */
        this.rotationSteps = rotationSteps;

        /**
         * The current center of the image
         * @private
         */
        this._center = { x: 0, y: 0 };

        /**
         * The number of degrees by which the element is currently rotated
         * @private
         */
        this._currentRotation = 0;

        /**
         * Whether or not the user is currently rotating the element
         * @private
         */
        this._isRotating = false;

        /**
         *  Mouse down event to start rotation
         *  @private
         */
        this._boundOnMouseDown = this._onMouseDown.bind(this);
        this.element.addEventListener('mousedown', this._boundOnMouseDown);

        /**
         * Mouse move event to rotate the element
         * @private
         */
        this._boundOnMouseMove = this._onMouseMove.bind(this);
        document.addEventListener('mousemove', this._boundOnMouseMove);

        /**
         * Mouse up event to stop rotation
         * @private
         */
        this._boundOnMouseUp = this._onMouseUp.bind(this);
        document.addEventListener('mouseup', this._boundOnMouseUp);
    }

    /**
     * Enables the rotating state and the current element center on left-click
     * @private
     * @param {MouseEvent} e The mouse down event
     */
    _onMouseDown(e) {
        e.preventDefault();

        const boundingRect = this.element.getBoundingClientRect();

        this._center.x = boundingRect.left + boundingRect.width / 2;
        this._center.y = boundingRect.top + boundingRect.height / 2;
        this._isRotating = true;
    }

    /**
    * Calculates the rotation angle when the user moves their mouse while rotating the image
    * @private
    * @param {MouseEvent} e The mouse move event
    */
    _onMouseMove(e) {
        if (this._isRotating) {
            // Calculate the current angle of the pointer relative to the center of the element
            const dx = e.pageX - this._center.x;
            const dy = e.pageY - this._center.y;

            let angle = Math.atan2(dx, -dy) * (180 / Math.PI);

            // Ensure the element rotates 360 degrees to avoid the image flipping
            // when moving beyond 180 degrees
            if (angle < 0) {
                angle = angle + 360;
            }

            // Calculate the degrees per rotation step
            const degreesPerStep = 360 / this.rotationSteps;

            // Snapping the angle to the nearest step
            angle = Math.round(angle / degreesPerStep) * degreesPerStep;

            this.rotate(angle);
        }
    }

    /**
     * Disables the rotating state when the left mouse button is released
     * @private
     * @param {MouseEvent} e The mouse up event
     */
    _onMouseUp() {
        this._isRotating = false;
    }

    /** Unbinds all event listeners */
    destroy() {
        this.element.removeEventListener('mousedown', this._boundOnMouseDown);
        document.removeEventListener('mousemove', this._boundOnMouseMove);
        document.removeEventListener('mouseup', this._boundOnMouseUp);
    }

    /** Rotates the element to 0 degrees */
    reset() {
        this.rotate(0);
    }

    /**
      Rotates the image by the given `degrees`.
      @param {number} degrees - The number of degrees by which the image should be rotated (0 - 360)
    */
    rotate(degrees) {
        this._currentRotation = degrees % 360;
        this.element.style.transform = `rotate(${this._currentRotation}deg)`;
    }


    /**
     * The number of degrees by which the element is currently rotated
     * @returns {number} The current rotation angle in degrees (0-360)
     */
    get currentRotation() {
        return this._currentRotation;
    }
}
