import React, {useState, useEffect} from "react";
import "../styles/MultiStepProgressBar.css";
import { ProgressBar, Step } from "react-step-progress-bar";

const MultiStepProgressBar = ({ page, onPageNumberClick, isRunning}) => {
    const [stepPercentage, setStepPercentage] = useState(0);

    useEffect(() => {
        if (stepPercentage < 100 && isRunning) {
            setTimeout(() => setStepPercentage(prev => prev += ((100/60)/20)), 50)
        }
    }, [stepPercentage, isRunning])

    return (
        <ProgressBar percent={stepPercentage} width={"75%"} height={"5px"} filledBackground={"rgb(22,119,255)"}>
            <Step style={{ backgroundColor:"rgb(22,119,255)" }}>
                {({ accomplished, index }) => (
                    <div
                        className={`indexedStep ${accomplished ? "accomplished" : null}`}
                        onClick={() => onPageNumberClick("1")}
                    >
                        {index + 1}
                    </div>
                )}
            </Step>
            <Step>
                {({ accomplished, index }) => (
                    <div
                        className={`indexedStep ${accomplished ? "accomplished" : null}`}
                        onClick={() => onPageNumberClick("2")}
                    >
                        {index + 1}
                    </div>
                )}
            </Step>
            <Step>
                {({ accomplished, index }) => (
                    <div
                        className={`indexedStep ${accomplished ? "accomplished" : null}`}
                        onClick={() => onPageNumberClick("3")}
                    >
                        {index + 1}
                    </div>
                )}
            </Step>
            <Step>
                {({ accomplished, index }) => (
                    <div
                        className={`indexedStep ${accomplished ? "accomplished" : null}`}
                        onClick={() => onPageNumberClick("4")}
                    >
                        {index + 1}
                    </div>
                )}
            </Step>
            <Step>
                {({ accomplished, index }) => (
                    <div
                        className={`indexedStep ${accomplished ? "accomplished" : null}`}
                        onClick={() => onPageNumberClick("4")}
                    >
                        {index + 1}
                    </div>
                )}
            </Step>
        </ProgressBar>
    );
};

export default MultiStepProgressBar;
