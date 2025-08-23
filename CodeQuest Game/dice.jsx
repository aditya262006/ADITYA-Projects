import React, { useState } from "react";

export default function Dice({ onRoll, lastRoll }) {
  const [rolling, setRolling] = useState(false);

  function triggerRoll() {
    if (rolling) return;
    setRolling(true);
    setTimeout(() => {
      onRoll();
      setRolling(false);
    }, 900); // animation length
  }

  return (
    <div className="dice-control">
      <div className={`dice-box ${rolling ? "rolling" : ""}`}>
        <div className="dot tl"></div>
        <div className="dot tr"></div>
        <div className="dot center"></div>
        <div className="dot bl"></div>
        <div className="dot br"></div>
      </div>
      <button onClick={triggerRoll} className="roll-btn">{rolling ? "Rolling..." : "Roll Dice"}</button>
      <div className="last-roll">Last: {lastRoll ?? "-"}</div>
    </div>
  );
}
