import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { notification, TimePicker, Select } from "antd";

import LoadingIndicator from "./LoadingIndicator";
import api from "../api";
import dayjs from 'dayjs';

import "../styles/FormSlot.css"

function FormSlot({ route }) {
    const [subject, setSubject] = useState("");
    const [time_start, setTimeStart] = useState("");
    const [time_end, setTimeEnd] = useState(null);
    const [loading, setLoading] = useState(false);
    const [class_id, setClassId] = useState(null);
    const navigate = useNavigate();

    const message = "Create new slot";

    const [classNames, setClassNames] = useState([]);

    useEffect(() => {
        getClass();
    }, [])

    const getClass = () => {
        api.get("classes/detail")
            .then((res) => res.data)
            .then((data) => { setClassNames(data); console.log(data); })
            .catch((e) => {
                alert(e)
            })
    }

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();


        try {
            api.post(route, { class_id, subject, time_start, time_end })
                .then((res) => {
                    if (res.status === 201) notification.success({
                        message: 'Success',
                        description: `Slot created successfully!
                                    Please refrest to see it in class`,
                        placement: 'topRight',
                        duration: 3,
                    });
                    navigate("/attendent")
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
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="Subject"
            />
            <TimePicker.RangePicker
                format="HH:mm"
                onChange={(e) => {
                    setTimeStart(e[0].format('HH:mm:ss'));
                    setTimeEnd(e[1].format('HH:mm:ss'));
                }}
                defaultValue={[
                    dayjs('00:00', 'HH:mm'),
                    dayjs('23:59', 'HH:mm'),
                ]}
            />
            <Select className="ant-select-selector"
                value={class_id}
                onChange={setClassId}
                placeholder="Select an option"
                style={{ width: 200 }}
            >
                {[classNames?.map((className) => (
                    <Select.Option key={className.id} value={className.id} >{className.class_name}</Select.Option>
                ))]}
            </Select>
            {loading && <LoadingIndicator />}
            <button className="form-button" type="submit" disabled={loading}>
                {message}
            </button>
        </form>
    );
}

export default FormSlot

