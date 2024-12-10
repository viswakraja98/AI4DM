<script lang="ts">

    import {onDestroy, onMount} from 'svelte';
    import p5 from 'p5';

    let canvas: HTMLCanvasElement = document.createElement('canvas');
    let gridSize = 50;
    let circle: DrawingCircle;
    let isDrawingCircle = false;
    let isMovingCircle = false;
    let audioContext: AudioContext;
    let beepOscillator: OscillatorNode | null = null;
    let gainNode: GainNode | null = null;
    let spacebarDown = false;
    let isIntersectionAudioEnabled = true;
    let _p: p5;

    let {lines = $bindable(), canvasImage = $bindable()} = $props();

    // let lines: { x: number; y: number }[][] = $props();
    // let canvasImage: string = $props();

    class DrawingCircle {
        x: number;
        y: number;
        radius: number;
        currentPath: { x: number; y: number }[];

        constructor(x: number, y: number, radius: number) {
            this.x = x;
            this.y = y;
            this.radius = radius;
            this.currentPath = [];
        }

        draw(p: p5) {
            p.fill(255, 0, 0);
            p.stroke(0);
            p.strokeWeight(2);
            p.ellipse(this.x, this.y, this.radius * 2);
        }

        contains(p: p5, mx: number, my: number) {
            return p.dist(mx, my, this.x, this.y) <= this.radius;
        }

        move(p: p5, mx: number, my: number) {
            this.x = p.constrain(mx, 0, 600);
            this.y = p.constrain(my, 0, 400);
        }
    }

    function getGridCoordinates(x: number, y: number) {
        let gridX = Math.floor(x / gridSize);
        let gridY = Math.floor(y / gridSize);
        return {
            x: gridX,
            y: gridY
        };
    }
    function createBeepOscillator() {
        if (beepOscillator) {
            beepOscillator.stop();
        }
        beepOscillator = audioContext.createOscillator();
        beepOscillator.start();
        gainNode = audioContext.createGain();
        beepOscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
    }

    function quiet() {
        if (gainNode == null) return;
        gainNode.gain.setValueAtTime(0, audioContext.currentTime);
        return;
    }
    function ring() {
        if (beepOscillator == null || gainNode == null) {
            createBeepOscillator();
        }
        beepOscillator!.frequency.setValueAtTime(1200, audioContext.currentTime);
        gainNode!.gain.setValueAtTime(0.7, audioContext.currentTime);
    }

    function adjustGridSound(x: number, y: number) {
        if (beepOscillator == null || gainNode == null) {
            createBeepOscillator();
        }
        if (!isIntersectionAudioEnabled) {
            gainNode!.gain.setValueAtTime(0, audioContext.currentTime);
            return;
        }

        if (x < 600 && x > 0 && y < 400 && y > 0) {
            if (audioContext.state != 'running' && isIntersectionAudioEnabled) {
                createBeepOscillator();
            }
        } else {
            return;
        }

        let frequency = p5.prototype.constrain(p5.prototype.map(x, 0, 600, 300, 500), 300, 500);
        let volume = p5.prototype.constrain(p5.prototype.map(y, 400, 0, 0.05, 0.7), 0.05, 0.7);

        beepOscillator!.frequency.setValueAtTime(frequency, audioContext.currentTime);
        gainNode!.gain.setValueAtTime(volume, audioContext.currentTime);
    }

    onMount(() => {
        audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
        new p5((p: p5) => {
            _p = p;
            p.setup = () => {
                p.createCanvas(600, 400, canvas);
                p.background(240);
                drawGrid(p);
                circle = new DrawingCircle(p.width / 2, p.height / 2, 20);
            };

            p.draw = () => {
                if (!isDrawingCircle && !isMovingCircle) {
                    p.background(240);
                    drawGrid(p);

                    lines.forEach(path => {
                        p.stroke(0);
                        p.strokeWeight(2);
                        p.noFill();
                        p.beginShape();
                        path.forEach(point => {
                            p.vertex(point.x, point.y);
                        });
                        p.endShape();
                    });

                    circle.draw(p);
                }
            };

            p.mouseMoved = () => {
                if (circle.contains(p, p.mouseX, p.mouseY)) {
                    ring();
                } else {
                    quiet();
                }
            }

            p.mousePressed = () => {
                if (spacebarDown && circle.contains(p, p.mouseX, p.mouseY)) {
                    isMovingCircle = true;
                } else if (!spacebarDown && circle.contains(p, p.mouseX, p.mouseY)) {
                    isDrawingCircle = true;
                    circle.currentPath = [{ x: circle.x, y: circle.y }];
                }
            };

            p.mouseDragged = () => {
                if (isMovingCircle) {
                    circle.move(p, p.mouseX, p.mouseY);


                    p.background(240);
                    drawGrid(p);

                    lines.forEach(path => {
                        p.stroke(0);
                        p.strokeWeight(2);
                        p.noFill();
                        p.beginShape();
                        path.forEach(point => {
                            p.vertex(point.x, point.y);
                        });
                        p.endShape();
                    });

                    circle.draw(p);
                } else if (isDrawingCircle) {
                    circle.move(p, p.mouseX, p.mouseY);
                    adjustGridSound(p.mouseX, p.mouseY)

                    circle.currentPath.push({ x: circle.x, y: circle.y });

                    p.background(240);
                    drawGrid(p);

                    lines.forEach(path => {
                        p.stroke(0);
                        p.strokeWeight(2);
                        p.noFill();
                        p.beginShape();
                        path.forEach(point => {
                            p.vertex(point.x, point.y);
                        });
                        p.endShape();
                    });

                    p.stroke(0, 100);
                    p.strokeWeight(2);
                    p.noFill();
                    p.beginShape();
                    circle.currentPath.forEach(point => {
                        p.vertex(point.x, point.y);
                    });
                    p.endShape();

                    circle.draw(p);
                }
            };

            p.mouseReleased = () => {
                if (isDrawingCircle) {
                    if (circle.currentPath.length > 1) {
                        lines = [...lines, circle.currentPath];
                        canvasImage = _base64(p, 2);
                    }
                    isDrawingCircle = false;
                }

                isMovingCircle = false;
            };

            function drawGrid(p: p5) {
                p.stroke(200);
                p.strokeWeight(1);

                for (let x = 0; x <= p.width; x += gridSize) {
                    p.line(x, 0, x, p.height);
                }

                for (let y = 0; y <= p.height; y += gridSize) {
                    p.line(0, y, p.width, y);
                }
            }
        });
    });

    const handleKeyPress = (e: KeyboardEvent) => {
        if (e.key === 'c') {
            lines = [];
        }
        if (e.key === 'w') {
            spacebarDown = !spacebarDown;
            isDrawingCircle = false;
            isMovingCircle = false;
        }
        if (e.key === 'z') {
            lines = lines.slice(0, -1);
        }

        if (e.key === 's' || e.key === 'S') {
            const gridCoords = getGridCoordinates(circle.x, circle.y);

            const message = `Circle is in grid box: Column ${gridCoords.x}, Row ${gridCoords.y}`;

            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(message);
                window.speechSynthesis.speak(utterance);
            }
            alert(message);
        }

        if (e.key === 'f' || e.key === 'F') {
            isIntersectionAudioEnabled = !isIntersectionAudioEnabled;

            const message = isIntersectionAudioEnabled
                ? 'Intersection Audio: Enabled'
                : 'Intersection Audio: Disabled';

            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(message);
                window.speechSynthesis.speak(utterance);
            }
            alert(message);
        }
    };

    function _base64(p: p5, multiplier: number = 2) {
        const offScreenCanvas = document.createElement('canvas');
        offScreenCanvas.width = p.width * multiplier;
        offScreenCanvas.height = p.height * multiplier;
        const offScreenContext = offScreenCanvas.getContext('2d');

        if (offScreenContext) {
            offScreenContext.clearRect(0, 0, offScreenCanvas.width, offScreenCanvas.height);
            offScreenContext.fillStyle = '#f0f0f0';  // Background color
            offScreenContext.fillRect(0, 0, offScreenCanvas.width, offScreenCanvas.height);
            offScreenContext.lineWidth = 1 * multiplier; // Double the original line width
            for (let path of lines) {
                offScreenContext.beginPath();
                offScreenContext.moveTo(path[0].x * multiplier, path[0].y * multiplier); // Double the coordinates
                for (let point of path) {
                    offScreenContext.lineTo(point.x *  multiplier, point.y * multiplier); // Double the coordinates
                }
                offScreenContext.stroke();
            }

            return offScreenCanvas.toDataURL('image/png');
        }
        return ""
    }


</script>

<style>
    #canvas-container {
        outline: None;
    }
    canvas {
        border-radius: 25px;
    }
</style>

<div id="canvas-container" onkeyup={(e) => handleKeyPress(e)} tabindex="0">
    <canvas bind:this={canvas}></canvas>
</div>

