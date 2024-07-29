import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import LoadingIndicator from "./LoadingIndicator";
import api from "../api";

import "../styles/FormClass.css"

function FormClass({ route }) {
    const [ClassName, setClassName] = useState("");
    const [Semester, setSemester] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const message = "Create new class";

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            const res = await api.post("addClass/", { ClassName, Semester });
            window.location.reload();
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
                value={ClassName}
                onChange={(e) => setClassName(e.target.value)}
                placeholder="Class Name"
            />
            <input
                className="form-input"
                type="text"
                value={Semester}
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

