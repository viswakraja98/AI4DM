<script lang="ts">
  import P5jsCanvas from "./lib/p5js_canvas.svelte";

  let lines: any = $state([]);
  let canvasImage: string = $state("");
  let promptText: string = $state("");

  let sdxlLoading: boolean = $state(false);

  let sketchTranslatedURI: string = $state("");
  let imgDescriptorLoading: boolean = $state(false);
  let imageDescription: string = $state("");

  let vqaAnswer = $state("");
  let vqaLoading = $state(false);
  let vqaPromptText: string = $state("");


  function submitCanvas() {
    vqaAnswer = "";
    vqaPromptText = "";
    imageDescription = "";
    if (canvasImage != null && canvasImage !== "" && promptText != "") {
      sdxlLoading = true;
      fetch(
              "http://localhost:8000/run/sdxl",
              {
                method: 'POST', // HTTP method
                headers: {
                  'Content-Type': 'application/json' // Tell the server we're sending JSON data
                },
                body: JSON.stringify({
                  image: canvasImage,
                  prompt: promptText,
                })
              }
      ).then((response) => {
        response.text().then(text => {
          sketchTranslatedURI = text;
          sdxlLoading = false;
        }).catch(error => {sdxlLoading = false;});
      }).catch((error) => {sdxlLoading = false;});
    }
  }

  $effect(() => {
    if (sketchTranslatedURI != "") {
      imgDescriptorLoading = true;
      vqaAnswer = "";
      vqaPromptText = "";
      fetch(
              "http://localhost:8000/run/img_desc",
              {
                method: 'POST', // HTTP method
                headers: {
                  'Content-Type': 'application/json' // Tell the server we're sending JSON data
                },
                body: JSON.stringify({
                  image: sketchTranslatedURI,
                })
              }
      ).then((response) => {
        response.text().then(text => {
          imageDescription = text;
          imgDescriptorLoading = false;
        }).catch(error => {imgDescriptorLoading = false;});
      }).catch((error) => {imgDescriptorLoading = false;});
    }
  })


  let submitVQA = () => {
    if (vqaPromptText != "") {
      vqaLoading = true;
      fetch(
              "http://localhost:8000/run/vqa",
              {
                method: 'POST', // HTTP method
                headers: {
                  'Content-Type': 'application/json' // Tell the server we're sending JSON data
                },
                body: JSON.stringify({
                  image: sketchTranslatedURI,
                  prompt: vqaPromptText,
                })
              }
      ).then((response) => {
        response.text().then(text => {
          vqaAnswer = text;
          vqaLoading = false;
        }).catch(error => {vqaLoading = false;});
      }).catch((error) => {vqaLoading = false;});
    }
  }
</script>

<main>
  <div class="container" >
    <!-- Row 1 -->
    <h1>Accessible Canvas</h1>
    <h3>Sketch to Image Generation</h3>
    <div class="section-descriptor">
      Create a realistic image by drawing your concept sketch and providing a descriptive prompt.
    </div>
    <h4>Canvas Drawing Instructions:</h4>
    <div class="instructions">
      <ol>
        <li>Move your mouse to hover over the red circle (it will produce a ringing sound as your virtual cursor).</li>
        <li>Press and hold the mouse button over the circle to draw a path. Release to save the path.</li>
        <li>To move the circle without drawing, press 'w' and click and drag it. </li>
        <li>To undo the last line drawn, press 'z'. </li>
        <li>Press 's' to hear the circle's current grid location.</li>
        <li>Press 'f' to toggle grid intersection audio. When enabled, moving the circle across grid lines will produces varying pitch from left to right and increases volume as you move from bottom to top.</li>
      </ol>
    </div>
    <div class="row">
      <!-- Column 1 -->
<!--      <div class="col">-->
        <div>
          <span>You drew {lines.length} lines.</span>
          <P5jsCanvas bind:lines={lines} bind:canvasImage={canvasImage}></P5jsCanvas>
        </div>
<!--      </div>-->
      <!-- Column 2 -->
<!--      <div class="col inp-and-submit">-->
        <div class="input-field">
          <input name="promptText" bind:value={promptText} type="text" required spellcheck="false"/>
          <label for="promptText">Prompt</label>
        </div>
        <div>
          <input type="button" value="Submit" onclick={() => submitCanvas()} />
        </div>
<!--      </div>-->
    </div>

    <h3>Image Description & Visual Q&A</h3>
    <div class="section-descriptor">
      Explore AI image descriptions and ask detailed questions to gain deeper insights about the visuals.
    </div>
    <!-- Row 2 -->
    <div class="row">
      <!-- Column 1 -->
<!--      <div class="col">-->
        {#if (sketchTranslatedURI !== "" && !sdxlLoading)}
          <img class="boosted-img" src={sketchTranslatedURI} alt="Sketch boosted with AI" style="width: 600px"/>
        {:else if (sdxlLoading)}
          <img class="loading" src="https://media.tenor.com/On7kvXhzml4AAAAj/loading-gif.gif" alt="Loading">
          {:else}
          <div></div>
        {/if}
<!--      </div>-->
      <!-- Column 2 -->
<!--      <div class="col">-->
        {#if (imageDescription !== "" && !imgDescriptorLoading)}
          <div class="descriptor" style="text-align: start">{imageDescription}</div>
          <div class="inp-and-submit">
            <div class="input-field">
              <input name="vqaPromptText" bind:value={vqaPromptText} type="text" required spellcheck="false"/>
              <label for="vqaPromptText">Enter Question</label>
            </div>
            {#if (vqaAnswer !== "" && !vqaLoading)}
              <div class="vqa-answer">Answer: {vqaAnswer}</div>
            {:else if (vqaLoading)}
              <img class="loading"  src="https://media.tenor.com/On7kvXhzml4AAAAj/loading-gif.gif" alt="Loading">
            {:else} <div></div>
            {/if}
            <div>
              <input type="button" value="Submit" onclick={() => submitVQA()} />
            </div>
          </div>
        {:else if (vqaLoading)}
          <img class="loading"  src="https://media.tenor.com/On7kvXhzml4AAAAj/loading-gif.gif" alt="Loading">
          {:else} <div></div>
        {/if}
<!--      </div>-->
    </div>
    <h3>Project Overview</h3>
    <div class = "section-descriptor">
      The goal of my project is to make creative expression and collaboration more
      accessible to Blind and Low Vision (BLV) users by developing new tools for  artistic creation and effective communication. This project aims to empower BLV users with greater agency and opportunities to create, modify, and deeply engage with generated digital art, while also acting as a medium for visual communication. By exploring how I can leverage current AI models to create these tools, I seek to bridge the gap between visual and non-visual experiences, enabling inclusive and meaningful artistic collaboration.
    </div>
    <h3>Usage of AI Models</h3>

    <h4>Sketch to Image Model</h4>
    <div class = "instructions">
      <strong>Model:</strong> TencentARC/t2i-adapter-sketch-sdxl-1.0 <br/>
      <strong>Functionality:</strong> Converts sketches into detailed images to assist BLV users in creating expressive visuals. <br/>
    </div>

    <h4>Image to Text Description</h4>
    <div class = "instructions">
      <strong>Model:</strong> OpenAI GPT-4.0 <br/>
      <strong>Functionality:</strong> Generates textual descriptions of images to provide spatial and contextual understanding for BLV users. <br/>
    </div>

    <h4>Visual Question Answering (VQA) Model</h4>
    <div class="instructions">
      <strong>Model:</strong> Salesforce/blip-vqa-capfilt-large <br/>
      <strong>Functionality:</strong> Answers questions about an image to enhance interactive engagement with visual content. <br/>
    </div>
    <div class="row"></div>
    <div class="copyright">
      © Viswak Raja 2024
    </div>
  </div>
</main>



<style>
  .row>* {
    margin-bottom: 20px;
  }
  .row {
    gap: 20px;
  }

  .input-field {
    position: relative;
  }
  .input-field input[type=text] {
    min-width: 350px;
    width: calc(100% - 2 * 15px);
    height: 60px;
    border-radius: 6px;
    font-size: 18px;
    padding: 0 15px;
    border: 2px solid #fff;
    background: transparent;
    color: #fff;
    outline: none;
  }
  .input-field label {
    position: absolute;
    top: 50%;
    left: 15px;
    transform: translateY(-50%);
    color: #fff;
    font-size: 19px;
    pointer-events: none;
    transition: 0.3s;
  }
  input:focus {
    border: 2px solid #ffcc00;
  }
  input:focus ~ label,
  input:valid ~ label {
    top: 0;
    left: 15px;
    font-size: 16px;
    padding: 0 2px;
    background: #242424;
  }

  input[type=button] {
    background-color: #535bf2;
    border-radius: 25px;
    outline: none;
    border: none;
    padding: 15px;
    width: 100%;
    font-size: 25px;
    font-weight: bold;
  }

  input[type=button]:hover {
    background-color: #4049a3;
  }

  input[type=button]:active {
    background-color: #272c78;
  }
  .inp-and-submit > :not(:last-child) {
    margin-bottom: 25px;
  }
  .boosted-img {
    width: 600px;
    border-radius: 25px;
  }

  .descriptor {
    text-align: start;
    font-size: 18px;
  }

  .loading {
    width: 50px;
    margin-top: 25px;
  }
  main>* {
    max-width: 600px;
  }

  h1 {

    text-align: start;
  }
  h3 {
    text-align: start;
    font-size: 24px;
  }
  h4 {
    text-align: start;
    font-size: 20px;
  }
  .section-descriptor {
    text-align: start;
    margin-bottom: 20px;
  }
  .instructions {
    text-align: start;
    margin-bottom: 20px;
  }

  .vqa-answer {
    text-align: start;
    background: #4c4c4c;
    border-radius: 10px;
    padding: 20px;
    font-size: 20px;
  }

  .row::after {
    content: "";
    display: block;
    width: 100%;
    height: 2px;
    border-bottom: 1.5px solid #ffffff;
  }
  .copyright {
    margin-top: 25px;
  }
</style>
