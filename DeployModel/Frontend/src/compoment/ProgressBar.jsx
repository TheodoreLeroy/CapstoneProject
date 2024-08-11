import React, { useState, useEffect } from 'react';
import { Button, InputNumber, Progress } from 'antd';
import dayjs from 'dayjs';

const ProgressBar = ({isRunning, duration}) => {
    const [time, setTime] = useState(duration); // Time in milliseconds
    const [initialTime, setInitialTime] = useState(duration); // Store initial time for reset

    useEffect(() => {
        let interval;

        if (isRunning && time > 0) {
            interval = setInterval(() => {
                setTime(prevTime => {
                    if (prevTime <= 1000) {
                        clearInterval(interval);
                        isRunning = false;
                        return 0;
                    }
                    return prevTime - 1000;
                });
            }, 1000); // Update time every second
        }

        return () => clearInterval(interval); // Cleanup interval on component unmount
    }, [isRunning,time]);

    useEffect(() =>{
        setTime(duration);
        setInitialTime(duration);
    }, [isRunning])

    const startPause = () => {
        if (time > 0) {
            isRunning = false;
        }
    };

    const formatTime = (time) => {
        const seconds = (`0${Math.floor((time / 1000) % 60)}`).slice(-2);
        const minutes = (`0${Math.floor((time / 60000) % 60)}`).slice(-2);
        const hours = (`0${Math.floor(time / 3600000)}`).slice(-2);

        return `${hours}:${minutes}:${seconds}`;
    };

    const progressPercent = 100 - (time / initialTime) * 100;

    return (
        <div style={{ textAlign: 'left', marginTop: '50px' }}>
            {isRunning ? <> <div style={{ fontSize: "24px"}}>
                {formatTime(time)}
            </div>
            <Progress
                percent={progressPercent}
                strokeColor="rgb(24, 144, 255)"
                style={{ marginTop: '10px', marginBottom: '20px' }}
                showInfo={false}
            /></> : <></>}
        </div>
    );
};

export default ProgressBar;
