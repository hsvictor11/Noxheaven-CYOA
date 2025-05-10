import React, { useState } from 'react';
import './App.css';
import ChoiceButton from './components/ChoiceButton';
import axios from 'axios';

function App() {
  const [currentText, setCurrentText] = useState("Welcome to Noxheaven. What will you do?");
  const [choices, setChoices] = useState([
    { id: 1, text: "Host an Evil Ladies event" },
    { id: 2, text: "Visit The Velvet Lounge" },
  ]);

const handleChoice = async (choiceId) => {
  try {
    const response = await axios.post('http://localhost:5000/process-choice', {
      choiceId: choiceId,
    });
    setCurrentText(response.data.new_text);
    setChoices(response.data.new_choices);
  } catch (error) {
    console.error("Error:", error);
  }
};

  return (
    <div className="App">
      <h1>Noxheaven CYOA</h1>
      <div className="game-container">
        <div className="story-text">{currentText}</div>
        <div className="choices-container">
          {choices.map((choice) => (
            <ChoiceButton
              key={choice.id}
              text={choice.text}
              onSelect={() => handleChoice(choice.id)}
            />
          ))}
        </div>
        <div className="stats-container">
          <h3>Evil Ladies Reputation: Low</h3>
          <h3>Obsidian Order Progress: 0%</h3>
        </div>
      </div>
    </div>
  );
}

export default App;