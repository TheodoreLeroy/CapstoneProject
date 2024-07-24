import React from "react";
import "../styles/Slot.css"
import { useState } from "react";
import MultiStepProgressBar from "./MultiStepProgressBar";

const Slot = () =>{
    const [page, setPage] = useState("pageone");

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
        <p className="slot-number">Slot: 1</p>
        <p className="slot-name">Subject: </p>
        <p className="slot-class">Class: </p>
        <p className="slot-date">Date: </p>
        <MultiStepProgressBar page={page} onPageNumberClick={nextPageNumber} />
        {
            {
                pageone: <PageOne onButtonClick={nextPage} />,
                pagetwo: <PageTwo onButtonClick={nextPage} />,
                pagethree: <PageThree onButtonClick={nextPage} />,
                pagefour: <PageFour />,
            }[page]
        }
    </div>)
}
export default Slot; 