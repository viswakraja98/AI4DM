let divData, story_text, story_style, speech, startBtn, stopBtn;

function setup() {
    let c = createCanvas(600, 600);
    c.parent('canvas-div');
    divData = document.querySelector("#canvas-div");

    speech = new p5.Speech(); // speech synthesis object

    // Start button setup
    let startBtnDiv = document.querySelector('#startBtnDiv');
    startBtn = createButton('Start Narrating!');
    startBtn.parent(startBtnDiv);
    startBtn.class('btn btn-primary');
    startBtn.mousePressed(startSpeaking);

    // Stop button setup
    let stopBtnDiv = document.querySelector('#stopBtnDiv');
    stopBtn = createButton('Stop Narrating!');
    stopBtn.parent(stopBtnDiv);
    stopBtn.class('btn btn-danger');
    stopBtn.mousePressed(stopSpeaking);
}

function draw() {
    // Get the story text and style
    story_text = divData.dataset.story;
    story_style = divData.dataset.style;

    // Set background color based on story_style condition
    if (story_style === "Surprise") {
        background(128, 0, 128); // Purple
    } else if (story_style === "Joy") {
        background(255, 255, 0); // Yellow
    } else if (story_style === "Fear") {
        background(0, 0, 255); // Blue
    } else if (story_style === "Anger") {
        background(255, 0, 0); // Red
    } else if (story_style === "Sadness") {
        background(0, 100, 0); // Dark Green
    } else if (story_style === "Love") {
        background(255, 105, 180); // Pink
    } else {
        background(0); // Default black color
    }

    // Display text in the top-left corner
    fill(255); // White text color
    textSize(18);
    textWrap(WORD);
    textAlign(LEFT, TOP); // Align text to the top left
    text(story_text || "Waiting for generated image...", 20, 20, width - 40, height - 40);
}

function startSpeaking() {
    if (story_text !== "Waiting for generated image...") {
        speech.speak(story_text);
    }
}

function stopSpeaking() {
    speech.stop();
}
