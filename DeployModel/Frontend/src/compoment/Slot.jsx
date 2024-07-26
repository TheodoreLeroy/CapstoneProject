import React from "react";
import "../styles/Slot.css"
import { useState } from "react";
import MultiStepProgressBar from "./MultiStepProgressBar";
import PageOne from "./Pages/PageOne";

const Slot = () => {
    const [page, setPage] = useState("pageone");
    const [isRunning, setIsRunning]= useState(false)


    const [numberSlot, setNumberSlot] = useState(1);
    const [nameSubject, setNameSubject] = useState("Math");
    const [nameClass, setNameClass] = useState("5C");
    const [date, setDate] = useState(new Date());


    const nextPage = (page) => {
        setPage(page);
    };

    const nextPageNumber = (pageNumber) => {
        switch (pageNumber) {
            case "1":
                setPage("pageone");
                break;
            case "2":
                setPage("pagetwo");
                break;
            case "3":
                setPage("pagethree");
                break;
            case "4":
                alert("Ooops! Seems like you did not fill the form.");
                break;
            default:
                setPage("1");
        }
    };
    return (<div className="slot-container">
        <div className="slot-infomation">
            <p className="slot-number">Slot: {numberSlot}</p>
            <p className="slot-name">Subject: {nameSubject}</p>
            <p className="slot-class">Class: {nameClass}</p>
            <p className="slot-date">Date: {date.toDateString()}</p>
            <button className="btn" onClick={() => { setIsRunning(true) }}>Run</button>
        </div>
        <MultiStepProgressBar page={page} onPageNumberClick={nextPageNumber} isRunning={isRunning} className="class-attendent" />
        {
            {
                pageone: <PageOne onButtonClick={nextPage} />,
                pagetwo: <PageOne onButtonClick={nextPage} />,
                pagethree: <PageOne onButtonClick={nextPage} />,
                pagefour: <PageOne />,
            }[page]
        }
    </div>)
}
export default Slot; 