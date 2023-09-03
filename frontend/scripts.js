/**
 * Allow the user to rotate the given element by left-clicking the element and dragging the mouse in a circle around the element center until the left mouse button is released.
 */
class RotationController {

    /**
     * Create a new `RotationController` for the given `element`.
     * @param {HTMLElement} element The element rotated by this instance
     * @param {Object} options The options for this instance
     * @param {number} [options.rotationSteps=360] The number of positions to which the element can snap during rotation, evenly divided around the circle.
     */
    constructor(element, { rotationSteps = 360 } = {}) {

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
     * Enable the rotating state and the current element center on left-click
     * @private
     * @param {MouseEvent} e The mouse down event
     */
    _onMouseDown(e) {
        e.preventDefault();

        const boundingRect = this.element.getBoundingClientRect();

        this._center.x = boundingRect.left + boundingRect.width / 2;
        this._center.y = boundingRect.top + boundingRect.height / 2;

        this._isRotating = true;
        this.element.classList.add('active');

        document.addEventListener('mousemove', this._boundOnMouseMove);
        document.addEventListener('mouseup', this._boundOnMouseUp);
    }

    /**
    * Calculate the rotation angle when the user moves their mouse while rotating the image
    * @private
    * @param {MouseEvent} e The mouse move event
    */
    _onMouseMove(e) {
        // Do nothing if the user is not actively rotating the element
        if (!this._isRotating) return;

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

    /**
     * Disables the rotating state when the left mouse button is released
     * @private
     * @param {MouseEvent} e The mouse up event
     */
    _onMouseUp() {
        this._isRotating = false;
        this.element.classList.remove('active');

        document.removeEventListener('mousemove', this._boundOnMouseMove);
        document.removeEventListener('mouseup', this._boundOnMouseUp);
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

/**
 * Render a set of images under the given root node and allow each rendered image to be rotated. Collect the overall rotation state as the current CAPTCHA solution.
 */
class RotatingImagesController {

    /**
     * Create a new `RotatingCirclesController` instance
     * @param {HTMLElement} root The root element in which to render the images
     */
    constructor(root) {

        /**
         * @type {HTMLElement}
         */
        this.root = root;

        /**
         * @type {RotationController[]}
         * @private
         */
        this._controllers = [];
    }

    /**
     * Render the given images and attach RotationController instances to each image
     * @param {string[]} images List of base64 encoded images
     */
    render(images) {
        this.root.classList.add('rotating-images')
        for (const image of images) {
            const imgElement = document.createElement('img');
            imgElement.src = "data:image/png;base64," + image;
            imgElement.classList.add('rotatable-image');

            this._controllers.push(new RotationController(imgElement, { rotationSteps: 360 }));
            this.root.appendChild(imgElement);
        }
    }

    /**
     * Destroy each active controller and remove all child elements from the root element
     */
    destroy() {
        this.root.classList.remove('rotating-images')
        // Destroy each active controller
        while (this._controllers.length) {
            this._controllers.pop().destroy();
        }

        // Remove all child elements from the root element
        while (this.root.firstChild) {
            this.root.removeChild(this.root.firstChild);
        }
    }

    /**
     * Reset every active controller to its original state
     */
    reset() {
        this._controllers.forEach(controller => controller.reset())
    }

    /**
     * The current solution as a list of the number of degrees by which each element is rotated
     * @type {number[]}
     */
    get solution() {
        return this._controllers.map(controller => controller.currentRotation);
    }
}

/**
 * A controller class to manage a draggable and droppable grid of images.
 */
class DragDropGridController {

    /**
     * Initialize a new instance of the `DragDropGridController` class.
     * @param {HTMLElement} root The root HTML element for the grid.
     * @param {Object} [options] The options for the controller.
     * @param {number} [options.columns=1] The number of columns in the grid.
     */
    constructor(root, { columns = 1 } = {}) {
        /**
         * The root HTML element for the grid.
         * @type {HTMLElement}
         */
        this.root = root;

        /**
         * The number of columns in the grid.
         * @type {number}
         */
        this.columns = columns;

        /**
         * The images to be rendered in the grid. Determines the default order of the images.
         * @type {string[]}
         * @private
         */
        this._images = [];
    }

    /**
     * Render the grid with the provided images.
     * @param {string[]} images - The images to be rendered.
     */
    render(images) {
        this._images = images;

        this.root.classList.add('grid-container');
        this.root.style.setProperty('--columns', this.columns);

        this._images.forEach((image, index) => {
            const gridItemElement = document.createElement('div');
            gridItemElement.classList.add('grid-item');
            gridItemElement.setAttribute('draggable', 'true');
            gridItemElement.setAttribute('data-index', index)

            gridItemElement.innerText = index;

            const imgElement = document.createElement('img');
            imgElement.src = "data:image/png;base64," + image;
            gridItemElement.appendChild(imgElement)

            gridItemElement.addEventListener('dragstart', this._onDragStart.bind(this));
            gridItemElement.addEventListener('dragover', this._onDragOver.bind(this));
            gridItemElement.addEventListener('drop', this._onDrop.bind(this));

            this.root.appendChild(gridItemElement);
        });
    }

    /**
     * Remove all the grid items and reset the root styles.
     */
    destroy() {
        this.root.classList.remove('grid-container');
        this.root.style.removeProperty('--columns');

        while (this.root.firstChild) {
            this.root.removeChild(this.root.firstChild);
        }
    }

    /**
     * Reset the grid to its initial state.
     */
    reset() {
        this.destroy();
        this.render(this._images);
    }

    /**
     * The current order of images in the grid as their indices.
     * @returns {number[]} The order of images as an array of indices.
     */
    get solution() {
        return Array.from(this.root.children).map(node => Number.parseInt(node.getAttribute('data-index')));
    }

    /**
     * Handle the drag start event.
     * @param {DragEvent} event - The drag event.
     * @private
     */
    _onDragStart(event) {
        // Finds the current index of the target element without needing to create a new array
        const sourceIndex = Array.prototype.indexOf.call(this.root.children, event.target);
        event.dataTransfer.setData('sourceIndex', sourceIndex);
        event.dataTransfer.setDragImage(event.target.getElementsByTagName('img')[0], 0, 0);
        event.dataTransfer.dropEffect = "move";
    }

    /**
     * Handle the drag over event to allow the drop.
     * @param {DragEvent} event - The drag event.
     * @private
     */
    _onDragOver(event) {
        event.preventDefault();
    }

    /**
     * Handle the drop event to reorder the grid items.
     * @param {DragEvent} event - The drop event.
     * @private
     */
    _onDrop(event) {
        event.preventDefault();

        const sourceIndex = event.dataTransfer.getData('sourceIndex');
        const source = this.root.children.item(sourceIndex);

        const target = event.target.closest('.grid-item');
        const targetIndex = Array.prototype.indexOf.call(this.root.children, target);

        if (sourceIndex === targetIndex) return;

        // If dragging from left to right
        if (sourceIndex < targetIndex) {
            if (target.nextSibling) {
                this.root.insertBefore(source, target.nextSibling);
            } else {
                this.root.appendChild(source);
            }
        }
        // If dragging from right to left
        else {
            this.root.insertBefore(source, target);
        }
    }
}

/**
 * Render images as a grid and allow them to be rotated in place
 */
class ImageGridController {

    /**
     * Create a new `ImageGridController` instance
     * @param {HTMLElement} root The root element in which to render the images
     * @param {Object} [options] The options for the controller.
     * @param {number} [options.columns=2] The number of columns in the grid.
     * @param {number} [options.rotationSteps=4] The number of rotation steps for each image.
     */
    constructor(root, { columns = 2, rotationSteps = 4 } = {}) {

        /**
         * @type {HTMLElement}
         */
        this.root = root;

        /**
         * @type {number}
         */
        this.columns = columns;

        /**
         * Number of rotation steps for each image.
         * @type {number}
         */
        this.rotationSteps = rotationSteps;

        /**
         * @type {RotationController[]}
         * @private
         */
        this._controllers = [];
    }

    /**
     * Render the grid with the provided images.
     * @param {string[]} images - The images to be rendered.
     */
    render(images) {
        this.root.classList.add('grid-container');
        this.root.style.setProperty('--columns', this.columns);

        images.forEach((image, index) => {
            const gridItemElement = document.createElement('div');
            gridItemElement.classList.add('grid-item');

            gridItemElement.innerText = index;

            const imgElement = document.createElement('img');
            imgElement.src = "data:image/png;base64," + image;
            gridItemElement.appendChild(imgElement);

            this._controllers.push(new RotationController(gridItemElement, { rotationSteps: this.rotationSteps }));

            this.root.appendChild(gridItemElement);
        });
    }

    /**
     * Remove all the grid items, destroy all rotation controllers and reset the root styles.
     */
    destroy() {
        this.root.classList.remove('grid-container');
        this.root.style.removeProperty('--columns');

        while (this._controllers.length) {
            this._controllers.pop().destroy();
        }

        while (this.root.firstChild) {
            this.root.removeChild(this.root.firstChild);
        }
    }

    /**
     * Reset the grid to its initial state.
     */
    reset() {
        this._controllers.forEach(controller => controller.reset());
    }

    /**
     * The current solution as a list of the number of degrees by which each element is rotated
     * @returns {number[]} Array of rotation degrees for each image.
     */
    get solution() {
        return this._controllers.map(controller => controller.currentRotation);
    }
}
