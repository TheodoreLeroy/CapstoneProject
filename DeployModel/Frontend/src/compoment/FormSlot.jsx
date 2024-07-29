import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { notification, TimePicker, Select } from "antd";

import LoadingIndicator from "./LoadingIndicator";
import api from "../api";

import "../styles/FormSlot.css"

function FormSlot({ route }) {
    const [slotId, setSlotId] = useState("");
    const [subject, setSubject] = useState("");
    const [timeStart, setTimeStart] = useState(null);
    const [timeEnd, setTimeEnd] = useState(null);
    const [loading, setLoading] = useState(false);
    const [selectedOption, setSelectedOption] = useState(null);
    const navigate = useNavigate();

    const message = "Create new slot";

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        const timeStartFormatted = timeStart ? timeStart.format("HH:mm:ss") : null;
        const timeEndFormatted = timeEnd ? timeEnd.format("HH:mm:ss") : null;

        try {
            api.post(route, { ClassName, Semester })
                .then((res) => {
                    if (res.status === 201) notification.success({
                        message: 'Success',
                        description: `Slot created successfully!
                                    Please refrest to see it in class`,
                        placement: 'topRight',
                        duration: 3,
                    });
                });
        } catch (error) {
            alert(error)
        } finally {
            setLoading(false)
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>Create new class</h1>
            <input
                className="form-input"
                type="text"
                value={slotId}
                onChange={(e) => setClassName(e.target.value)}
                placeholder="Slot id"
            />
            <input
                className="form-input"
                type="text"
                value={subject}
                onChange={(e) => setSemester(e.target.value)}
                placeholder="Subject"
            />
            <TimePicker className="timePicker"
                value={timeStart}
                onChange={setTimeStart}
                format="HH:mm:ss"
            />
            <TimePicker className="timePicker"
                value={timeEnd}
                onChange={setTimeEnd}
                format="HH:mm:ss"
            />
            <Select className="ant-select-selector"
                value={selectedOption}
                onChange={setSelectedOption}
                placeholder="Select an option"
                style={{ width: 200 }}
            >
                <Option value="option1">Option 1</Option>
                <Option value="option2">Option 2</Option>
                <Option value="option3">Option 3</Option>
            </Select>
            {loading && <LoadingIndicator />}
            <button className="form-button" type="submit" disabled={loading}>
                {message}
            </button>
        </form>
    );
}

export default FormSlot

