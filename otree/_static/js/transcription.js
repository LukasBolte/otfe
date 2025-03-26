"use strict";

function transcription(parameters) {
    this.root = parameters.root;
    this.csvFile = parameters.csvFile; 
    this.keyboardLetters = parameters.keyboardLetters; 
    this.transcriptionArea = []; 
    this.currentRowIndex = parameters.startingRowIndex || 0; // Use the starting row index from parameters
    this.rows = []; 
    this.correctAttempts = 0; 
    this.incorrectAttempts = 0; 
    this.successfulTranscriptionsDiv = null; 
    this.paymentPerSuccess = parameters.paymentPerSuccess; 
    this.maxMistakes = parameters.maxMistakes; // Maximum allowed mistakes
    this.submitCooldown = parameters.submitCooldown; // Add the cooldown parameter
    this.mistakeMessage = parameters.mistakeMessage; // Add the mistake message parameter
    this.successMessage = parameters.successMessage; // Add the success message parameter
    this.cacheUniqueID = parameters.cacheUniqueID; // Add the cacheUniqueID parameter
    this.work_period_length = parameters.work_period_length; // Add the work_period_length parameter
    this.blurLevel = parameters.blurLevel; // Add the blurLevel parameter
    this.varName = parameters.varName; // Add the varName parameter
    this.training = parameters.training !== undefined ? parameters.training : false; // Default to false

    // Load progress from localStorage
    const savedData = JSON.parse(localStorage.getItem(this.cacheUniqueID+'transcriptionProgress'));
    if (savedData) {
        this.correctAttempts = savedData.correctAttempts;
        this.incorrectAttempts = savedData.incorrectAttempts;
        this.currentRowIndex = savedData.currentRowIndex;
    }

    // Initialize hidden input field with current progress
    const correctAttemptsJSON = JSON.stringify({
        correctAttempts: this.correctAttempts, 
        incorrectAttempts: this.incorrectAttempts
    });
    
    if (document.getElementById(this.varName)) {
        document.getElementById(this.varName).value = correctAttemptsJSON;
    }

    const greekMapping = {
        "alpha": "α",
        "beta": "β",
        "gamma": "γ",
        "delta": "δ",
        "epsilon": "ε",
        "zeta": "ζ",
        "eta": "η",
        "theta": "θ",
        "iota": "ι",
        "kappa": "κ",
        "lambda": "λ",
        "mu": "μ",
        "nu": "ν",
        "xi": "ξ",
        "omicron": "ο",
        "pi": "π",
        "rho": "ρ",
        "sigma": "σ",
        "tau": "τ",
        "upsilon": "υ",
        "phi": "φ",
        "chi": "χ",
        "psi": "ψ",
        "omega": "ω",
        "period": ".",
        "comma": ","
    };

    // Create modal structure
    this.createModal = function() {
        const modalHtml = `
            <div class="modal fade" id="transcriptionModal" tabindex="-1" aria-labelledby="transcriptionModalLabel" aria-hidden="true">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="transcriptionModalLabel">Transcription Result</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body" id="modalMessage">
                            <!-- Message will be inserted here -->
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>`;
        
        // Append modal to the body
        document.body.insertAdjacentHTML('beforeend', modalHtml);
    };


    this.drawTranscription = function(blurryText) {
        // Create a main container div (the box)
        const container = document.createElement('div');
        container.style.border = "2px solid black"; // Create a solid border
        container.style.padding = "20px"; // Add some padding inside the box
        container.style.margin = "20px auto"; // Center the box horizontally
        container.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.1)"; // Add a subtle shadow for a box effect
        container.style.borderRadius = "8px"; // Rounded corners for a smoother look


        if (!this.successfulTranscriptionsDiv) {
            this.successfulTranscriptionsDiv = document.createElement('div');
            container.appendChild(this.successfulTranscriptionsDiv);
        }
        this.updateSuccessfulTranscriptionsDisplay(); 

        const paymentDiv = document.createElement('div');
        paymentDiv.style.marginTop = "5px"; 
        paymentDiv.innerHTML = `<b>Gross payment per successful transcription:</b> $${(this.paymentPerSuccess / 100).toFixed(2)}`; 
        container.appendChild(paymentDiv); 

        // Add the reminder text
        const reminderDiv = document.createElement('div');
        reminderDiv.style.marginTop = "5px"; // Add some space above the reminder
        reminderDiv.innerHTML = "<b>Reminder:</b> There is no obligation to work for the full " + this.work_period_length + "-minute work period, but you will only be able to proceed after the " + this.work_period_length + "-minute work period is over. You can complete as many transcriptions as you like during the work period."; 
        if (!this.training) {
            container.appendChild(reminderDiv); // Add reminder text to the container
        }
        

        // 3. Create the blurry text display
        const blurryTextDiv = document.createElement('div');
        blurryTextDiv.style.display = "flex"; // To make the letters align side by side
        blurryTextDiv.style.marginTop = "20px"; // Add some space above the blurry text
        blurryTextDiv.style.justifyContent = "center"; // Center the blurry text

        blurryText.forEach(letter => {
            const letterSpan = document.createElement('span');
            letterSpan.innerText = letter; // Set the letter text (now Greek letters)
            letterSpan.style.fontSize = "40px"; // Adjust the font size
            letterSpan.style.filter = this.blurLevel; // Increased blur effect
            letterSpan.style.marginRight = "10px"; // Add some spacing between letters
            blurryTextDiv.appendChild(letterSpan);
        });

        this.transcriptionDiv = document.createElement('div');
        this.transcriptionDiv.style.display = "flex"; 
        this.transcriptionDiv.style.border = "1px solid black";
        this.transcriptionDiv.style.padding = "10px";
        this.transcriptionDiv.style.minHeight = "60px"; 

        const keyboardDiv = document.createElement('div');
        keyboardDiv.style.display = "flex"; 
        keyboardDiv.style.marginTop = "20px";
        keyboardDiv.style.justifyContent = "center"; // Center the keyboard


        this.keyboardLetters.forEach(letter => {
            const letterButton = document.createElement('button');
            letterButton.innerText = letter.char; // Set the letter as button text
            letterButton.type = "button"; // Set the button type
            letterButton.style.marginRight = "0px"; // Add some spacing between letters
            letterButton.style.fontSize = "24px"; // Increase the font size for readability
            letterButton.style.width = "40px"; // Set a fixed width for uniformity
            letterButton.onclick = () => {
                this.transcriptionArea.push(letter.char); // Add clicked letter to transcriptionArea
                const selectedLetter = document.createElement('span'); // Create a span for each letter
                selectedLetter.innerText = letter.char; // Display the letter
                selectedLetter.style.marginRight = "10px"; // Add some spacing between letters
                selectedLetter.style.fontSize = "24px"; // Increase the font size for readability
                this.transcriptionDiv.appendChild(selectedLetter);
            };
            keyboardDiv.appendChild(letterButton);
        });

        // 7. Create the Undo button
        const undoButton = document.createElement('button');
        undoButton.innerText = "Undo";
        undoButton.type = "button"; 
        undoButton.className = "btn btn-warning btn-large"; // Add Bootstrap classes
        undoButton.style.marginTop = "20px";
        undoButton.onclick = () => {
            if (this.transcriptionArea.length > 0) {
                this.transcriptionArea.pop(); // Remove the last letter from the transcription area
                this.transcriptionDiv.removeChild(this.transcriptionDiv.lastChild); // Remove the last displayed letter
            }
        };

        // 8. Create the Submit button
        const submitButton = document.createElement('button');
        submitButton.innerText = "Submit";
        submitButton.className = "btn btn-success btn-large"; // Add Bootstrap classes
        submitButton.id = "submitButton"; // Add an ID for easier access
        submitButton.style.marginLeft = "10px"; // Space between Undo and Submit
        submitButton.disabled=true;
        setTimeout(() => {
            document.getElementById("submitButton").disabled = false;  // Re-enable after cooldown
        }, this.submitCooldown * 1000); // Convert seconds to milliseconds

        submitButton.onclick = () => {
            // Disable the submit button
          
    
            this.checkTranscription(blurryText); // Check the transcription when submitting
        };

        // 6. Create a container for the Undo and Submit buttons
        const buttonContainer = document.createElement('div');
        buttonContainer.style.display = "flex"; // Use flexbox for alignment
        buttonContainer.style.justifyContent = "space-between"; // Space between buttons
        buttonContainer.style.alignItems = "center"; // Align items vertically
        buttonContainer.style.marginTop = "20px"; // Add some margin above the buttons

        // Append buttons to the button container
        buttonContainer.appendChild(undoButton); // Add the Undo button to the container
        buttonContainer.appendChild(submitButton); // Add the Submit button to the container
        



        // Append all elements to the container
        container.appendChild(this.successfulTranscriptionsDiv); // Add the successful transcriptions div
        container.appendChild(paymentDiv); // Add payment display to the container
        container.appendChild(blurryTextDiv);
        container.appendChild(this.transcriptionDiv);
        container.appendChild(keyboardDiv);
        container.appendChild(buttonContainer); // Add the button container to the main container

        
        document.getElementById(this.root).innerHTML = ''; // Clear the root element
        document.getElementById(this.root).appendChild(container);

        // Conditionally add the "Next" button
        if (this.training) {
            const nextButton = document.createElement('button');
            nextButton.innerText = "Next";
            nextButton.className = "btn btn-primary btn-large otree-btn-next"; // Add Bootstrap classes
            nextButton.style.float = "right"; // Float to the right
            nextButton.disabled = this.correctAttempts <= 4; // Disable initially

            nextButton.onclick = () => {
                this.loadBlurryTextFromCurrentRow(); // Load the next row when clicked
                document.getElementById("myNextID").click(); // Click the hidden "Next" button
                
            };

            const nextButtonContainer = document.createElement('div');
            // Add the "Next" button to the container
            // nextButtonContainer.appendChild(nextButton);
            
            // Insert the container as a sibling after the existing element
            document.getElementById(this.root).appendChild(nextButton); // Correctly insert after the container

            // container.appendChild(nextButtonContainer); // Add the "Next" button container
        }
    };

    // Disable Submit Button Method
    
    this.loadRowsFromCSV = function() {
        fetch(this.csvFile)
            .then(response => response.text())
            .then(data => {
                this.rows = data.split('\n').map(row => 
                    row.split(',').map(letter => letter.trim())
                ); 
                this.loadBlurryTextFromCurrentRow(); 
            })
            .catch(error => console.error("Error loading CSV file:", error));
    };

    this.loadBlurryTextFromCurrentRow = function() {
        if (this.currentRowIndex < this.rows.length) {
            const currentRow = this.rows[this.currentRowIndex];

            const blurryText = currentRow.map(letter => {
                if (letter.length === 0) {
                    return ' '; 
                }
                return greekMapping[letter] || letter; 
            });

            this.drawTranscription(blurryText);

            this.transcriptionArea = [];
            this.transcriptionDiv.innerHTML = ''; 
        } else {
            console.log("No more rows to process.");
        }
    };

    this.checkTranscription = function(blurryText) {
        const expectedText = blurryText.join('').trim();
        const userText = this.transcriptionArea.join('').trim();
        const isCorrect = this.calculateMistakes(expectedText, userText) <= this.maxMistakes;

        if (isCorrect) {
            this.correctAttempts++;
            this.showModal(this.successMessage);
        } else {
            this.incorrectAttempts++;
            this.showModal(this.mistakeMessage);
        }

        console.log(`Transcription is ${isCorrect ? "correct" : "incorrect"}. Expected: "${expectedText}", Got: "${userText}"`);

        this.updateSuccessfulTranscriptionsDisplay();

        // Save progress to localStorage
        localStorage.setItem(this.cacheUniqueID+'transcriptionProgress', JSON.stringify({
            correctAttempts: this.correctAttempts,
            incorrectAttempts: this.incorrectAttempts,
            currentRowIndex: this.currentRowIndex
        }));

        // Save correctAttempts as JSON in the hidden input field
        const correctAttemptsJSON = JSON.stringify({ correctAttempts: this.correctAttempts, incorrectAttempts: this.incorrectAttempts });
        document.getElementById(this.varName).value = correctAttemptsJSON;

        this.currentRowIndex++;
        this.loadBlurryTextFromCurrentRow(); 
    };

    this.calculateMistakes = function(expected, actual) {
        let mistakes = 0;
    
        // Trim trailing spaces
        expected = expected.trim();
        actual = actual.trim();
    
        console.log("Expected:", expected);
        console.log("Actual:", actual);
    
        const maxLength = Math.max(expected.length, actual.length);
        for (let i = 0; i < maxLength; i++) {
            if (expected[i] !== actual[i]) {
                mistakes++;
            }
        }
    
        return mistakes; // Return the total number of mistakes
    };

    this.updateSuccessfulTranscriptionsDisplay = function() {
        this.successfulTranscriptionsDiv.style.marginTop = "5px"; 
        this.successfulTranscriptionsDiv.innerHTML = `<b>Transcriptions successfully completed this period:</b> ${this.correctAttempts} (incorrect attempts: ${this.incorrectAttempts})`;
    };

    this.showModal = function(message) {
        document.getElementById("modalMessage").innerText = message; // Set the modal message
        $('#transcriptionModal').modal('show'); // Show the modal
    };

    this.createModal();
    this.loadRowsFromCSV(); 
}