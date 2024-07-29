import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import LoadingIndicator from "./LoadingIndicator";
import api from "../api"; 

import "../styles/Form.css"

function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const message = method === "login" ? ["Login", "Register", "Already have account? Try "] : ["Register", "Login", "Don't have account? Try "];

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            // const res = await api.post(route, { username, password })
            if (method === "login") {
                // localStorage.setItem(ACCESS_TOKEN, res.data.access);
                // localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                navigate("/home")
            } else {
                navigate("/login")
            }
        } catch (error) {
            alert(error)
        } finally {
            setLoading(false)
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>{message[0]}</h1>
            <input
                className="form-input"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
            />
            <input
                className="form-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />
            {loading && <LoadingIndicator />}
            <button className="form-button" type="submit">
                {message[0]}
            </button>
            <nav >
                {message[2]} <a href={`/${message[1]}`}>{message[1]}</a>
            </nav>
        </form>
    );
}

export default Form

