document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const textInput = document.getElementById('text-input');
    const difficultyBtns = document.querySelectorAll('.difficulty-btn');
    const generateBtn = document.getElementById('generate-btn');
    const quizSection = document.getElementById('quiz-section');
    const resultsSection = document.getElementById('results-section');
    const quizContainer = document.getElementById('quiz-container');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');
    const scoreDisplay = document.getElementById('score-display');
    const reviewList = document.getElementById('review-list');
    const downloadPdfBtn = document.getElementById('download-pdf-btn');
    const restartBtn = document.getElementById('restart-btn');

    let currentDifficulty = 'medium';
    let quizData = [];
    let currentQuestionIndex = 0;
    let userAnswers = [];

    // Handle difficulty selection
    difficultyBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            difficultyBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentDifficulty = btn.dataset.level;
            toggleGenerateBtn();
        });
    });

    // Enable/disable generate button based on input
    function toggleGenerateBtn() {
        const hasFile = fileInput.files.length > 0;
        const hasText = textInput.value.trim() !== '';
        generateBtn.disabled = !(hasFile || hasText);
    }

    fileInput.addEventListener('change', toggleGenerateBtn);
    textInput.addEventListener('input', toggleGenerateBtn);

    // Generate quiz button click
    generateBtn.addEventListener('click', async () => {
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';

        try {
            let text = '';

            // Get text from file or textarea
            if (fileInput.files.length > 0) {
                const file = fileInput.files[0];
                text = await extractTextFromFile(file);
            } else {
                text = textInput.value.trim();
            }

            if (!text) {
                alert('Please provide some text to generate a quiz from.');
                return;
            }

            // Determine question count based on text length
            const wordCount = text.trim().split(/\s+/).length;
            let questionCount;
            if (wordCount < 500) {
                questionCount = 5;
            } else if (wordCount < 1500) {
                questionCount = 10;
            } else if (wordCount < 3000) {
                questionCount = 15;
            } else {
                questionCount = 20;
            }

            // Call backend to generate quiz
            const response = await fetch('/api/generate_quiz', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    difficulty: currentDifficulty,
                    questionCount: questionCount
                })
            });

            if (!response.ok) {
                throw new Error(`Failed to generate quiz: ${response.statusText}`);
            }

            quizData = await response.json();

            // Initialize quiz
            currentQuestionIndex = 0;
            userAnswers = new Array(quizData.length).fill(null);
            showQuestion();
            quizSection.classList.remove('hidden');
            generateBtn.textContent = 'Generate Quiz';
        } catch (error) {
            console.error(error);
            alert('An error occurred while generating the quiz. Please try again.');
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Quiz';
        }
    });

    // Show current question
    function showQuestion() {
        quizContainer.innerHTML = '';
        if (currentQuestionIndex >= quizData.length) {
            showResults();
            return;
        }

        const question = quizData[currentQuestionIndex];
        const questionElement = document.createElement('div');
        questionElement.className = 'question';
        questionElement.innerHTML = `
            <h3>Question ${currentQuestionIndex + 1} of ${quizData.length}</h3>
            <p>${question.question}</p>
            <div class="options">
                ${question.options.map((option, index) => `
                    <label class="option">
                        <input type="radio" name="option" value="${index}" ${userAnswers[currentQuestionIndex] === index ? 'checked' : ''}>
                        ${option}
                    </label>
                `).join('')}
            </div>
        `;
        quizContainer.appendChild(questionElement);

        // Update navigation buttons
        prevBtn.disabled = currentQuestionIndex === 0;
        nextBtn.textContent = currentQuestionIndex === quizData.length - 1 ? 'Submit' : 'Next';
    }

    // Handle option selection
    quizContainer.addEventListener('change', (e) => {
        if (e.target.name === 'option') {
            userAnswers[currentQuestionIndex] = parseInt(e.target.value);
        }
    });

    // Navigation buttons
    prevBtn.addEventListener('click', () => {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            showQuestion();
        }
    });

    nextBtn.addEventListener('click', () => {
        if (currentQuestionIndex < quizData.length - 1) {
            currentQuestionIndex++;
            showQuestion();
        } else {
            // Submit quiz
            submitQuiz();
        }
    });

    // Submit quiz
    function submitQuiz() {
        // Calculate score
        let score = 0;
        quizData.forEach((question, index) => {
            if (userAnswers[index] === question.correct_index) {
                score++;
            }
        });

        // Show results
        scoreDisplay.textContent = `Your score: ${score} out of ${quizData.length}`;

        // Build review list
        reviewList.innerHTML = '';
        quizData.forEach((question, index) => {
            const reviewItem = document.createElement('div');
            reviewItem.className = 'review-item';
            const isCorrect = userAnswers[index] === question.correct_index;
            reviewItem.innerHTML = `
                <h4>Question ${index + 1}: ${question.question}</h4>
                <p><strong>Your answer:</strong> ${question.options[userAnswers[index]]}</p>
                <p><strong>Correct answer:</strong> <span class="${isCorrect ? 'correct' : 'incorrect'}">${question.options[question.correct_index]}</span></p>
                <p><strong>Explanation:</strong> ${question.explanation}</p>
            `;
            reviewList.appendChild(reviewItem);
        });

        quizSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');
    }

    // Download PDF
    downloadPdfBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/generate_pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    quizData: quizData,
                    userAnswers: userAnswers
                })
            });

            if (!response.ok) {
                throw new Error('Failed to generate PDF');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'quizmate-quiz.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error(error);
            alert('Failed to generate PDF. Please try again.');
        }
    });

    // Restart button
    restartBtn.addEventListener('click', () => {
        // Reset form
        fileInput.value = '';
        textInput.value = '';
        difficultyBtns.forEach(btn => btn.classList.remove('active'));
        difficultyBtns[1].classList.add('active'); // Medium
        currentDifficulty = 'medium';
        quizSection.classList.add('hidden');
        resultsSection.classList.add('hidden');
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generate Quiz';
    });

    // Helper function to extract text from file
    async function extractTextFromFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || 'Failed to extract text from file');
    }

    const data = await response.json();
    return data.text;
}
});