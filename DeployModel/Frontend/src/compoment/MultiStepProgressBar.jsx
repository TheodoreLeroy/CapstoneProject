import React, { useState, useEffect } from "react";
import "../styles/MultiStepProgressBar.css";
import { ProgressBar, Step } from "react-step-progress-bar";

const MultiStepProgressBar = ({ page, onPageNumberClick, isRunning, totalSteps }) => {
    const [stepPercentage, setStepPercentage] = useState(0);

    useEffect(() => {
        if (stepPercentage < 100 && isRunning) {
            setTimeout(() => setStepPercentage(prev => prev + (100 / (totalSteps * 20))), 50);
        }
    }, [stepPercentage, isRunning, totalSteps]);

    return (
        <ProgressBar percent={stepPercentage} width={"75%"} height={"5px"} filledBackground={"rgb(22,119,255)"}>
            {Array.from({ length: totalSteps }).map((_, index) => (
                <Step key={index} style={{ backgroundColor: "rgb(22,119,255)" }}>
                    {({ accomplished }) => (
                        <div
                            className={`indexedStep ${accomplished ? "accomplished" : ""}`}
                            onClick={() => onPageNumberClick((index + 1).toString())}
                        >
                            {index + 1}
                        </div>
                    )}
                </Step>
            ))}
        </ProgressBar>
    );
};

export default MultiStepProgressBar;
