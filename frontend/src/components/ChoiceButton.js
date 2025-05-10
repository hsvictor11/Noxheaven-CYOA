const ChoiceButton = ({ text, onSelect }) => {
  return (
    <button className="choice-button" onClick={onSelect}>
      {text}
    </button>
  );
};

export default ChoiceButton;