import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { notification } from "antd";

import LoadingIndicator from "./LoadingIndicator";
import api from "../api";

import "../styles/FormClass.css"

function FormClass({ route }) {
    const [class_name, setClassName] = useState("");
    const [semester, setSemester] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const message = "Create new class";

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            api.post("addClass/", { class_name, semester })
                .then((res) => {
                    if (res.status === 201) {
                        notification.success({
                        message: 'Success',
                        description: `Class created successfully!
                                    Please refrest to see it in class`,
                        placement: 'topRight',
                        duration: 3,
                    });
                    }
                }).catch((e) => {
                    notification.error({
                        message: 'Error',
                        description: e.response.data.class_name,
                        duration: 3,
                    });
                });
        } catch (Error) {
            alert(Error)
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
                value={class_name}
                onChange={(e) => setClassName(e.target.value)}
                placeholder="Class Name"
            />
            <input
                className="form-input"
                type="text"
                value={semester}
                onChange={(e) => setSemester(e.target.value)}
                placeholder="Semester"
            />
            {loading && <LoadingIndicator />}
            <button className="form-button" type="submit" disabled={loading}>
                {message}
            </button>
        </form>
    );
}

export default FormClass

