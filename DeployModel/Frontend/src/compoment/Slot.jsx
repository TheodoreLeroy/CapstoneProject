import React, { useState, useEffect } from "react";

import GetDataFromRoute from "./GetDataFromBackend";
import MultiStepProgressBar from "./MultiStepProgressBar";
import PageOne from "./Pages/PageOne";

import "../styles/Slot.css"

const Slot = (params) => {
    const totalSteps = 15;
    const [page, setPage] = useState("pageone");
    const [isRunning, setIsRunning] = useState(false)

    const [slotInfomation, setSlotInfomation] = useState([])
    const [students, setStudents] = useState([]);

    useEffect(() => {
        getStudents();
        getSlot();
    }, [])

    const getStudents = async () => {
        const studentData = await GetDataFromRoute(`studentsClass${params.params.idClass}/`)
        setStudents(studentData);
    }
    const getSlot = async () => {
        const slotData = await GetDataFromRoute(`slot${params.params.idSlot}/`)
        setSlotInfomation(slotData[0]);
    }

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
    return (<div className="slot-container-main">
        <div className="slot-infomation">
            <p className="slot-number">Slot: {slotInfomation.id}</p>
            <p className="slot-name">Subject: {slotInfomation.subject}</p>
            <p className="slot-class">ClassId: {slotInfomation.class_id} </p>
            <p className="slot-date">Date: {slotInfomation.time_start} - {slotInfomation.time_end}</p>
            <button className="btn" onClick={() => { setIsRunning(true) }}>Run</button>
        </div>
        <MultiStepProgressBar page={page} onPageNumberClick={nextPageNumber} isRunning={isRunning} className="class-attendent" totalSteps={totalSteps} />
        {
            // in working....................................................
            {
                pageone: <PageOne students={students} onButtonClick={nextPage} />,
                pagetwo: <PageOne students={students} onButtonClick={nextPage} />,
                pagethree: <PageOne students={students} onButtonClick={nextPage} />,
                pagefour: <PageOne />,
            }[page]
        }
    </div>)
}
export default Slot; 